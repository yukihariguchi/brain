#!/usr/bin/env python3
"""Claude と Codex の最上位モデルで1つの論点を考え、最終回答を回答の型で出す。

流れ: 発散 → 攻撃 → 討論 → 統合
  1. 発散: 両モデルが互いを見ずに独立で3案ずつ出す（幅を作る）
  2. 攻撃: 相手の案ごとに致命的な穴1つと「結論を変えうる事実」を出す
  3. 討論: 提案側と反論側を交代しながら往復（既定2ラウンド）
  4. 統合: Claude が回答の型で答える。末尾に「残る反論」と「要確認」

使い方:
  tools/think/think.py "論点" --refs hello/hello-dining.md decisions.md
  tools/think/think.py @question.md --refs a.md b.md --rounds 3

出力: thoughts/<日付>-<slug>/ に transcript.md（gitignore）と final.md（commit 対象）
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
- 議事に発散の案と攻撃があれば、そこから選ぶか組み合わせる。新案を出すなら既存案を捨てる理由を1行で言う。
- 反論のうち受け入れるものは取り込んで答えを修正する。受け入れないものは1行で理由を言う。
- 結論を曖昧にしない。条件付きなら条件を明記する。"""

CRITIC_TASK = f"""あなたの役割は「反論側」。
直前の提案を崩す。目的は勝つことではなく、経営者が見落とす前提・因果の飛び・事実の誤りを出すこと。
- 出すのは議事にまだ出ていない反論だけ。最大3つ。1反論=結論1行+根拠1〜2行。
- 反論のたびに「提案のどの一文に対する反論か」を明示する。
- 事実の誤りは前提ファイルの該当箇所を引いて示す。
- 新しい反論が本当に無いなら、本文を「{NO_OBJECTION}」の1行だけにする。無理に出さない。"""

DIVERGE_TASK = """あなたの役割は「発散」。この論点に対して、互いに前提の異なる案を3つ出す。
- 他のモデルの案は見ていない。自分の考えだけで出す。無難な案を並べない。1つは経営者が自分では出しにくい角度にする
- 各案の型: 「案N: 1行の結論」→「前提: この案が成り立つ条件1行」→「崩れる条件: 何が事実だとこの案は捨てるべきか1行」
- 3案で9行。前置きと後書きは書かない"""

ATTACK_TASK = """あなたの役割は「攻撃」。相手モデルの3案を読み、案ごとに次を書く。
- 致命的な穴: 最大1つ。前提ファイルの事実と食い違うなら該当箇所を引く。無ければ「なし」
- 結論を変えうる事実: この案を採る/捨てるを決める事実を1〜2個。「何の数字か・どこで取れるか（推測なら明示）」まで書く
- 3案で最大12行。自分の案を弁護しない"""

FINAL_TASK = """あなたの役割は「最終回答」。議事全体（発散・攻撃・討論）を読み、論点への答えを経営者に返す。
出力の型（厳守）:
- 1行目は結論。空行で区切る
- 根拠は箇条書き。1項目=1理由=1行。因果のステップは削らない
- 結論と根拠で10行以内
- 続けて「残る反論:」として、決着しなかった反論を最大2行。無ければ書かない
- 続けて「要確認:」として、結論を変えうる事実を最大3行。「何の数字か・どこで取れるか」を書く
- 一文一義。1文40〜50字まで。略語は初出時に展開。造語・比喩を使わない
- 論点表・議事の要約・双方の主張の列挙はしない。答えだけ書く"""


def slugify(text: str, limit: int = 40) -> str:
    s = re.sub(r"\s+", "-", text.strip())
    s = re.sub(r"[^\w\-ぁ-んァ-ン一-龥]", "", s)
    return s[:limit] or "think"


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
    ap.add_argument("--refs", nargs="+", required=True, help="前提として渡す brain のファイル（必須）")
    ap.add_argument("--rounds", type=int, default=2, help="討論のラウンド数")
    ap.add_argument("--claude-model", default="fable")
    ap.add_argument("--codex-model", default=None, help="未指定なら Codex CLI の既定モデル")
    ap.add_argument("--codex-effort", default="high", help="Codex の model_reasoning_effort")
    ap.add_argument("--out", default="thoughts", help="出力先（brain からの相対）")
    args = ap.parse_args()

    missing = [c for c in ("claude", "codex") if not shutil.which(c)]
    if missing:
        sys.exit(f"CLI が見つかりません: {', '.join(missing)}。codex は brew install codex && codex login")

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
        codex_label = f"Codex({args.codex_model or 'default'})"

        def call(side: str, system: str, prompt: str) -> str:
            if side == "claude":
                return runner.claude(system, prompt, args.claude_model)
            return runner.codex(system, prompt)

        names = {"claude": f"Claude({args.claude_model})", "codex": codex_label}

        ideas = {}
        for side in ("claude", "codex"):
            print(f"[発散] {names[side]}", file=sys.stderr)
            ideas[side] = call(side, f"{COMMON_SYSTEM}\n\n{DIVERGE_TASK}",
                               build_prompt(question, refs_text, "", DIVERGE_TASK))
        for side in ("claude", "codex"):
            transcript += f"\n## 発散（{names[side]}）\n\n{ideas[side]}\n"
        transcript_path.write_text(transcript, encoding="utf-8")

        for attacker, target in (("claude", "codex"), ("codex", "claude")):
            print(f"[攻撃] {names[attacker]} → {names[target]} の案", file=sys.stderr)
            task = f"{ATTACK_TASK}\n\n### 相手（{names[target]}）の3案\n\n{ideas[target]}"
            attack = call(attacker, f"{COMMON_SYSTEM}\n\n{ATTACK_TASK}",
                          build_prompt(question, refs_text, transcript, task))
            transcript += f"\n## 攻撃（{names[attacker]} → {names[target]} の案）\n\n{attack}\n"
            transcript_path.write_text(transcript, encoding="utf-8")

        stopped = False
        r = 0
        for r in range(1, args.rounds + 1):
            proposer, critic = ("claude", "codex") if r % 2 == 1 else ("codex", "claude")

            print(f"[討論 {r}] 提案: {names[proposer]}", file=sys.stderr)
            proposal = call(proposer, f"{COMMON_SYSTEM}\n\n{PROPOSER_TASK}",
                            build_prompt(question, refs_text, transcript, PROPOSER_TASK))
            transcript += f"\n## 討論 Round {r} 提案（{names[proposer]}）\n\n{proposal}\n"
            transcript_path.write_text(transcript, encoding="utf-8")

            print(f"[討論 {r}] 反論: {names[critic]}", file=sys.stderr)
            objection = call(critic, f"{COMMON_SYSTEM}\n\n{CRITIC_TASK}",
                             build_prompt(question, refs_text, transcript, CRITIC_TASK))
            transcript += f"\n## 討論 Round {r} 反論（{names[critic]}）\n\n{objection}\n"
            transcript_path.write_text(transcript, encoding="utf-8")

            if NO_OBJECTION in objection and len(objection) < len(NO_OBJECTION) + 20:
                print(f"[討論 {r}] 新しい反論なし。終了", file=sys.stderr)
                stopped = True
                break

        print("[final] 最終回答: Claude", file=sys.stderr)
        final = runner.claude(f"{COMMON_SYSTEM}\n\n{FINAL_TASK}",
                              build_prompt(question, refs_text, transcript, FINAL_TASK), args.claude_model)

    header = (
        f"# {question}\n\n"
        f"日付: {today} / 討論ラウンド: {r}{'（反論なしで終了）' if stopped else ''} / "
        f"Claude: {args.claude_model} / Codex: {args.codex_model or 'default'} / "
        f"参照: {', '.join(args.refs)}\n\n---\n\n"
    )
    final_path.write_text(header + final + "\n", encoding="utf-8")
    print(final)
    print(f"\n---\n最終回答: {final_path.relative_to(ROOT)}\n議事: {transcript_path.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
