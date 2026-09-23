# tools/think

Claude と Codex の最上位モデルで1つの論点を考え、最終回答を CLAUDE.md の「回答の型」で出す（結論→根拠、10行以内）。論点表は出さない。

流れ
1. 発散: 両モデルが互いを見ずに独立で3案ずつ出す。幅を作る工程
2. 攻撃: 相手の案ごとに致命的な穴1つと「結論を変えうる事実」を出す
3. 討論: 提案側と反論側を交代しながら往復（既定2ラウンド）
4. 統合: Claude が回答の型で答える。末尾に「残る反論」「要確認（結論を変えうる事実と取り方）」

## 準備

- Claude Code CLI（`claude`）がログイン済みであること
- Codex CLI: `brew install codex && codex login`

## 使い方

```
tools/think/think.py "Respo を軸に AR で会計まで完結させる方針の穴は" --refs hello/hello-dining.md decisions.md
tools/think/think.py @question.md --refs hello/hello-dining.md decisions.md hr.md --rounds 3
```

- `--refs` は必須。前提にするファイルを毎回明示する
- claude と codex の両 CLI が無いとエラーで止まる。代替はしない
- 討論はラウンドごとに提案側と反論側を入れ替える（奇数: Claude 提案 / Codex 反論）
- 反論側が「新しい反論なし」と返したら規定ラウンド前でも終了
- 最終回答は Claude が書く。発散の案は素材で、採否は播口さんが決める
- モデルの既定は Claude=fable、Codex=gpt-6-astra（reasoning effort xhigh）。`--claude-model` `--codex-model` `--codex-effort` で変更

## 出力

- `thoughts/<日付>-<論点>/final.md`: 最終回答。commit する
- `thoughts/<日付>-<論点>/transcript.md`: 往復ログ。gitignore 済み
- 決めたことは final.md からではなく、通常どおり decisions.md と会社ファイルに書く
