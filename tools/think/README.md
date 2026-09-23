# tools/think

Claude と Codex の最上位モデルで1つの論点を考え、最終回答を CLAUDE.md の「回答の型」で出す（結論→根拠、10行以内）。論点表は出さない。

流れ（調査 → 発散 → 攻撃 → 討論 → 統合 → 校閲 → 修正）
1. 調査: 両モデルが Web 検索で外部の事実を集める（数字・出典つき）。新しい案の材料
2. 発散: 両モデルが互いを見ず、播口さんの仮説も見ずに5案ずつ出す。2案以上は現方針と食い違う案
3. 攻撃: 相手の案ごとに「事実で示せる穴」と「推測の穴」を分ける。推測だけで案を落とさない
4. 討論: ここで初めて仮説と議論の経過を見せ、提案側と反論側を交代しながら往復（既定3ラウンド）
5. 統合: Claude が回答の型で答える。仮説より強い案が無ければ「無い」と明言し、推測だけで落ちた案を別枠で残す
6. 校閲: Codex が統合案を検査（議事に無い主張、仮説の言い直し、落とした案の扱い、型）
7. 修正: Claude が校閲を反映して最終回答にする

所要は30分前後。時間より質を優先する設計。

## 準備

- Claude Code CLI（`claude`）がログイン済みであること
- Codex CLI: `brew install codex && codex login`

## 使い方

入力は question.md。会話を持っている Claude Code のセッションが書く。播口さんが「今の議論を think に投げて」と言えば、Claude が `thoughts/<日付>-<論点>/question.md` を作って実行し、final.md を会話に返す。

```
# 論点              ← 1行
## 背景（事実）      ← 調査・発散・攻撃にも渡す。事実だけ。brain に無いものはここに全部書く
## 議論の経過        ← 討論から渡す。会話で出た推論・却下した案・前回の think の結論と評価
## 現在の仮説        ← 討論から渡す。播口さんの今の答えと、問いたいこと
```

見出しに「経過」「仮説」「推論」を含む節は討論まで隠す。発散が仮説に引きずられるのを防ぐため。

```
tools/think/think.py thoughts/2026-09-23-xxx/question.md --refs hello/hello-dining.md decisions.md
tools/think/think.py "1行の論点" --refs a.md b.md    # 背景なしの簡易実行
```

- `--refs` は必須。前提にするファイルを毎回明示する
- 背景を渡さないと、モデルは前提ファイルの言い直しに寄る。仮説を発散に見せると仮説の修正版に収束する（2026-09-23 に確認）
- `--no-research` で調査を飛ばせる。`--rounds` で討論の回数
- claude と codex の両 CLI が無いとエラーで止まる。代替はしない
- 討論はラウンドごとに提案側と反論側を入れ替える（奇数: Claude 提案 / Codex 反論）
- 反論側が「新しい反論なし」と返したら規定ラウンド前でも終了
- 最終回答は Claude が書く。発散の案は素材で、採否は播口さんが決める
- モデルの既定は Claude=fable（effort xhigh）、Codex=gpt-6-astra（reasoning effort xhigh）。`--claude-model` `--claude-effort` `--codex-model` `--codex-effort` で変更

## 出力

- `thoughts/<日付>-<論点>/question.md`: 入力。commit する
- `thoughts/<日付>-<論点>/final.md`: 最終回答。commit する
- `thoughts/<日付>-<論点>/transcript.md`: 往復ログ。gitignore 済み
- 反映が終わったディレクトリは消す。中身は decisions.md と会社ファイルに移す
- 決めたことは final.md からではなく、通常どおり decisions.md と会社ファイルに書く
