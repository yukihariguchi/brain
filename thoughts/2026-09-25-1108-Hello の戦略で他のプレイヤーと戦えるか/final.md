# Hello（パーソナルアシスタント）の戦略（hello/hello.md）で、Muse・Google・Apple・LINE と戦えるか。戦えないなら何を変えるべきか

日付: 2026-09-25 / 討論ラウンド: 3 / Claude: fable(xhigh) / Codex: gpt-6-astra(xhigh) / 調査: あり / 参照: hello/hello.md, hello/base.md, decisions.md

---

修正。仮説より強いと事実で示せた案は無い（10 案とも推測で保留）。差は「電話＋Hello 名義の番号」1 本に絞る。決済は日本の実購入 100 件を測るまで差に数えない。チャットは招待 URL→部屋→普通チャットの順に数値で通す。

- 戦える根拠: 日本では Google の自動着信応答・Call for Me・AI モード予約が未提供、Muse は日本未定、Agent i に電話が無い。日本で本人が実況を見て引き取れる発信を出している競合は確認できていない。
- 戦えない根拠: Call for Me が 09-24 に実況と本人引き取りを米国 Pixel 11 で出した。「本人が出る」は独自でない。残る差は Hello 名義番号への着信・日本語・非 Pixel の 3 つ。
- 「日本で一番最初」は電話と番号についても未証明。Genspark の日本向け電話の提供範囲が未確認。汎用の対話は国内 ChatGPT 月 931 万人、生成 AI 利用者 2,360 万人の後ろになる。
- 記憶は Gemini が他社から取り込めるので切替費用に数えない（推測。Hello の記録の移行範囲と所要時間は未測定）。
- 「決済」は保留。Muse は Stripe Link の使い捨てカードと購入保護を初日から持つが、日本のカード対応は未確認。Hello 側にも保存セッション＋Face ID の経路があり、Live View の手数が毎回乗るとは言えない。「店側に HelloPay がある保証つき予約電話」は店の合意と請求実績が出るまで差に数えない（未検証）。
- 「チャットで LINE を disrupt」は事実で崩れないが支える事実も無い。Apple Invites は登録不要で無料、Agent i in chat は年内。普通チャットは判定 3 の後に置く。
- 課金: 番号の無料配布は採算未確認（HelloX の番号原価・現預金・調達余力が未提示）。参考原価は Twilio 換算で番号 710 円/月・通話 200 円/件、Truecaller の有料転換は 0.75%。番号月額に月 3 件の無料通話を含めると、参考原価で 3 件使う人は 980 円でも月 330 円の赤字。番号は原価 × 1.3 以上（仮置き）の月額、通話は全件 1 件ごとに課金。番号を持たない層は共通番号（プール）から発信し 1 件ごとに払う。
- 判定 1（〜2026-12、値は仮置き）: 発信＋本人引き継ぎ。本人不在込みの完遂率 70% 以上、本人作業時間の中央値 50% 減。本人不在時の完遂率が 50% 未満なら運用部隊を開示つき有料の上位段で戻す。
- 判定 2（〜2027-03、値は仮置き）: 着信＋1 人 1 番号。番号保有者の 30% が 90 日内に店・宅配・病院から実着信。有料 100 人の 90 日内再依頼 40 人以上。主指標は番号保有者のうち月 1 件以上発信依頼がある率。実着信 30% 未満なら番号なしの件数課金代行に変える。
- 判定 3（〜2027-06、値は仮置き）: Respo 導入店 20 店で保証つき予約電話、5 店が 1 人 150 円を請求実績で入金。招待 URL のサインイン 25% 以上。予定終了後 30 日内に人が用事以外の会話を始めた部屋が 50% 以上で普通チャットに着手。本人確認は 2027-04 の JPKI 前提で NFC のみ作る。
- Google が日本語の Call for Me か自動着信応答を発表した時点で、番号無料化の可否を資金で決める。Muse が Instagram 国内 6,600 万 MAU から無料電話つきで来た時点の守りは、有料番号保有数 × 月 1 件依頼率。

仮説より強い可能性がある案:
- 運用部隊が開示つきで同じ通話を引き取り 1 件 500 円（Claude 案 2）: 本人不在時の完遂率が 50% 未満（仮置き）で、失敗・再架電・待機・通信・AI を含む 1 完遂あたり総原価が勤務記録と通話ログで 500 円未満なら採る。
- 訪日客向け 7 日パスを最初の市場に加える（Claude 案 3）: 日本語を話せない利用者の依頼を運用部隊なしで 70% 以上（仮置き）完遂し、1,980 円の購入者 1 人あたりで紹介料・全通話・返金・決済費用を引いた収支が販売記録と請求明細で正なら、国内向けと並走で採る。
- カード会社の会員特典として配る（Claude 案 4・Codex 案 5）: 対象会員 5 万人以上、最低売上の前払い、契約終了後の直接継続を確約する契約が 1 社取れれば配布経路として採る。
- 音声 eSIM の MVNO（Claude 案 1）: MVNE の見積書で着信・転送・音声モデル込みの 1 回線月額原価が 880 円未満、本人番号での発信と SMS の取り込みが提供条件で可なら、050 の代わりに採る。
- チャットなし・店負担で消費者無料（Claude 案 5）: 判定 3 の入金が 5 店を超え、番号保有者 1 人月あたりの有料予約粗利が番号維持費を上回れば、消費者無料への切替を判定に上げる。
- 30 日見積もり番号・一人事業者向け・法人購買・別居家族向け（Codex 案 1〜4）: 消費者向け PA を捨てるので現方針と並ばない。各案の崩れる条件（購入試験 300 人中 30 人、30 事業者中 15 社が 3 か月継続、10 社 500 件で作業時間 50% 減、100 件中本人対応 30 件以下）を通した案だけ HelloX の法人向け機能として別枠で検討する。

残る反論:
- 外部の獲得経路が招待 URL しか無い。サイドボタンは起動機能で配布ではない。獲得費 6 か月回収の判定は招待 URL 1 本の数字で置くしかない。
- 決済を差から落とすか残すかは、日本の実購入 100 件で保存カード入力・Live View・既存セッションを分けて完了率と本人操作時間を測るまで決まらない。
- 判定値（原価倍率 1.3・完遂率 70%・実着信 30%・再依頼 40 人・入金 5 店・雑談 50%）は全て仮置きで、実測から導いた基準が無い。

要確認:
- HelloX の番号 1 本の月額原価と通話 1 分の原価。HelloX の仕入契約と通話ログで取る。出た時点で番号月額を原価 × 1.3（仮置き）に置き直す。
- 番号無料化の必要資金、Hello JP の現預金、調達確約額。経理資料と調達契約で取る。Google の日本語発表時に無料化できる人数と期間をこれで決める。
- HelloPay の PCI DSS 審査範囲に保管カードの他社サイト入力が入るか、割賦販売法の取扱業者該当性。QSA の審査報告書と経産省への照会。不可なら EC は保存セッション＋Face ID のみ。
- Google の日本語 Call for Me か自動着信応答、Muse の日本公開と日本のカード対応の時期。Google Japan ブログと Meta Newsroom。
- Genspark の日本向け代理電話の提供範囲。Genspark ヘルプセンター。日本で提供済みなら「電話で一番最初」も消える。

出典:
- https://techcrunch.com/2026/09/24/google-tests-letting-gemini-make-phone-calls-initially-for-us-pixel-owners/
- https://9to5google.com/2026/09/24/pixel-11-call-for-me/
- https://support.google.com/pixelphone/answer/9118387?hl=ja
- https://www.seohacks.net/column/30555/
- https://www.nikkei.com/article/DGXZQOGN0901N0Z00C26A9000000/
- https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- https://blog.google/innovation-and-ai/products/gemini-app/switch-to-gemini-app/
- https://jpw.genspark.ai/helpcenter/call-for-me
- https://ictr.co.jp/report/%E3%80%90%E6%A5%AD%E7%95%8C%E3%83%88%E3%83%94%E3%83%83%E3%82%AF%E3%82%B9%E3%80%91%E7%94%9F%E6%88%90ai%E5%88%A9%E7%94%A8%E3%80%8Cchat-gpt%E3%80%8D%E3%81%8C%E5%9C%A7%E5%80%92%E7%9A%841%E4%BD%8D%E2%80%95.html/
- https://prtimes.jp/main/html/rd/p/000000027.000019182.html
- https://netshop.impress.co.jp/node/12342
- https://www.apple.com/newsroom/2025/02/introducing-apple-invites-a-new-app-that-brings-people-together/
- https://www.twilio.com/en-us/voice/pricing/jp
- https://developers.openai.com/api/docs/pricing
- https://mb.cision.com/Main/20429/4340107/4057915.pdf
- https://biz.trustdock.io/column/after202704-amlcft
- https://developer.apple.com/support/app-distribution-in-japan
- https://tenlifestylegroup.com/2025/11/12/full-year-trading-update-and-notice-of-results-2025/
- https://japanbuzz.info/social-media-in-japan/
