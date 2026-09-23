# tools/debate

Claude と Codex の最上位モデルを交互に呼び、1つの論点を往復させて最終回答を出す。
出力の型は CLAUDE.md の「回答の型」と同じ（結論→根拠、10行以内）。論点表は出さない。

## 準備

- Claude Code CLI（`claude`）がログイン済みであること
- Codex CLI: `brew install codex && codex login`

## 使い方

```
tools/debate/debate.py "Respo を軸に AR で会計まで完結させる方針の穴は"
tools/debate/debate.py @question.md --refs hello/hello-dining.md decisions.md hr.md --rounds 3
tools/debate/debate.py "論点" --mock-codex    # Codex 未導入時の動作確認。Codex 役を Claude(Opus) が代替
```

- ラウンドごとに提案側と反論側を入れ替える（奇数: Claude 提案 / Codex 反論）
- 反論側が「新しい反論なし」と返したら規定ラウンド前でも終了
- 最終回答は Claude が書く

## 出力

- `debates/<日付>-<論点>/final.md`: 最終回答。commit する
- `debates/<日付>-<論点>/transcript.md`: 往復ログ。gitignore 済み
- 決めたことは final.md からではなく、通常どおり decisions.md と会社ファイルに書く
