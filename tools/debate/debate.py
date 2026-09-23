#!/usr/bin/env python3
"""Claude と Codex の最上位モデルを交互に呼び、1つの論点を往復させて最終回答を出す。

使い方:
  tools/debate/debate.py "論点"                       # 既定: 5ラウンド、参照は hello-dining.md と decisions.md
  tools/debate/debate.py @question.md --refs a.md b.md --rounds 3
  tools/debate/debate.py "論点" --mock-codex           # Codex 未導入時。Codex 役を Claude(Opus) で代替

出力: debates/<日付>-<slug>/ に transcript.md（gitignore）と final.md（commit 対象）
"""
import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REFS = ["hello/hello-dining.md", "decisions.md"]
NO_OBJECTION = "新しい反論なし"

COMMON_SYSTEM = """あなたは経営者の壁打ち相手。相手は複数社を横断して見る経営者で、事業企画から開発まで自分で見る。技術も事業も噛み砕かなくていい。
ルール:
- 日本語。1行目は結論。根拠は箇条書きで1項目1理由。
- 事実は与えられた前提ファイルから引く。前提にないことは「推測」と明示する。
- 造語・比喩・抽象語を避ける。数字で語れるものは数字で語る。
- 既出の論点を繰り返さない。議事に書いてあることを言い直さない。
- 全体15行以内。"""

PROPOSER_TASK = """あなたの役割は「提案側」。
これまでの議事にある反論を全部踏まえ、論点に対する現時点で最も強い答えを出す。
- 反論のうち受け入れるものは取り込んで答えを修正する。受け入れないものは1行で理由を言う。
- 結論を曖昧にしない。条件付きなら条件を明記する。"""

CRITIC_TASK = f"""あなたの役割は「反論側」。
直前の提案を崩す。目的は勝つことではなく、経営者が見落とす前提・因果の飛び・事実の誤りを出すこと。
- 出すのは議事にまだ出ていない反論だけ。最大3つ。1反論=結論1行+根拠1〜2行。
- 反論のたびに「提案のどの一文に対する反論か」を明示する。
- 事実の誤りは前提ファイルの該当箇所を引いて示す。
- 新しい反論が本当に無いなら、本文を「{NO_OBJECTION}」の1行だけにする。無理に出さない。"""

FINAL_TASK = """あなたの役割は「最終回答」。議事全体を読み、論点への答えを経営者に返す。
出力の型（厳守）:
- 1行目は結論。空行で区切る
- 根拠は箇条書き。1項目=1理由=1行。因果のステップは削らない
- 全体10行以内
- 最後に「残る反論:」として、議事で決着しなかった反論を最大2行。無ければ書かない
- 一文一義。1文40〜50字まで。略語は初出時に展開。造語・比喩を使わない
- 論点表・議事の要約・双方の主張の列挙はしない。答えだけ書く"""


def slugify(text: str, limit: int = 40) -> str:
    s = re.sub(r"\s+", "-", text.strip())
    s = re.sub(r"[^\w\-ぁ-んァ-ン一-龥]", "", s)
    return s[:limit] or "debate"


def read_refs(refs):
    parts = []
    for r in refs:
        p = (ROOT / r) if not Path(r).is_absolute() else Path(r)
        if not p.exists():
            sys.exit(f"参照ファイルが見つかりません: {p}")
        parts.append(f"### {r}\n\n{p.read_text(encoding='utf-8').strip()}\n")
    return "\n".join(parts)


class Runner:
    def __init__(self, args, workdir: Path):
        self.args = args
        self.workdir = workdir  # CLAUDE.md を読ませないため brain 外の作業ディレクトリで実行する

    def claude(self, system: str, prompt: str, model: str) -> str:
        cmd = [
            "claude", "-p", "--model", model, "--tools", "", "--setting-sources", "",
            "--no-session-persistence", "--system-prompt", system,
        ]
        return self._run(cmd, prompt)

    def codex(self, system: str, prompt: str) -> str:
        if self.args.mock_codex:
            return self.claude(system, prompt, self.args.mock_model)
        out = self.workdir / "codex-last.md"
        if out.exists():
            out.unlink()
        cmd = [
            "codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only",
            "-C", str(self.workdir), "--output-last-message", str(out),
            "-c", f'model_reasoning_effort="{self.args.codex_effort}"',
        ]
        if self.args.codex_model:
            cmd += ["-m", self.args.codex_model]
        full = f"{system}\n\n---\n\n{prompt}"
        stdout = self._run(cmd, full)
        if out.exists():
            return out.read_text(encoding="utf-8").strip()
        return stdout

    def _run(self, cmd, stdin_text: str) -> str:
        res = subprocess.run(
            cmd, input=stdin_text, text=True, capture_output=True, cwd=str(self.workdir),
        )
        if res.returncode != 0:
            sys.stderr.write(res.stderr)
            sys.exit(f"コマンド失敗: {' '.join(cmd[:2])}")
        return res.stdout.strip()


def build_prompt(question: str, refs_text: str, transcript: str, task: str) -> str:
    return (
        f"## 論点\n\n{question}\n\n"
        f"## 前提ファイル\n\n{refs_text}\n"
        f"## これまでの議事\n\n{transcript or '（まだ無し）'}\n\n"
        f"## あなたの仕事\n\n{task}"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", help="論点の文字列。@path.md でファイル指定")
    ap.add_argument("--refs", nargs="*", default=DEFAULT_REFS, help="前提として渡す brain のファイル")
    ap.add_argument("--rounds", type=int, default=5)
    ap.add_argument("--claude-model", default="fable")
    ap.add_argument("--codex-model", default=None, help="未指定なら Codex CLI の既定モデル")
    ap.add_argument("--codex-effort", default="high", help="Codex の model_reasoning_effort")
    ap.add_argument("--mock-codex", action="store_true", help="Codex 役を Claude で代替（動作確認用）")
    ap.add_argument("--mock-model", default="opus")
    ap.add_argument("--out", default="debates", help="出力先（brain からの相対）")
    args = ap.parse_args()

    if not shutil.which("claude"):
        sys.exit("claude CLI が見つかりません")
    if not args.mock_codex and not shutil.which("codex"):
        sys.exit("codex CLI が見つかりません。brew install codex && codex login。動作確認だけなら --mock-codex")

    question = args.question
    if question.startswith("@"):
        question = Path(question[1:]).read_text(encoding="utf-8").strip()

    refs_text = read_refs(args.refs)
    today = dt.date.today().isoformat()
    out_dir = ROOT / args.out / f"{today}-{slugify(question)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = out_dir / "transcript.md"
    final_path = out_dir / "final.md"

    transcript = f"# 論点\n\n{question}\n\n参照: {', '.join(args.refs)}\n"
    transcript_path.write_text(transcript, encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        runner = Runner(args, Path(tmp))
        codex_label = "Codex(mock=Claude " + args.mock_model + ")" if args.mock_codex else "Codex"

        def call(side: str, system: str, prompt: str) -> str:
            if side == "claude":
                return runner.claude(system, prompt, args.claude_model)
            return runner.codex(system, prompt)

        stopped = False
        for r in range(1, args.rounds + 1):
            proposer, critic = ("claude", "codex") if r % 2 == 1 else ("codex", "claude")
            names = {"claude": f"Claude({args.claude_model})", "codex": codex_label}

            print(f"[round {r}] 提案: {names[proposer]}", file=sys.stderr)
            proposal = call(proposer, f"{COMMON_SYSTEM}\n\n{PROPOSER_TASK}",
                            build_prompt(question, refs_text, transcript, PROPOSER_TASK))
            transcript += f"\n## Round {r} 提案（{names[proposer]}）\n\n{proposal}\n"
            transcript_path.write_text(transcript, encoding="utf-8")

            print(f"[round {r}] 反論: {names[critic]}", file=sys.stderr)
            objection = call(critic, f"{COMMON_SYSTEM}\n\n{CRITIC_TASK}",
                             build_prompt(question, refs_text, transcript, CRITIC_TASK))
            transcript += f"\n## Round {r} 反論（{names[critic]}）\n\n{objection}\n"
            transcript_path.write_text(transcript, encoding="utf-8")

            if NO_OBJECTION in objection and len(objection) < len(NO_OBJECTION) + 20:
                print(f"[round {r}] 新しい反論なし。終了", file=sys.stderr)
                stopped = True
                break

        print("[final] 最終回答: Claude", file=sys.stderr)
        final = runner.claude(f"{COMMON_SYSTEM}\n\n{FINAL_TASK}",
                              build_prompt(question, refs_text, transcript, FINAL_TASK), args.claude_model)

    header = (
        f"# {question}\n\n"
        f"日付: {today} / ラウンド: {r}{'（反論なしで終了）' if stopped else ''} / "
        f"Claude: {args.claude_model} / Codex: {args.codex_model or ('mock:' + args.mock_model if args.mock_codex else 'default')} / "
        f"参照: {', '.join(args.refs)}\n\n---\n\n"
    )
    final_path.write_text(header + final + "\n", encoding="utf-8")
    print(final)
    print(f"\n---\n最終回答: {final_path.relative_to(ROOT)}\n議事: {transcript_path.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
