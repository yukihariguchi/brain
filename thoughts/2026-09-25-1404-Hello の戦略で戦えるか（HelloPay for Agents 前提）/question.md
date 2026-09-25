# Hello（パーソナルアシスタント）の戦略（hello/hello.md）は、決済が HelloPay for Agents（hello/hello-pay.md）で実現する前提で、Muse・Google・Apple・LINE・Genspark と戦えるか。戦えないなら何を変えるべきか

## 背景（事実）

2026-09-25 時点で播口と Claude が事実として共有しているもの。hello/hello.md・hello/base.md・decisions.md に無いものを含む。

### Hello 側の資産と制約

- HelloX: 音声 AI 電話＋クラウド PBX。中身の音声モデルは GPT の Realtime。AutoReserve は既に AI が店に電話して予約を取っている（本番稼働、日英仏伊西独）。AI が完遂できない電話を引き取る 200 人規模の運用部隊があるが、Hello ではこれを使わない（本人が引き継ぐ）と決めた
- HelloPay: 決済代行。PCI DSS を持つ（審査範囲に「保管カードをコードで他社サイトに入力する」が入るかは要確認）
- Hello JP は純資産マイナス。現預金・調達余力は未提示。PayPay 型の配布費（1 人約 2,500 円）は出せるか不明
- 正社員 50 名規模。Hello はまだアプリが無い。最初は社内テスター版（2〜3 週間）を目指す
- HelloX の PBX に会議通話（聞く・ささやく・割り込む）と通話中のテキスト指示の受け口があるかは要確認。番号在庫と 1 本の月額原価、電気通信事業の届出と番号使用計画の認定も要確認

### 製品の設計で決めたこと（hello.md より細かい部分）

- 画面は 3 種類だけ。メイン画面（本人とアシスタントの 1 本の会話。通話中はそのまま通話画面）/ 友人との部屋（相手ごと。人とそれぞれのアシスタント）/ 招待 URL の Web
- 通話は 1 本ずつ。3 軒に聞く時も順にかける。着信は裏で AI が受けて後で知らせる
- 部屋ではアシスタントは「皆に関わる用事の進み」だけを文で言う（カードは当面作らない）。アシスタント同士の詰め合いは部屋に流さず、結果を幹事側のアシスタントが 1 通で出し、過程は折りたたみ。相手の委任ルールの中身は見せない。本人への質問は部屋に出さず通知とメイン画面へ
- 自分のアシスタントへの指示は部屋の「Hello」ボタンから（メイン画面と同じ会話が部屋の文脈で開く）。相手には見えない。公開/非公開の切り替えは置かない
- 記憶は 1 つ、発言はその場所のもの。部屋で言った好みはメイン画面のアシスタントも知る。文面は同期しない
- 招待 URL は「答える＝1 タップサインイン＝Hello に入る」。登録なしで答える経路は最初は出さない。本人確認はリンクのトークン（電話番号は使わない）。リンクの検知はアカウントで行い deferred deep link は使わない
- 電話機能を使う時だけ本人確認（日本で番号付与に本人確認が要る）。チャットと招待は本人確認なし
- 決済: 本人のカードを Hello が保管、毎回は CVV と本人認証だけ。認証画面は Live View（Hello 側で動くブラウザの画面を本人の端末に映し、本人が打つ）。Live View は Browserbase の Session Live View や Cloudflare Browser Run に商用部品があり、自前でも Chrome DevTools Protocol の screencast と入力転送で作れる（試作 1 週間、本番 3〜6 週間の推定）。ユーザーが既にアカウントと保存カードを持つサイトでは本人のセッションで支払い、承認は Face ID
- Web 操作は AI が手順を作りコードが実行し、壊れたら AI が直す。AI に毎回操作させない
- 外部連携は MCP、許可は OAuth。Gmail の受信読み取りには Google の年次セキュリティ審査（CASA）が要る

### 競合の現況（2026-09、Web で確認）

- Meta Muse: 2026-09-08 米国公開、2 週で 250 万 DL、チャート 1 位。自社アプリと WhatsApp の中で動く。電話機能は 09-16 に米国内の店向けベータ。Reuters・404 Media（09-23）が、電話の一部を人間のコールセンター契約者が代行し事後まで知らされない例を報道。Muse の発見は Instagram・Facebook のグラフとリール。メインチャット 1 つ＋サブチャット複数の設計
- 競合 Instinct も同週に電話機能を早期アクセスで開始（米国限定）
- Google: Pixel の Call Screen（2018 年〜。着信を AI が受け、実況の文字起こしと定型ボタンの指示）、Pixel の Ask for Me（2024〜25。AI が店に電話して料金や空きを聞き、結果を後で見せる）、Duplex（2018 年の予約電話。Web 版は 2022 年に終了）。Google AI モードの予約は 2026-04 に 8 か国（日本の有無は要確認）
- Apple: iOS 26 で着信スクリーニングと保留待ちが日本語対応。Siri は App Intents で第三者アプリを呼ぶが順位は Apple が決める
- LINE ヤフー: Agent i を 2026-04-20 発表。上期に 20 領域以上。Agent i in chat（トークルーム内）は 2026 年内予定。LINE OA AI モード（2026 夏）、Agent i Biz（2026-08）。トレタ子会社化、LINE 経由予約の手数料 0 円。LINE の国内利用率は全年代 91〜95%、MAU 約 1 億。サードパーティへの Agent i 開放は API 未公表
- LINE・Instagram は友だち一覧・DM・トークを第三者に出さない。LINE に第三者から届く経路は公式アカウント（友だち追加した人のみ）と LIFF の shareTargetPicker（ユーザーが送り先を選ぶ）。公式アカウントはグループに招待されれば全メッセージを受け取れ、返信・投稿できる（1 グループ 1 アカウント、参加前の履歴は不可）。OS（Siri・Gemini）だけが LINE で自動送信できる
- 日本で LINE に挑んだメッセンジャーは全滅（+メッセージ 4,000 万配布、Kakao、Viber、Skype）。Threads は Meta の配布力でも 1 か月で DAU −79%。Partiful は 5 年で MAU 50 万・売上 0
- 電気通信事業法: 人と人の会話を媒介すると届出と通信の秘密が付く。iPhone の電話帳からの一括招待は Apple 審査規約 5.1.2(v) で禁止
- SMS: 日本で SMS を受けられるのは携帯番号（070/080/090/060）だけ。050 も 03 も不可。Twilio は日本の SMS 対応番号を提供せず、双方向は国内ゲートウェイの企業用番号のみ。国内の双方向 SMS（KDDI メッセージキャスト等）は企業に 1 本の審査済み共通番号
- 決済: 日本に個人向けの使い捨てバーチャルカードを第三者 API で発行できる基盤は見当たらない。法人向けの都度発行（インフキュリオン Xard 等）はある。Visa Intelligent Commerce は 2026 年初頭からアジア太平洋で試験導入（日本の明記なし）、Mastercard Agent Pay は 2025-11 に米国全会員、以後グローバル。GMO-PG が 2026-02 に Visa のネットワークトークン決済を実装
- 日本の予約は電話に依存: 台帳導入店でも予約の 45〜49% が電話。若い層の「電話が苦手」は各種調査で 6〜7 割前後（推定、出典要確認）。12 月は電話予約が年間最多、1 組 4.1 人

### 播口の見立て

- 日本語の音声対音声 AI の精度はまだ低く、エージェントが日本語の電話を完遂できるまで 1 年ほど。テキストは問題ない
- Google が同じ機能（発信の実況・自由文の指示・引き継ぎ）を組める部品を持つので、電話の優位の寿命は 12〜24 か月。その間に切替費用を積む
- パーソナルアシスタントは一度選ぶと変えにくいので、日本で一番最初に出す。機能の差より、シンプルに早く出す方がユーザーがつく
- ユーザーは電話にイライラしている。ここを取れれば強い

### 前回（2026-09-25 11:08 の think）以後に確定した事実

- 決済は HelloPay for Agents で実現する前提に置く（播口の判断。仕様は hello/hello-pay.md。要点: 本人は最初に 1 度カードを登録し、以後はチャットで OK を押すだけ。HelloPay 加盟店なら保管カードで API 請求、それ以外の店はライフカードが BIN スポンサーとして出す使い切り番号をエージェントが打つ。本人認証はライフカードが HelloPay の承認記録で通す。立て替えは保証金プールで、ライフカードがアクワイアラーでもあるので相殺を求める。損益は 1 万円あたり A（クレカ裏付け）−160 円、C（加盟店）+100 円。ロードマップは段階 0（2026-10〜11 ライフカードと条件を決める）→ 段階 1（2026-12〜2027-02 社内 100 件）→ 段階 2（2027-03〜05 テスター公開、電話の先の決済）→ 段階 3（2027 後半 Visa/Mastercard のエージェント用トークン）。Live View は for Agents が Hello の公開に間に合わない場合の最初の方式と、動いた後の例外用）
- HelloPay の事実: PSP、PCI DSS あり、アクワイアラーは今ライフカードのみ（入金月 2 回）、カード発行ライセンスは無い（ライフカードが BIN スポンサー）。HelloPay Issuing を 4 つ目のプロダクトに置き、将来の Hello Card（常設カード）もその上に載せる構想
- 日本のエージェント決済の現況: 本番は Mastercard × 三菱UFJニコス × Evonet の 1 件（2026-05）。Visa の検証に三井住友・ニコス・セゾン。消費者向けに取引ごとの番号を出す事業者は無い。Stripe Link（Muse が採用）は日本非対応
- Google は 2026-09-24 に「Call for Me」を米国の Pixel 11・有料 Gemini 向けに小規模で開始。AI が店に電話し、本人は実況を見て、いつでも引き取れる。発信は本人の携帯番号から。日本語・Pixel 以外・日本での提供は無い（TechCrunch 2026-09-24）
- Genspark は 2025 年から日本語の代理電話（Call For Me）を日本で提供（有料プラン）。予約・問い合わせ・キャンセルを AI が日本語でかける。実況・途中の指示・本人の引き取り・着信・本人名義の番号の有無は要確認
- AutoReserve の実測（2026-09-24 の社内文書）: Web・直近 30 日・カード決済ありの予約リクエスト 52,793 件のうち 32,478 件（61.5%）で 3DS が発火。チャレンジ（追加入力）の発生率は海外カードで高い
- HelloX の音声モデルは GPT-Live（音声対音声）を既定にする作業が 2026-09-24〜25 に進行中（社内仕様書）。最初の返答の後に黙り込む不具合を修正中
- hello.md の競合比較は 2026-09-25 に更新済み。「Hello に残る差は 4 つ。日本語で今出せること / Hello が付与した本人名義の番号で発信し着信も受けること / どの端末でも使えること / 電話の先で決済まで完結すること（HelloPay for Agents）」

### 調査メモ 1（Claude、2026-09-25 14:05〜14:34 の Web 調査。再実行時は --no-research で使う）


結論: 「日本で AI が 050 からかける」も「エージェント決済の A/C 二分」も既に他社が出しており、Hello に残る差は実況・引き取り・本人名義番号への着信・電話の先の決済の 4 つで、それを支える数字は下の通り。

1. **Meta Muse の料金と決済**: 無料枠は週の利用上限つき、Power $20/月、Maximum $100/月。米国 18 歳以上のみ、無料でもカード登録が必須。Link 加盟店（100 万超）では保存済み決済、それ以外は Link が承認額に限定した単回バーチャルカードを発行。他国展開の日付は未公表
   出典: https://www.usecarly.com/blog/meta-muse/ / https://stripe.com/newsroom/news/stripe-helps-meta-muse-shop-with-link
   効く点: HelloPay for Agents の C/A 二分は Muse×Link と同型。Link 日本非対応の間だけ「日本で先に出す」が成り立つ

2. **Muse の電話は人が 95〜98%**: Reuters（2026-09-22）。人が処理した通話の成功率 95〜98%、AI 単独は「大幅に低い」（数値未公表）。店が AI と気づいて切る事例が発端。テストは一旦終了
   出典: https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/09/22/meta-testing-a-human-concierge-for-its-new-personal-ai-agent-muse-reuters-exclusive/
   効く点: 英語でも AI 単独の完遂率は低い。「本人が引き継ぐ」設計が完遂率を埋める唯一の手段になる

3. **電話代行の裏に人、8 年繰り返し**: Google Duplex は 2019 年に通話の 25% を人が開始、15% で人が介入（NYT の実測では成功 4 件中 3 件が人）。Facebook M は回答の 70% 以上が人で 2018-01 終了
   出典: https://techcrunch.com/2019/05/22/googles-duplex-calls-still-frequently-require-human-intervention/ / https://en.wikipedia.org/wiki/M_(virtual_assistant)
   効く点: 運用部隊を使わない Hello は、AI 完遂率の低さを実況・引き取り UI で吸収する前提になる

4. **Google Call for Me の制約**: Pixel 11 系＋有料 Gemini＋Phone by Google 公開ベータ、端末言語が英語、米国内 18 歳以上、米国番号への発信のみ。他国は「未定」
   出典: https://9to5google.com/2026/09/24/pixel-11-call-for-me/
   効く点: 日本語化は言語・番号・端末の 3 条件を全部外す必要があり、12〜24 か月の見立ての根拠になる

5. **Google AI モードの予約代行は日本未提供**: エージェント型レストラン予約は 2026-05-07 時点で日本対象外。AI モード日本語版は 2025-09-09 開始
   出典: https://www.seohacks.net/column/30555/ / https://k-tai.watch.impress.co.jp/docs/news/2040998.html
   効く点: Google は電話以前の Web 予約代行すら日本に来ていない

6. **Genspark Call For Me の仕様**: 対応 7 か国（米英日シンガポール韓中仏）、通話基盤は 40 か国超。無料 1 日 100 クレジット、Plus $24.99/月、Pro $249.99/月。店側には 050 番号が表示され、AI が「Ruby」と名乗り録音告知。通話後に要約・全文・録音。実況・途中指示・本人引き取り・着信は記述なし（未確認）
   出典: https://murakami.pro/telephoneagent/ / https://note.com/enspire/n/nc1922b40d8e9 / https://www.genspark.ai/ja/blog/what-is-genspark
   効く点: 「日本で AI が 050 からかける」は既存。Hello の差は実況・途中指示・引き取り・着信・本人名義番号に限定される

7. **Genspark の規模**: ARR $250M（2026-03 末）、MAU 200 万超、有料席 約 10 万。日本の月間訪問 1,496 万（2026-01）、法人問い合わせは日本が世界首位
   出典: https://getlatka.com/companies/genspark.ai / https://pandaily.com/genspark-raises-385-million-accelerates-commercialization-of-ai-agent-platform / https://kotopat.com/en/gensparks-corporate-push-in-japan-shows-the-generative-ai-markets-battleground-is-shifting-from-models-to-business-deliverables/
   効く点: 日本で「一番最初のパーソナルアシスタント」はもう取られている。早い者勝ちの主張は「本人名義番号＋着信＋決済」で言い直す必要

8. **LINE Agent i の現況（2026-09-14）**: 基本無料、使い放題 750 円/月。27 領域（08-28）→10 月に 40 へ。タスク機能 09-11 提供。in chat は年内予定。予約・購入の代行は未提供（探す・比較・提案・通知まで）。1 日延べ 1,200 万利用
   出典: https://ai-revolution.co.jp/media/what-is-lineyahoo-agent-i/
   効く点: 月額の相場は 750 円。LINE の「代行」が無い窓は年内〜2027 前半

9. **PayPay と LINE の接続**: PayPay 登録 7,500 万（2026-08-09）、決済取扱高 12.5 兆円・78 億回（FY2024）。LINE×PayPay アカウント連携は 2026 夏開始。LY は PayPay 加盟店 1,000 万超で予約・購入・決済を代行する方針を明言
   出典: https://about.paypay.ne.jp/en/pr/20260810/01/ / https://www.watch.impress.co.jp/docs/news/2012321.html
   効く点: LINE 側の「決済まで完結」は PayPay で埋まる。Hello の決済の差は「PayPay が使えない相手（電話の先・カードのみの店）」に限定される

10. **OpenAI Instant Checkout の手数料**: 加盟店から 4%、Stripe の処理料 約 3.2% は別（$100 の注文で計 $7.20）。2025-09-29 米国開始、Shopify 加盟店は 2026-01 から。ユーザー無料
    出典: https://stripe.com/newsroom/news/stripe-openai-instant-checkout / https://www.growthcentr.com/chatgpt-instant-checkout-fees-and-requirements/
    効く点: 外部向け 3%（上限 3.5%）は OpenAI の 4% より低い。ただし OpenAI は加盟店負担、Hello の A ルートはユーザー負担 200 円/万で、負担者の前提が逆

11. **Stripe Issuing の単価**: バーチャルカード発行 $0.10/枚、紛争 $15/件、インターチェンジ分配あり（例: 取扱高の 1%）。日本では Issuing 非提供
    出典: https://stripe.com/pricing / https://stripe.com/guides/earn-revenue-by-issuing-cards
    効く点: hello-pay.md の発行手数料 −20 円/万・分配 +80 円/万の外部ベンチマーク

12. **Visa 日本国内クレジットの公開インターチェンジ**: 一般 2.28%（Classic）、非適格 2.68%、航空 1.10%、公共 0.60%、B2B 1,200 円＋0.80%。プリペイド・デビットの料率は同ページに無く未確認
    出典: https://www.visa.co.jp/about-visa/interchange-fees.html
    効く点: A ルートの +80 円/万（0.8%）はライフカードとの分配次第。プリペイド料率が別なら損益表を引き直す

13. **Vプリカ（ライフカードの既存商品）の手数料と使えない店**: ネット購入手数料 200 円/枚（額に関係なく）。利用不可: 継続課金（Vプリカ＋のみ可）、ガソリンスタンド、有料道路有人ブース、ギャンブル、電子マネー・ギフトコード購入、対面店舗、後日カード提示の要る取引（航空券・乗車券・チケット・ホテル事前予約）
    出典: https://support.vpc.lifecard.co.jp/%E2%85%A4%E3%83%97%E3%83%AA%E3%82%AB%E3%81%A7%E5%88%A9%E7%94%A8%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84%E3%82%B1%E3%83%BC%E3%82%B9%E3%82%92%E6%95%99%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84-66261dd1853d6b002599309f / https://vpc.lifecard.co.jp/rule2/gift.html / https://pay-route.co.jp/article/2026/04/03/v-prepaid-card-fees-comparison-and-saving-guide/
    効く点: A ルートが最初から弾かれる業種の一覧。ホテル・航空・チケットは Live View 予備が必須。200 円はユーザー手数料 −200 円/万と同額

14. **EMV 3-DS の全 EC 義務化**: 経産省ガイドライン 5.0（2024-03-15）で 2025-03 末までに原則全 EC 加盟店に導入
    出典: https://www.businesslawyers.jp/articles/1447 / https://www.veritrans.co.jp/tips/column/3d_secure.html
    効く点: 使い切り番号を打つ店の大半が 3DS を要求する。「ライフカードが承認記録で通す」が段階 0 の最重要確認。AutoReserve の発火率 61.5% は今後上がる（推測）

15. **自前発行の参入コスト**: 前払式か資金移動業のどちらかが必須。元 issuer 起業家の記事で資金移動業の登録に 1 年半以上、初期費用は「億を超える桁」。高額電子移転可能型（移転可能残高が 1 回 10 万円超 or 月 30 万円超）は犯収法の本人確認対象で事前届出
    出典: https://note.com/horishou/n/n5f8a08595269 / https://www.shigyo.co.jp/search_post/kinyu/prepaid/kougakudenshiiten/
    効く点: 自前発行却下の裏付け。単回・移転不可の使い切り番号は高額電子移転可能型に当たらない見込み（推測、段階 0 で弁護士確認）

16. **050 の本人確認と番号原価**: 携帯電話不正利用防止法施行規則の改正で 2024-04-01 から 050 アプリ電話も契約時本人確認（氏名・住居・生年月日）の対象。Twilio は日本番号を個人に売らず、法人の規制バンドル＋郵送で住所確認。Twilio の日本 National（050）$4.50/月、Toll Free $25/月、いずれも SMS 不可
    出典: https://biz.trustdock.io/column/mobilephonelaw / https://support.twilio.com/hc/en-us/articles/4405840066715-Japanese-Phone-Number-Regulatory-Changes / https://www.twilio.com/content/dam/twilio-com/pricing-data/en/csv/PMded94a0dae30eaaec0f115f22859bd38_SiteNumbersPricing.csv
    効く点: 1 ユーザー 1 番号の原価上限は小売で $4.50/月（卸はこれ未満と推測）。本人確認は電話機能の必須オンボーディング

17. **iOS 18.2（2024-12）で既定の通話・メッセージアプリを全世界で変更可**: WhatsApp が既定通話アプリとして対応済み
    出典: https://9to5mac.com/2024/10/23/ios-182-lets-you-set-new-default-apps-for-messaging-calls-more-via-settings-hub/
    効く点: Hello を iPhone の既定「通話」アプリに置ける。Hello 番号の着信・発信を電話帳と同列にし、切替費用を積む経路になる

18. **Apple 審査 3.1.5 / 3.1.3(e)**: アプリ外で消費する物品・サービスの購入は IAP 禁止（Apple Pay・カード入力を使う）
    出典: https://developer.apple.com/app-store/review/guidelines/
    効く点: Hello 内の予約・買い物・電話の先の決済は 30% の対象外。IAP になるのは月額課金だけ

19. **無断キャンセルの数字**: 経産省 2018-11 レポート、被害 年 2,000 億円、予約全体の 1% 弱、前日・2 日前キャンセル込みで 1.6 兆円。キャンセル料の目安はコース全額・席のみ客単価 5 割。TableCheck 調査では 7 割の店が対策せず、4 割で発生
    出典: https://president.jp/articles/-/26974 / https://prtimes.jp/main/html/rd/p/000000032.000023564.html
    効く点: 「カード保証つき予約電話」を店が受ける理由の定量根拠

20. **電話が苦手の出典**: ソフツー 2023-11 調査で若者世代の 7 割以上が「電話恐怖症」、ソフトバンク 2025-02 調査で 10・20 代の約 4 割が「電話が苦手」
    出典: https://prtimes.jp/main/html/rd/p/000000063.000028096.html / https://toyokeizai.net/articles/-/880458?display=b
    効く点: 前提の「6〜7 割（出典要確認）」の出典。定義で 4 割〜7 割にぶれる

21. **生成 AI の個人利用率**: 日本 26.7%（FY2024、前年 9.1%）、20 代 44.7%。米 68.8%、中 81.2%、独 59.2%
    出典: https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r07/html/nd112210.html / https://ledge.ai/articles/generative_ai_personal_use_japan_2025
    効く点: 「一度選んだら変えない」層の母集団は 20 代でも半分弱。早い者勝ちで取れる数の上限

Sources:
- [Meta Muse AI: What It Does, What It Costs](https://www.usecarly.com/blog/meta-muse/)
- [Stripe helps Muse shop with Link](https://stripe.com/newsroom/news/stripe-helps-meta-muse-shop-with-link)
- [Reuters exclusive via BNN Bloomberg](https://www.bnnbloomberg.ca/business/artificial-intelligence/2026/09/22/meta-testing-a-human-concierge-for-its-new-personal-ai-agent-muse-reuters-exclusive/)
- [TechCrunch: Duplex human intervention](https://techcrunch.com/2019/05/22/googles-duplex-calls-still-frequently-require-human-intervention/)
- [Wikipedia: M (virtual assistant)](https://en.wikipedia.org/wiki/M_(virtual_assistant))
- [9to5Google: Pixel 11 Call for Me](https://9to5google.com/2026/09/24/pixel-11-call-for-me/)
- [SEO HACKS: AI モード予約の提供地域](https://www.seohacks.net/column/30555/)
- [ケータイ Watch: AI モード予約](https://k-tai.watch.impress.co.jp/docs/news/2040998.html)
- [ムラカミドットプロ: Genspark 通話代行](https://murakami.pro/telephoneagent/)
- [note: Genspark×Pixel 通話検証](https://note.com/enspire/n/nc1922b40d8e9)
- [Genspark 公式ブログ](https://www.genspark.ai/ja/blog/what-is-genspark)
- [Getlatka: Genspark](https://getlatka.com/companies/genspark.ai)
- [Pandaily: Genspark $385M](https://pandaily.com/genspark-raises-385-million-accelerates-commercialization-of-ai-agent-platform)
- [Kotopat: Genspark Japan](https://kotopat.com/en/gensparks-corporate-push-in-japan-shows-the-generative-ai-markets-battleground-is-shifting-from-models-to-business-deliverables/)
- [AI革命: Agent i 2026年9月](https://ai-revolution.co.jp/media/what-is-lineyahoo-agent-i/)
- [PayPay PR 2026-08-10](https://about.paypay.ne.jp/en/pr/20260810/01/)
- [Impress Watch: LY AI カンパニー](https://www.watch.impress.co.jp/docs/news/2012321.html)
- [Stripe: Instant Checkout](https://stripe.com/newsroom/news/stripe-openai-instant-checkout)
- [Growthcentr: Instant Checkout fees](https://www.growthcentr.com/chatgpt-instant-checkout-fees-and-requirements/)
- [Stripe Pricing](https://stripe.com/pricing)
- [Stripe: earn revenue by issuing cards](https://stripe.com/guides/earn-revenue-by-issuing-cards)
- [Visa 日本 インターチェンジ](https://www.visa.co.jp/about-visa/interchange-fees.html)
- [Vプリカ 利用できないケース](https://support.vpc.lifecard.co.jp/%E2%85%A4%E3%83%97%E3%83%AA%E3%82%AB%E3%81%A7%E5%88%A9%E7%94%A8%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84%E3%82%B1%E3%83%BC%E3%82%B9%E3%82%92%E6%95%99%E3%81%88%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84-66261dd1853d6b002599309f)
- [Vプリカギフト利用規約](https://vpc.lifecard.co.jp/rule2/gift.html)
- [Vプリカ手数料比較](https://pay-route.co.jp/article/2026/04/03/v-prepaid-card-fees-comparison-and-saving-guide/)
- [BUSINESS LAWYERS: EMV 3DS 義務化](https://www.businesslawyers.jp/articles/1447)
- [DGFT: 3D セキュア](https://www.veritrans.co.jp/tips/column/3d_secure.html)
- [note: スタートアップがイシュアを始めるために](https://note.com/horishou/n/n5f8a08595269)
- [サポート行政書士法人: 高額電子移転可能型](https://www.shigyo.co.jp/search_post/kinyu/prepaid/kougakudenshiiten/)
- [TRUSTDOCK: 携帯電話不正利用防止法](https://biz.trustdock.io/column/mobilephonelaw)
- [Twilio: Japanese Phone Number Regulatory Changes](https://support.twilio.com/hc/en-us/articles/4405840066715-Japanese-Phone-Number-Regulatory-Changes)
- [Twilio: Numbers Pricing CSV](https://www.twilio.com/content/dam/twilio-com/pricing-data/en/csv/PMded94a0dae30eaaec0f115f22859bd38_SiteNumbersPricing.csv)
- [9to5Mac: iOS 18.2 default apps](https://9to5mac.com/2024/10/23/ios-182-lets-you-set-new-default-apps-for-messaging-calls-more-via-settings-hub/)
- [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [PRESIDENT: 無断キャンセル 2,000 億円](https://president.jp/articles/-/26974)
- [TableCheck PR: No show 調査](https://prtimes.jp/main/html/rd/p/000000032.000023564.html)
- [ソフツー PR: 電話恐怖症](https://prtimes.jp/main/html/rd/p/000000063.000028096.html)
- [東洋経済: 電話恐怖症](https://toyokeizai.net/articles/-/880458?display=b)
- [総務省 情報通信白書 令和7年版](https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r07/html/nd112210.html)
- [Ledge.ai: 生成AI 個人利用 26.7%](https://ledge.ai/articles/generative_ai_personal_use_japan_2025)

### 調査メモ 2（Codex、同上）


- **1．Genspark Plusは月払い24.99米ドル、年払い換算19.99米ドル／月。月間クレジットは10,000からで、代理電話は1件500クレジット、依頼分析・要約は別途消費する。**  
  → 出典：[料金](https://www.genspark.ai/business/pricing)、[会員プラン](https://www.genspark.ai/helpcenter/membership-plans)、[電話料金](https://mufg.genspark.ai/helpcenter/call-for-me)  
  → 効く点（推測）：Helloの月額と電話件数を決める直接の比較対象になる。

- **2．Gensparkは本人の既存番号を発信者番号として表示できる場合がある。条件は「SMSではなく音声通話で番号認証」「相手側の通信網が番号置換に対応」の2つ。日本での適用、着信対応、通話中の本人介入は未確認。**  
  → 出典：[Genspark電話仕様](https://mufg.genspark.ai/helpcenter/call-for-me)  
  → 効く点（推測）：本人番号での発信と、専用番号への着信を分けて競合比較する必要がある。

- **3．GensparkのGenTeamは、人と各人のAIが同じチャネルで会話・作業する製品。AIの応答設定は「メンション時だけ」「全メッセージ」の2種類で、メール・URLで参加者を招待できる。**  
  → 出典：[GenTeam公式仕様](https://www.genspark.ai/helpcenter/genteam)  
  → 効く点（推測）：人と各人のアシスタントが同居する部屋だけでは、Hello独自の機能にならない。

- **4．Museは基本利用0米ドルで、有料プランは利用量を増やす方式。Metaは大半の用途を無料枠で利用できると説明している。有料プランの現行価格・無料枠の完了件数は公式公開資料では未確認。**  
  → 出典：[Meta公式発表](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)  
  → 効く点（推測）：Helloの有料化には、無料の汎用依頼処理に追加して払う理由が必要になる。

- **5．Muse経由の対象購入にはLinkの購入保護が付く。米国の対象利用者には、破損・盗難・紛失最大500米ドル、返品送料等最大250米ドル、返品拒否時の返金保証最大1,000米ドルを追加料金なしで提供する。**  
  → 出典：[Museへの適用](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[Link補償条件](https://link.com/protections)  
  → 効く点（推測）：決済完了後の返品・補償まで、HelloPayと比較される。

- **6．日本のGoogle AI Proは月額2,900円で、5TBのストレージとGmail・Googleドキュメント内のAIを含む。Googleは150以上の国・地域で提供している。**  
  → 出典：[Google公式料金](https://gemini.google/jp/subscriptions/?hl=ja)  
  → 効く点（推測）：Helloが同程度の月額を取る場合、電話の利用価値をGoogleの同梱サービス全体と比較される。

- **7．Agent iは広告2種類で広告主への課金を開始済み。ディスプレイ広告は2026年7月23日、検索連動型ショッピング広告は8月31日から。Agent i単独への配信指定はできず、単独売上・利用者数は未確認。**  
  → 出典：[LINEヤフー公式発表](https://www.lycorp.co.jp/ja/news/release/020776/)  
  → 効く点（推測）：LINE側は利用者課金以外で依頼処理費を回収できるため、月額だけの価格比較では競争条件を捉えられない。

- **8．米国Rocket Moneyの2025年売上は3.90億米ドル、2024年は2.97億米ドル。電話等による料金交渉は成功時に初年度削減額の35〜60％を課金する方式がある。売上増の主因は有料会員増と開示している。**  
  → 出典：[2025年Form 10-K](https://www.sec.gov/Archives/edgar/data/1805284/000162828026013283/rkt-20251231.htm)、[交渉料金](https://help.rocketmoney.com/en/articles/9744501-bill-negotiation-savings-process)  
  → 効く点（推測）：電話代行を「削減できた金額」で課金する事業の実績として使える。

- **9．Yohanaは2023年9月に月額18,000円から10,000円へ値下げし、当時の日米累計対応は12万件以上。その後、2026年1月30日にサービスを終了した。終了時の会員数・採算・終了原因は未確認。**  
  → 出典：[料金改定と対応件数](https://news.panasonic.com/jp/topics/205303)、[終了告知](https://panasonic.jp/subscription/products/yohana.html)  
  → 効く点（推測）：汎用の生活支援では、対応件数の増加を継続課金の成立と同一視できない。

- **10．OpenTableは世界6万店以上。米国向けCoreは月額299米ドル＋送客した来店客1人1米ドル、Proは月額499米ドル＋同1米ドル。両プランとも自店サイト経由予約の従量料金は0、前払い体験には2％のサービス料がある。**  
  → 出典：[店舗数](https://www.opentable.com/blog/press/page/dining-trends-2026/)、[料金表](https://www.opentable.com/restaurant-solutions/plans/)  
  → 効く点（推測）：店側の月額・送客・前払いを別々に課金する設計の比較対象になる。

- **11．TableCheckは2024年のFastPass導入事例で、優先案内料390円／人・500円／人を公表。「Japanese Soba Noodles 蔦」では390円導入後、日本人客数が導入前の1.5倍になったと同社が報告している。**  
  → 出典：[TableCheck導入事例](https://www.tablecheck.com/join/about-us/press/2024/0209tablecheckfastpass/)  
  → 効く点（推測）：待ち時間を減らす結果に対する都度課金を、国内で検証する際の価格参考になる。

- **12．日本のiPhoneでは、サイドボタンの長押し1操作から第三者の音声会話アプリを起動できる。日本設定のApple Accountと日本国内での利用が条件で、起動後すぐ音声会話を開始する実装を求めている。**  
  → 出典：[Apple開発者仕様](https://developer.apple.com/documentation/appintents/launching-your-voice-based-conversational-app-from-the-side-button-of-iphone)  
  → 効く点（推測）：Hello自身を端末から直接呼び出す経路として検証できる。

- **13．日本のApp Storeはデジタルサービス売上に標準21％、対象プログラム参加者や2年目以降のサブスクには10％。Apple決済利用は追加5％、アプリ内リンク先Webでの購入は標準15％・対象条件下10％。物品・現実のサービス売上は対象外。**  
  → 出典：[Apple日本向け取引条件](https://www.apple.com/jp/newsroom/2025/12/apple-announces-changes-to-ios-in-japan/)  
  → 効く点（推測）：Helloの月額料金は、HelloPayで回収してもストア手数料が残る場合を含めて採算計算する必要がある。

- **14．Google Playの公式移行表では、日本の新料金体系は2026年9月30日開始予定。自動更新課金のサービス料は10％で、Google決済利用時は決済料が別途加算される。日本の追加決済料は同資料では未公表。**  
  → 出典：[Google Play新料金体系](https://support.google.com/googleplay/android-developer/answer/16954621?hl=en)  
  → 効く点（推測）：公開時期に適用されるAndroid課金条件で、月額の手取りを計算できる。

- **15．Google PlayはAccessibilityService APIによる自律的な開始・計画・実行を禁止している。人が定義した固定ルールによる自動化は許容するが、一般向け音声アシスタントは障害者支援ツールの例外対象にならない。**  
  → 出典：[Google Play公式ポリシー](https://support.google.com/googleplay/android-developer/answer/10964491?hl=en)  
  → 効く点（推測）：Android端末上で他社アプリをAIに操作させる方式は、Webブラウザ操作と分けて実装可否を判断する必要がある。

- **16．Twilioの日本向け公開小売価格は、National番号が月4.75米ドル、固定電話等への発信が毎分0.0746米ドル、携帯への発信が毎分0.1850米ドル。番号1万本の維持費は月47,500米ドルになる計算。Helloの仕入れ原価ではない。**  
  → 出典：[Twilio日本料金](https://www.twilio.com/en-us/voice/pricing/jp)  
  → 効く点（推測）：専用番号を無料付与する人数と、有料化する時点の比較基準になる。

- **17．旅行業法は、報酬を得て所定の旅行手配を行う事業に登録を要求し、旅行業者等には営業所ごとに旅行業務取扱管理者1人以上を要求する。Helloの宿泊・交通予約が該当するかは未確認。**  
  → 出典：[観光庁・旅行業法概要](https://www.mlit.go.jp/kankocho/seisaku_seido/ryokogyoho/ryokogyohogaiyo.html)  
  → 効く点（推測）：決済の実現とは別に、最初から受けられる旅行依頼の範囲を決める条件になる。

- **18．EU AI Act第50条の対人AIに関する透明性義務は2026年8月2日から適用。AIとの対話だと明白な場合等を除き、相手にAIとの対話であることを知らせる設計が必要。**  
  → 出典：[EU法令第50条](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)、[欧州委員会の適用日説明](https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems)  
  → 効く点（推測）：仏・伊・西・独向けの電話完了率は、AIだと告知する条件で測る必要がある。

- **19．経産省推計では、2024年の国内BtoC-ECは26.1兆円、そのうち旅行サービスは3兆5,249億円。これは購入・予約の取扱額で、アシスタントへの支払額ではない。**  
  → 出典：[経産省EC市場調査](https://www.meti.go.jp/press/2025/08/20250826005/20250826005.html)  
  → 効く点（推測）：市場規模から売上を計算する際、取扱額とHelloが徴収できる料金を分けられる。

- **20．日本政府観光局の2025年推計では訪日外客は4,268万3,600人。韓国945万9,600人、中国909万6,300人、台湾676万3,400人、香港251万7,300人で、4市場合計は65.2％になる計算。**  
  → 出典：[日本政府観光局・国地域別統計](https://res.cloudinary.com/jnto/image/upload/v1/media/filer_public/a6/94/a694ba81-4622-4d6a-8570-7b8fcd88a114/number_of_visitor_arrivals_to_japan_in_december_2025_gtklma)  
  → 効く点（推測）：訪日客向けに始める場合、中国語・韓国語での依頼受付の優先順位を判断できる。

## 議論の経過（推論・却下した案）

- 2026-09-24 の think「連絡先とチャットをパーソナルアシスタント基盤の体験に置き換え、バイラルで LINE を disrupt できるか」の結論は否定的だった: 「置き換えは捨てる。電話番号で届く形を取り、LINE 公式アカウント＋LIFF で幹事予約を取り、汎用アシスタントの開発は 2027-02 まで止める」。根拠は LINE 利用率 91〜95%、Threads・Partiful・+メッセージの先例、通信の秘密、Apple の電話帳規約。播口はこれを受けず、汎用アシスタントを作り、チャットで LINE を disrupt する方針を維持した。Claude の懸念（OS が呼ばれる位置を持つ / 慣性は今の習慣を持つ側を守る / Muse は乗り換えを要求しない）は出し終えている
- 却下した案: 電話完遂と食の記録を Muse・ChatGPT・Agent i に供給する側に立つ（播口は自社アシスタントを選択）/ アプリに雑談チャットを載せて LINE を直接崩す → その後「用事から生まれる部屋」＋普通のチャットも持つ、に転換 / LINE・Instagram の連絡先統合（API が閉じている）/ 汎用でなく食に特化した店選び AI だけ（播口は汎用を選択）/ 運用部隊が電話を引き取る（人件費が乗る）/ Hello の法人バーチャルカードで立替（店に Hello 名義が出る）/ ワンタイムコードの転送（規約と詐欺の文面）/ 用途ごとの URL や複数のカード型（複雑化）/ 登録なしで答える Partiful 型（入る人を取る道具にする）/ deferred deep link
- Opus の機能分解（推定）: LINE の起動の 9 割は雑談・家族連絡・通知で、時間では 4 割。幹事・予約・集金・電話の用事は起動の 5% で時間の 5 割超（週 37 分）。10 倍便利は起動回数でなく用事 1 件の所要時間で出す。「置き換え」の理由になる束は幹事リンク＋電話代行＋委任回答の 3 つ
- Claude の整理: 番号の効用は発信でなく着信（本人が外に出す番号）にあり、切替費用として積まれる。早い者勝ちは「1 人あたりに積まれた量」で決まる。LINE の Agent i in chat と正面で競わず、参加者がプラットフォームをまたぐ予定と実行が要る予定を取る（この段落は hello.md からは削除された）
- 未決のまま残っているもの: 課金（番号・月額・件数）/ 優位の 12〜24 か月で何をどの順に積むか / 最初に出す用事と配布の具体

- 前回の think（2026-09-25 11:08）の結論: 「差は電話＋Hello 名義の番号 1 本に絞る。決済は日本の実購入 100 件を測るまで差に数えない。チャットは招待 URL→部屋→普通チャットの順に数値で通す。判定 1〜3（〜2026-12 発信＋引き継ぎ、〜2027-03 着信＋1 人 1 番号、〜2027-06 保証つき予約電話と招待 URL）」。仮説より強いと事実で示せた案は無し。播口は「決済は HelloPay for Agents の仕様を書いたので実現できる前提で再度 think」と指示した。決済を差から外す前回の結論は、この前提で見直す
- 播口は「普通チャットを判定 3 の後に置く」に同意していない（「早めに引き剥がす」を維持）

## 現在の仮説（播口）

hello/hello.md の全文が仮説（競合比較は 2026-09-25 更新済み）。要約:

- Muse と同じ種類の汎用パーソナルアシスタントを日本で一番最初に出す。当たり前の部分は他社と同水準でよい
- 差がつくのは電話と決済。Hello が付与した 050 番号から AI が電話し、本人が実況を見て指示し、いつでも代われ、出られなければ折り返す。着信も受ける。決済は HelloPay for Agents で、本人はチャットで OK を押すだけで、電話の先（Web も API も無い店）まで決済が届く。HelloX × HelloPay で「カード保証つきの予約電話」「電話で交渉してその場で払う」「相手も HelloX ならデータで完結」
- チャットと連絡先を Hello の中に持ち、LINE を disrupt する。普通のチャットとグループチャットができ、同じ部屋にそれぞれのアシスタントが居る。入口は招待としての共有 URL。早めに引き剥がしに行く
- 早い者勝ち。切替費用（外に出した番号・記録・保存セッションとカード・委任）を 1 人あたりに積む

問いたいこと:

1. 決済が HelloPay for Agents で実現する前提で、この戦略で Muse・Google・Apple・LINE・Genspark と戦えるか。戦える根拠と戦えない根拠を事実で分ける
2. 「電話と決済を差にする」「チャットで LINE を disrupt する」「日本で一番最初に出す」のうち、どれが事実で崩れ、どれが立つか。前回の結論（決済を差から外す、チャットは後）を、この前提で改めるべき点と維持すべき点
3. 優位の寿命の間に何をどの順に積めば守れるか。数字で判定できる条件にする
4. 何が事実ならこの戦略を変えるべきか
