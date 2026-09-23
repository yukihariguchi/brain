#!/usr/bin/env python3
"""Claude と Codex の最上位モデルで1つの論点を考え、最終回答を回答の型で出す。

流れ: 調査 → 発散 → 攻撃 → 討論 → 統合 → 校閲 → 修正
  1. 調査: 両モデルが Web 検索で外部の事実を集める（数字・出典つき）。新しい案の材料
  2. 発散: 両モデルが互いを見ず、播口さんの仮説も見ずに5案ずつ出す（幅を作る）
  3. 攻撃: 相手の案ごとに「事実で示せる穴」と「推測の穴」を分けて出す。推測だけで案を落とさない
  4. 討論: ここで初めて仮説と議論の経過を見せ、提案側と反論側を交代しながら往復（既定3ラウンド）
  5. 統合: Claude が回答の型で答える。仮説より強い案が無ければ「無い」と明言する
  6. 校閲: Codex が統合案を検査する（議事に無い主張、仮説の言い直し、推測だけで落とした案の扱い）
  7. 修正: Claude が校閲を反映して最終回答にする

入力: question.md。会話を持っている Claude Code のセッションが書く。
  # 論点            ← 1行。出力ディレクトリ名にも使う
  ## 背景（事実）    ← 調査・発散・攻撃にも渡す。事実だけ
  ## 議論の経過      ← 討論から渡す。会話で出た推論・却下した案
  ## 現在の仮説      ← 討論から渡す。播口さんの今の答え
  見出しに「経過」「仮説」「推論」を含む節は討論まで隠す。節が無ければ全文をどの工程にも渡す

使い方:
  tools/think/think.py thoughts/2026-09-23-xxx/question.md --refs hello/hello-dining.md decisions.md
  tools/think/think.py "1行の論点" --refs a.md b.md        # 背景なしの簡易実行

出力: thoughts/<日付>-<slug>/ に transcript.md（gitignore）と final.md（commit 対象）
"""
import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NO_OBJECTION = "新しい反論なし"
HIDDEN_WORDS = ("経過", "仮説", "推論")

COMMON_SYSTEM = """あなたは経営者の壁打ち相手。相手は複数社を横断して見る経営者で、事業企画から開発まで自分で見る。技術も事業も噛み砕かなくていい。
ルール:
- 日本語。1行目は結論。根拠は箇条書きで1項目1理由。
- 事実は前提ファイル・背景・事実メモから引く。そこに無いことは「推測」と明示する。
- 造語・比喩・抽象語を避ける。数字で語れるものは数字で語る。
- 既出の論点を繰り返さない。議事に書いてあることを言い直さない。
- 前置き・後書き・言い換えは書かない。"""

RESEARCH_TASK = """あなたの役割は「調査」。Web 検索を使い、この論点を考えるのに要る外部の事実を集める。
- 集めるもの: 似た構造で成功・失敗した事業の稼ぎ方と数字（手数料率・売上構成・店数）/ 日本と主要国の競合の料金と規模 / 関係する規制と免許 / プラットフォーム（OS・エージェント・Google 等）の規約と手数料 / 市場の数字
- 1件の型: 「事実（数字を含める）」→「出典 URL」→「この論点で何に効くか1行」
- 10〜20件。前提ファイルに既に書いてあることは集めない。確認できなかったものは「未確認」と書き、それらしい数字を作らない
- 見出しは「## 事実メモ」。前置きは書かない"""

DIVERGE_TASK = """あなたの役割は「発散」。この論点に対して、互いに前提の異なる案を5つ出す。
- 他のモデルの案も、経営者の現在の考えも見ていない。自分の考えだけで出す。無難な案を並べない
- 5案のうち2つ以上は、前提ファイルに書かれている現方針の方向と食い違う案にする。現方針の維持や言い直しは数えない
- 各案の型: 「案N: 1行の結論」→「仕組み: 誰が何をして金がどう動くか、3〜5行」→「根拠: 前提ファイル・背景・事実メモから引く。数字があれば数字で」→「試算: 仮置きの数字で年間の売上か粗利の桁を出す。仮置きと明示」→「崩れる条件: 何が事実ならこの案は捨てるか1行」
- 行数の上限は無い"""

ATTACK_TASK = """あなたの役割は「攻撃」。相手モデルの案を1つずつ検査する。目的は落とすことではなく、事実と推測を分けること。
案ごとに書く:
- 事実で示せる穴: 前提ファイル・背景・事実メモの該当箇所を引いて示す。無ければ「なし」
- 推測の穴: 事実で示せないが疑わしい点。「推測」と明示する
- 結論を変えうる事実: この案を採る/捨てるを決める事実を1〜2個。「何の数字か・どこで取れるか」まで書く
- 判定: 「事実で落ちる」「推測で保留」「生き残り」のどれか。推測だけでは落とさない
自分の案を弁護しない"""

PROPOSER_TASK = """あなたの役割は「提案側」。
ここから経営者の「議論の経過」と「現在の仮説」を見られる。生き残りと保留の案、経営者の仮説を比べ、論点に対する現時点で最も強い答えを出す。
- 仮説より強い案があるならそれを推す。理由は事実メモか前提ファイルの事実で言う
- 仮説の方が強いなら「仮説より強い案は無い」と明言し、仮説を具体化して一段強くする
- これまでの議事にある反論を全部踏まえる。受け入れるものは取り込み、受け入れないものは1行で理由を言う
- 結論を曖昧にしない。条件付きなら条件を明記する。全体20行以内"""

CRITIC_TASK = f"""あなたの役割は「反論側」。
直前の提案を崩す。目的は勝つことではなく、経営者が見落とす前提・因果の飛び・事実の誤りを出すこと。
- 出すのは議事にまだ出ていない反論だけ。最大3つ。1反論=結論1行+根拠1〜2行
- 反論のたびに「提案のどの一文に対する反論か」を明示する
- 根拠は事実メモ・前提ファイル・背景から引く。引けないものは「推測」と明示する
- 新しい反論が本当に無いなら、本文を「{NO_OBJECTION}」の1行だけにする。無理に出さない"""

FINAL_TASK = """あなたの役割は「統合」。議事全体（事実メモ・発散・攻撃・討論）を読み、論点への答えを経営者に返す。
出力の型（厳守）:
- 1行目は結論。「現在の仮説」に対して、同意 / 修正 / 別案 のどれかを明示する。仮説より強い案が無いなら「仮説より強い案は無い」と書く。空行で区切る
- 根拠は箇条書き。1項目=1理由=1行。因果のステップは削らない。結論と根拠で10行以内
- 続けて「仮説より強い可能性がある案:」として、攻撃・討論で推測だけを理由に落ちた案を最大3つ。各1行、「何が事実なら採るか」を添える。無ければ書かない
- 続けて「残る反論:」として、決着しなかった反論を最大2行。無ければ書かない
- 続けて「要確認:」として、結論を変えうる事実を最大3行。「何の数字か・どこで取れるか」を書く
- 続けて「出典:」として、結論と根拠に使った事実メモの URL だけを列挙する
- 一文一義。1文40〜50字まで。略語は初出時に展開。造語・比喩を使わない
- 論点表・議事の要約・双方の主張の列挙はしない。前提ファイルの方針の言い直しは答えではない"""

REVIEW_TASK = """あなたの役割は「校閲」。統合案を検査し、直すべき点だけを列挙する。
検査項目:
1. 議事（事実メモ・前提ファイル・背景・発散・攻撃・討論）に根拠が無い主張。該当する一文を引く
2. 結論が「現在の仮説」や前提ファイルの方針の言い直しになっていないか。なっていれば、議事の中でそれより強い候補がどれかを言う
3. 攻撃・討論で推測だけを理由に落ちた案が「仮説より強い可能性がある案」に載っているか。漏れがあれば案名を挙げる
4. 「要確認」が「何の数字か・どこで取れるか」まで書けているか
5. 型の違反（1行目に同意/修正/別案の明示が無い、結論と根拠で10行超、1文が長い、比喩や造語）
- 指摘だけを箇条書きで。1指摘=1行+根拠1行。問題が無い項目は書かない。全部問題が無ければ「指摘なし」の1行"""

REVISE_TASK = """あなたの役割は「修正」。直前の統合案に校閲の指摘を反映し、最終回答を書く。
- 指摘のうち議事の事実に照らして正しいものは直す。正しくないものは無視してよいが、最終回答には書かない
- 出力は統合の型（1行目に同意/修正/別案、根拠、仮説より強い可能性がある案、残る反論、要確認、出典）そのまま
- 最終回答だけを書く。変更点の説明は書かない"""


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


def split_question(text: str):
    """question.md を (title, open_text, hidden_text) に分ける。
    見出しに 経過/仮説/推論 を含む ## 節は hidden。節が無ければ全文 open。"""
    lines = text.strip().splitlines()
    first = next((l for l in lines if l.strip()), text)
    title = re.sub(r"^#+\s*", "", first).strip()
    if not any(l.startswith("## ") for l in lines):
        return title, text.strip(), ""
    open_parts, hidden_parts = [], []
    cur, hidden = [], False
    for l in lines:
        if l.startswith("## "):
            (hidden_parts if hidden else open_parts).append("\n".join(cur))
            cur, hidden = [l], any(w in l for w in HIDDEN_WORDS)
        else:
            cur.append(l)
    (hidden_parts if hidden else open_parts).append("\n".join(cur))
    return title, "\n".join(p for p in open_parts if p.strip()).strip(), "\n".join(p for p in hidden_parts if p.strip()).strip()


class Runner:
    def __init__(self, args, workdir: Path):
        self.args = args
        self.workdir = workdir  # CLAUDE.md を読ませないため brain 外で実行する

    def claude(self, system: str, prompt: str, search: bool = False) -> str:
        cmd = ["claude", "-p", "--model", self.args.claude_model, "--effort", self.args.claude_effort,
               "--setting-sources", "", "--no-session-persistence", "--system-prompt", system]
        if search:
            cmd += ["--tools", "WebSearch,WebFetch", "--allowedTools", "WebSearch", "WebFetch",
                    "--permission-mode", "dontAsk"]
        else:
            cmd += ["--tools", ""]
        return self._run(cmd, prompt)

    def codex(self, system: str, prompt: str, search: bool = False) -> str:
        out = self.workdir / f"codex-{abs(hash(prompt))}.md"
        cmd = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "read-only", "-C", str(self.workdir),
               "--output-last-message", str(out), "-m", self.args.codex_model,
               "-c", f'model_reasoning_effort="{self.args.codex_effort}"']
        if search:
            cmd += ["--search"]
        stdout = self._run(cmd, f"{system}\n\n---\n\n{prompt}")
        return out.read_text(encoding="utf-8").strip() if out.exists() else stdout

    def call(self, side: str, system: str, prompt: str, search: bool = False) -> str:
        return (self.claude if side == "claude" else self.codex)(system, prompt, search)

    def _run(self, cmd, stdin_text: str) -> str:
        res = subprocess.run(cmd, input=stdin_text, text=True, capture_output=True, cwd=str(self.workdir))
        if res.returncode != 0:
            sys.stderr.write(res.stderr)
            sys.exit(f"コマンド失敗: {' '.join(cmd[:2])}")
        return res.stdout.strip()


def build_prompt(question: str, refs_text: str, transcript: str, task: str) -> str:
    return (f"## 論点と背景\n\n{question}\n\n"
            f"## 前提ファイル\n\n{refs_text}\n"
            f"## これまでの議事\n\n{transcript or '（まだ無し）'}\n\n"
            f"## あなたの仕事\n\n{task}")


def log(msg):
    print(f"[{dt.datetime.now():%H:%M:%S}] {msg}", file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", help="question.md のパス、または1行の論点")
    ap.add_argument("--refs", nargs="+", required=True, help="前提として渡す brain のファイル（必須）")
    ap.add_argument("--rounds", type=int, default=3, help="討論のラウンド数")
    ap.add_argument("--claude-model", default="fable")
    ap.add_argument("--claude-effort", default="max", help="Claude の effort（low/medium/high/xhigh/max）")
    ap.add_argument("--codex-model", default="gpt-6-astra")
    ap.add_argument("--codex-effort", default="xhigh", help="Codex の model_reasoning_effort")
    ap.add_argument("--no-research", action="store_true", help="調査（Web 検索）を飛ばす")
    ap.add_argument("--out", default="thoughts", help="出力先（brain からの相対）")
    args = ap.parse_args()

    missing = [c for c in ("claude", "codex") if not shutil.which(c)]
    if missing:
        sys.exit(f"CLI が見つかりません: {', '.join(missing)}。codex は brew install codex && codex login")

    question_file = None
    raw = args.question
    if raw.startswith("@") or raw.endswith(".md"):
        question_file = Path(raw.lstrip("@"))
        if not question_file.is_absolute():
            question_file = ROOT / question_file
        raw = question_file.read_text(encoding="utf-8")
    title, open_q, hidden_q = split_question(raw)
    full_q = f"{open_q}\n\n{hidden_q}".strip() if hidden_q else open_q

    refs_text = read_refs(args.refs)
    today = dt.date.today().isoformat()
    if question_file and question_file.parent.parent == ROOT / args.out:
        out_dir = question_file.parent
    else:
        out_dir = ROOT / args.out / f"{today}-{slugify(title)}"
    out_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = out_dir / "transcript.md"
    final_path = out_dir / "final.md"

    transcript = f"{full_q}\n\n参照: {', '.join(args.refs)}\n"
    if not full_q.startswith("#"):
        transcript = f"# 論点\n\n{transcript}"

    def save():
        transcript_path.write_text(transcript, encoding="utf-8")

    save()

    with tempfile.TemporaryDirectory() as tmp:
        run = Runner(args, Path(tmp))
        names = {"claude": f"Claude({args.claude_model})", "codex": f"Codex({args.codex_model})"}
        sides = ("claude", "codex")

        def both(fn):
            with ThreadPoolExecutor(max_workers=2) as ex:
                return dict(zip(sides, ex.map(fn, sides)))

        # 1. 調査（仮説は見せない）
        if not args.no_research:
            log("調査: 両モデルが Web 検索")
            notes = both(lambda s: run.call(s, f"{COMMON_SYSTEM}\n\n{RESEARCH_TASK}",
                                            build_prompt(open_q, refs_text, "", RESEARCH_TASK), search=True))
            for s in sides:
                transcript += f"\n## 事実メモ（{names[s]}）\n\n{notes[s]}\n"
            save()

        # 2. 発散（仮説は見せない。相手の案も見せない。事実メモは両方見せる）
        log("発散: 両モデルが独立に5案")
        ideas = both(lambda s: run.call(s, f"{COMMON_SYSTEM}\n\n{DIVERGE_TASK}",
                                        build_prompt(open_q, refs_text, transcript, DIVERGE_TASK)))
        for s in sides:
            transcript += f"\n## 発散（{names[s]}）\n\n{ideas[s]}\n"
        save()

        # 3. 攻撃（交差。仮説はまだ見せない）
        log("攻撃: 相手の案を検査")
        other = {"claude": "codex", "codex": "claude"}
        attacks = both(lambda s: run.call(
            s, f"{COMMON_SYSTEM}\n\n{ATTACK_TASK}",
            build_prompt(open_q, refs_text, transcript,
                         f"{ATTACK_TASK}\n\n### 検査する案（{names[other[s]]}）\n\n{ideas[other[s]]}")))
        for s in sides:
            transcript += f"\n## 攻撃（{names[s]} → {names[other[s]]} の案）\n\n{attacks[s]}\n"
        save()

        # 4. 討論（ここから仮説と経過を見せる）
        if hidden_q:
            transcript += f"\n## ここから開示: 議論の経過と現在の仮説\n\n{hidden_q}\n"
            save()
        stopped, r = False, 0
        for r in range(1, args.rounds + 1):
            proposer, critic = ("claude", "codex") if r % 2 == 1 else ("codex", "claude")
            log(f"討論 {r}: 提案 {names[proposer]}")
            proposal = run.call(proposer, f"{COMMON_SYSTEM}\n\n{PROPOSER_TASK}",
                                build_prompt(full_q, refs_text, transcript, PROPOSER_TASK))
            transcript += f"\n## 討論 Round {r} 提案（{names[proposer]}）\n\n{proposal}\n"
            save()
            log(f"討論 {r}: 反論 {names[critic]}")
            objection = run.call(critic, f"{COMMON_SYSTEM}\n\n{CRITIC_TASK}",
                                 build_prompt(full_q, refs_text, transcript, CRITIC_TASK))
            transcript += f"\n## 討論 Round {r} 反論（{names[critic]}）\n\n{objection}\n"
            save()
            if NO_OBJECTION in objection and len(objection) < len(NO_OBJECTION) + 20:
                log(f"討論 {r}: 新しい反論なし。終了")
                stopped = True
                break

        # 5. 統合 → 6. 校閲 → 7. 修正
        log("統合: Claude")
        draft = run.call("claude", f"{COMMON_SYSTEM}\n\n{FINAL_TASK}",
                         build_prompt(full_q, refs_text, transcript, FINAL_TASK))
        transcript += f"\n## 統合案（{names['claude']}）\n\n{draft}\n"
        save()
        log("校閲: Codex")
        review = run.call("codex", f"{COMMON_SYSTEM}\n\n{REVIEW_TASK}",
                          build_prompt(full_q, refs_text, transcript, f"{REVIEW_TASK}\n\n### 統合案\n\n{draft}"))
        transcript += f"\n## 校閲（{names['codex']}）\n\n{review}\n"
        save()
        log("修正: Claude")
        final = run.call("claude", f"{COMMON_SYSTEM}\n\n{REVISE_TASK}",
                         build_prompt(full_q, refs_text, transcript,
                                      f"{REVISE_TASK}\n\n### 統合案\n\n{draft}\n\n### 校閲の指摘\n\n{review}"))

    header = (f"# {title}\n\n"
              f"日付: {today} / 討論ラウンド: {r}{'（反論なしで終了）' if stopped else ''} / "
              f"Claude: {args.claude_model}({args.claude_effort}) / Codex: {args.codex_model}({args.codex_effort}) / "
              f"調査: {'なし' if args.no_research else 'あり'} / 参照: {', '.join(args.refs)}\n\n---\n\n")
    final_path.write_text(header + final + "\n", encoding="utf-8")
    print(final)
    log(f"最終回答: {final_path.relative_to(ROOT)}")
    log(f"議事: {transcript_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
