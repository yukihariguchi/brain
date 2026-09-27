# Assistant Benchmark 上位 10 製品と日韓台の国内勢を踏まえ、Hello（パーソナルアシスタント）は何をどの順に開発し、どの国にどの順で出すべきか（アジア中心。日本・韓国・台湾・香港・SG・タイ）

## 背景（事実）

2026-09-27 時点で播口と Claude が事実として共有しているもの。hello/hello.md・hello/hello-pay.md・hello/base.md・decisions.md に無いものを含む。

### Hello 側の前提（brain に無い細部）

- Hello, Inc. は日本の親会社の下に UK・韓国（ソウル）・台湾（台北）の 100% 子会社を既に持つ。2027 年に SG 親会社へ組み替える予定。KR / TW は「各国の事業運営」の箱と決めている
- HelloDining（AutoReserve）の店の営業順は 日本 → 韓国・台湾・香港・タイ・SG → パリ・ロンドン・バルセロナ・ローマ → 米国は最後、と決めている。AutoReserve は登録 500 万（海外 100 万）、AI 電話予約は日英仏伊西独で本番稼働。飲食店から AI 電話予約の削除要望が続くとの記事あり（ITmedia 2026-07-10）
- Hello の電話は HelloX（音声 AI＋クラウド PBX）。日本では 050 番号の付与に契約時の本人確認が義務（2024-04-01〜）。2026-04-01 の規則改正で本人確認書類の画像送信方式は廃止
- 決済の主方式は HelloPay for Agents（ライフカードを BIN スポンサーにした取引ごとの使い切りバーチャル Visa プリペイド）。段階 0（2026-10〜11）でライフカードと条件を決め、段階 1（2026-12〜2027-02）社内 100 件、段階 2（2027-03〜05）テスター公開、段階 3（2027 年後半）Visa / Mastercard のエージェント用トークン
- Live View（Hello 側のクラウドブラウザの映像を本人の端末に映し、本人が CVV と 3D セキュアのコードを相手のページに直接打つ）は for Agents が間に合わない場合の最初の決済方式、かつ動いた後の例外用。09-27 に開発側から「ブラウザ映像への直接入力はスクロールと入力の体験が悪い」と指摘があり、対策は「相手のページを見せたまま、アプリの入力欄から打鍵を遠隔ブラウザに直送（Hello のサーバーと LLM を通さない）」と整理した。アプリで認証コードを集めて裏で書き込む方式は、値が Hello を通るので「コードの転送」と同じになり採らない（本人の補償が消える・発行会社が経路を止めうる・詐欺の型と同じ）
- Hello JP は純資産マイナス。現預金・調達余力は未提示。正社員 50 名規模。Hello のアプリはまだ無く、最初は社内テスター版を目指す
- 前回 think（2026-09-25）の判定日程: 判定 1（〜2026-12）社外 100 人で期限内完了率 90%・本人作業時間は自己手配の半分以下 / 判定 2（〜2027-03）付与 60 日後に有料者の 50% 以上が着信用件を本人対応なしで解決 / 判定 3（〜2027-06）for Agents の実購入 100 件で誤請求 0・90 日有料継続 60%・変動費控除後の収支が正。値は仮置き

### Assistant Benchmark（assistantbenchmark.com、2026-09-25 更新）

- David Pawlan の個人プロジェクト（GitHub 公開、MIT）。スポンサー・アフィリエイトなし。各項目に公開タスク 1 つを実際に使い 1〜10 点。中核 8 項目（オンライン作業・推薦・購入・メール返信・先回り・ルーティン・外部連携・権限）＋追加 7 項目（記憶・人格・電話・グループ・連続タスク・先回りの自制・コンテンツ作成）。総合点の計算式は非公開。126 製品中 26 テスト済み
- JPMorgan がこの表を引用して Muse を 1 位と紹介し、投資家が「サブスクは手軽な収益化、コマース（Shopify・PayPal・Walmart・Instacart・Stripe）の方が大きい機会」と述べた
- 上位 10 の点数（総合 / 速度）: Muse 9.3 / 7 秒、Instinct 8.5 / 20 秒、Pally 8.3 / 22 秒、Ollie 8.3 / 11 秒、szn 8.2 / 39 秒、Shuffle 7.8 / 55 秒、Tomo 7.6 / 11 秒、Town 7.5 / 7 秒、Asaply 7.5 / 8 秒、Grok Bot 7.3 / 10 秒
- Muse の項目: オンライン作業 9・旅行 7・推薦 9・購入 10・メール 10・ルーティン 10・連携 10・権限 9。先回り・記憶・電話・グループは空欄（未テスト）
- 電話 10 点は szn のみ。グループは Ollie 9・Pally 7。記憶は szn 10・Instinct 9
- 10 製品とも、日本語・韓国語・繁体字中国語への対応とアジア展開予定の公式情報は無い

### 上位 10 製品の事実（2026-09-27、Web 検索。出典は末尾）

- Meta Muse（Meta）: 2026-09-08 発表。無料 / 月 20 ドル / 月 100 ドル。将来は取引手数料で収益（ザッカーバーグ）。提供は米国とカナダ（カナダは 2026-02-18）、18 歳以上。日本の App Store に無く、韓国・アジアの時期は「未定」。電話は 9/17 に米国内の店への AI 発信をベータ拡大。人のコンシェルジュが代行する試験で委託先が差別発言をし、VP が「a miss」と認めてロールバック。人が電話すると成功率 95〜98% という社内結果あり。決済は Stripe Link（1 回限りの仮想カード）。Stripe / Shopify / Shop Pay / PayPal と提携。自前のブラウザ VM（Amazon にブロックされる）。連携は Instagram / WhatsApp / Ticketmaster / OpenTable / Gmail / Google カレンダー / Drive に加え 9/23 に Best Buy / Gap / Sephora / Walmart / Wayfair / Expedia / GitHub / Notion。開発者コネクタ申請 1,500 件超。配布は iOS / Android / Web / WhatsApp 内、Mac のデスクトップ操作と専用メールアドレス。DL 推計 230〜430 万（9/25）、米国モバイル DAU 64.2 万（9/21）、9/18 に米 App Store 1 位
- Instinct（Spear Street Technology、SF）: 2025 年創業、創業者 23 歳・元 Sierra。累計 3.5 億ドル、評価額 25 億ドル（2026-08、Index / Benchmark）。100 億ドル評価で 10 億ドル調達交渉中と報道。招待制ベータで無料、課金より広告を検討。電話発信「Instinct Concierge」を 9/17 にアーリーアクセス。家族同士でエージェントが調整する Trusted People。常時動くクラウド PC。決済は接続済みの支払い手段で 1 回ごと承認、Stripe Link を含む。配布は iMessage / WhatsApp / 電話。利用者 10 万人超。専用メールアドレス（9/9）。連携解除後もメールを保存していた件が指摘された
- Pally（YC S25）: 2026-06 ローンチ、シード 520 万ドル。無料 / Pro 月 25 ドル / Max 月 100 ドル。通話枠は無料 15 分・Pro 30 分・Max 60 分。自分の番号とメールアドレスは Max のみ。既存の iMessage グループに参加可、新規作成は不可。ブラウザで予約・購入を承認付きで実行、承認は Face ID。配布は iMessage / RCS / WhatsApp / Telegram、アプリ不要
- Ollie（サンディエゴ）: シード 750 万ドル（2026-09-08、Khosla）。無料 月 50 通 / Everyday 月 25 ドル 150 通 / Always-On 月 100 ドル 1,000 通。有料は家族のグループチャット全体をカバー。買い物先は Amazon / Instacart / Walmart。電話発信なし。決済は購入の手前まで準備し請求はしない。配布は iMessage / SMS
- szn（theszn.ai）: 資金・所在不明。プレビュー中は無料。アシスタントごとに自分の電話番号・受信箱・PC を持つ。記憶 10 点（通路側席・豚肉 NG を指示なしで反映）。連携は Notion / カレンダー / Slack に接続できず 7 点。配布は iMessage / 電話 / Web
- Shuffle（getshuffle.xyz）: Pro 月 39 ドル / Ultra 月 199 ドル。米国の +1 番号。iMessage / SMS のグループに番号を足す方式（Pro 40 人）。決済なし。旅行機能の記載なし（表と不一致）
- Tomo（Mapo Labs、SF）: 2026-06 シード 500 万ドル（Bain Capital Ventures）。Pro 月 19.99 ドル。iOS と iMessage のみ。目標達成コーチ型。ステルス 3.5 ヶ月で有料 1 万人、月 20 日利用
- Town（SF、元 Plaid CTO）: 2026-06 シリーズ A 5,500 万ドル（a16z）。無料 月 30 チャット / 15〜199 ドル。仕事向け。連携 50 以上（Gmail / Outlook / Slack / Teams / HubSpot / Notion / Salesforce / GitHub / Linear）。電話・決済・ブラウザ操作の記載なし
- Asaply: ハッカソン発。サブスクなし、注文に少額手数料を上乗せ。近所の用事（コーヒー・ランチ・チケット・配車）。SMS / iMessage のみ。決済は Apple Pay で Asaply はカード番号を見ない。地域ごとに順次展開、英語のみ
- Grok Bot（xAI → SpaceXAI）: 2026-08-11 限定ベータ。月 300 ドルの最上位プラン等の契約者のみ。Bot ごとにクラウド PC（ブラウザ・ファイル・ターミナル）で 24 時間動作。Bot 同士のグループチャット。電話・決済の記載なし
- 共通点: 上位 10 のうち 7 製品（Instinct・Pally・Ollie・szn・Shuffle・Tomo・Asaply）が iMessage / SMS / WhatsApp の中で動き、専用アプリを持たないか任意。Muse・Instinct・Pally・szn・Shuffle・Tomo の 6 製品が「アシスタント専用の電話番号やメールアドレス」を持つか持ち始めた

### 日本（2026-09-27、Web 検索）

- LINE ヤフー Agent i: 2026-04-20 開始。DAU 1,200 万（複数入口の延べ）。領域エージェント 27（10 月までに 40）。単独アプリは 10 月予定。機能は探す・比べる・提案まで。予約・決済・電話代行の一般提供発表は無い。無料枠あり、使い放題は月 750 円。「Agent i in chat」（トークでタスク整理・カレンダー登録）は 2026 年内予定
- ソフトバンク（OpenAI と組む Crystal Intelligence）・NTT ドコモは法人向けのみ確認。個人向け汎用エージェントは確認できず
- Gemini in Chrome は 2026-04-20 に日本で開始（デスクトップのみ）。ブラウザ操作のエージェント機能は米国の有料プランのみ
- ChatGPT の agent モードは 2026 年 8 月上旬に廃止との記述あり（一次ソース未確認）。Instant Checkout は米国のみで 2026-03 に終了し、加盟店サイトへ送る形に変更
- Perplexity Comet: 全 OS で無料、46 言語。日本語・韓国語対応の明示と各国決済対応は不明
- LINE 国内 MAU 1 億超（2026-01-29）
- 決済: 2025 年キャッシュレス比率 58.0%、うちクレジット 82.7%。コード決済は前年比 +22.6%。EMV 3-D セキュアは 2025-03 末までに全 EC 加盟店へ原則導入
- Visa Agentic Ready（発行会社向け検証、2026-04-30 開始）の日本参加はクレディセゾン・三菱 UFJ ニコス・楽天カード・三井住友カード。Mastercard Agent Pay は 2026-05-20 に国内初の本番取引（三菱 UFJ ニコス等のカードで配車予約）
- 飲食予約: 店側の受付経路は電話 48.6%・グルメサイト 29.6%（飲食店ドットコム）。利用者側はネット予約 82.0%・電話 48.0%（リクルート 2023-11）。食べログのネット予約店舗 9.8 万（二次情報）
- Twilio の日本番号ガイドラインは法人書類のみ記載。個人向け可否は明記なし

### 韓国

- Kakao: ChatGPT for Kakao（2025-10 開始）が 2026-05 に累計 1,100 万人。Kakao Tools 経由で地図・予約・ギフトへ遷移（予約は画面遷移で本人が完了）。単独アプリ Kanana は 2026-10 終了、KakaoTalk 内は継続。KakaoTalk 国内 MAU 4,960 万（2026 Q2）
- Naver: Agent N。ショッピングエージェントを全カテゴリへ拡大中。地図の Place Agent はチャットで Naver 予約を依頼できる
- SKT A.: Agent Call で登録企業のコールセンター待ちを代行。SKT 加入者約 3,000 万に実質無料
- Samsung Galaxy S26: Bixby・Gemini・Perplexity の 3 エージェント。Gemini は配車・再注文をバックグラウンド実行
- 電話番号: 本人確認は携帯 3 社の PASS・SMS 認証が標準、本人名義の契約が前提。Twilio は Local / National / Toll-free は個人不可、Mobile は身分証で個人可、再販業者・ISV へは全種別提供不可
- 決済: 月内利用率 Naver Pay 64.7%・Kakao Pay 49.8%・Toss Pay 31.1%。3-D セキュアは ISP・안심클릭が慣行、EMV 3DS の義務化は不明。Visa Agentic Ready 参加は KB 国民・サムスン・新韓・カカオバンク・ハナ・現代。Mastercard は新韓カードで国内初の本番取引
- 飲食予約: CatchTable 国内 350 万ユーザー。Naver・Kakao・Tabling は韓国の本人認証が必要。電話比率は不明

### 台湾

- LINE 台湾: 2025-10-22 に「AI 代理時代」を宣言。店側向け AI 音声予約と公式アカウント向け会話アシスタント（2026 Q1 予定）。消費者向け汎用エージェントの提供状況は不明。LINE 台湾 2,200 万ユーザー（人口の約 94%）
- 台湾大哥大 MyAgent は法人向け。PChome の AI エージェントは不明
- 電話番号: Twilio は Local / Mobile を個人可（国内住所証明と身分証）。アプリが個人に番号を付与する場合の実名制の規制は不明
- 決済: EC はクレジット約 54%・ウォレット約 30%。LINE Pay 登録 1,310 万。3-D セキュアは決済代行で標準有効、義務化は確認できず。Visa Agentic Ready 参加は永豐・中國信託・玉山・台新・聯邦。Mastercard Agent Pay の本番取引完了国に台湾を含む
- 飲食予約: inline が約 3,000 店で EZTABLE に並び、ミシュラン店の 3 分の 2 が inline を採用。電話比率は不明

### 香港・SG・タイ・ベトナム・インドネシア（補助）

- Grab AI Assistant: 2026-04-08 発表。店探しから予約まで会話で完了。SG で提供、ID・MY・PH・TH・VN は年内予定
- メッセンジャー: SG・ID は WhatsApp、VN は Zalo（7,000 万超）、タイは LINE。WhatsApp の Meta AI は SG 提供済み
- QR 決済: QRIS（ID）は 2025 年 182 億件・利用者 5,700 万。PromptPay（TH）登録 7,400 万、タイは口座間送金が EC 44%・店頭 43%
- Mastercard の本番取引: SG（DBS・UOB）、香港（HSBC・DBS）、タイ（Krungthai Card）
- Visa Agentic Ready の 10 市場に日韓台・香港・SG・タイ・VN を含む。Mastercard Agent Pay の本番完了国に豪・NZ・SG・MY・印・韓・台・日・香港・タイ
- 各国の電話番号規制・3DS 義務化・飲食予約慣行は未調査

### 出典

- https://assistantbenchmark.com/ / https://github.com/dpawlan/ai-assistant-benchmark
- https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- https://techcrunch.com/2026/09/25/meta-is-putting-its-muscle-behind-muse-as-the-ai-app-takes-off/
- https://techcrunch.com/2026/09/21/metas-muse-is-outpacing-chatgpts-early-mobile-launch/
- https://techcrunch.com/2026/09/17/rival-ai-agents-instinct-and-metas-muse-both-add-the-ability-to-make-calls/
- https://www.404media.co/meta-tests-muse-ai-agent-calls-that-are-actually-made-by-humans-in-a-call-center/
- https://en.sedaily.com/international/2026/09/26/metas-muse-ai-agent-upends-industry-in-us-debut
- https://techcrunch.com/2026/08/26/viral-ai-startup-instinct-has-raised-350-million-at-a-2-5-billion-valuation/
- https://pally.com/ / https://ollie.ai/pricing/ / https://theszn.ai/ / https://www.getshuffle.xyz/ / https://www.town.com/press/series-a / https://asaply.ai/
- https://pulse2.com/tomo-raises-5-million-seed-round-led-by-bain-capital-ventures/
- https://www.mindstudio.ai/blog/grokbot-xai-agent-app
- https://www.watch.impress.co.jp/docs/news/2136632.html / https://www.lycorp.co.jp/ja/news/release/020594/
- https://techcrunch.com/2026/04/20/google-rolls-out-gemini-in-chrome-in-seven-new-countries/
- https://www.visa.com.sg/about-visa/newsroom/press-releases/visa-launches-agentic-ready-program-in-asia-pacific-with-over-50-partners-advancing-agentic-commerce.html
- https://thepaypers.com/payments/news/mastercard-rolls-out-authenticated-agentic-transactions-across-asean
- https://paymentnavi.com/paymentnews/174963.html
- https://www.watch.impress.co.jp/docs/news/2099068.html
- https://www.inshokuten.com/research/magazine/article/68 / https://www.recruit.co.jp/newsroom/pressrelease/2023/1121_12760.html
- https://www.itmedia.co.jp/business/articles/2607/10/news010.html
- https://www.kedglobal.com/artificial-intelligence/newsView/ked202510280008
- https://www.digitaltoday.co.kr/en/view/104683/naver-map-launches-place-agent-to-find-and-book-places-through-chat
- https://www.telecompaper.com/news/skt-expands-a-dot-ai-assistant-with-call-handling-and-task-management-features--1575607
- https://www.twilio.com/en-us/guidelines/kr/regulatory / https://www.twilio.com/en-us/guidelines/tw/regulatory / https://www.twilio.com/en-us/guidelines/jp/regulatory
- https://www.koreajoongangdaily.com/business/naver-pay-tops-korean-mobile-payment-market-on-rewards/12755193
- https://seoulstart.com/guides/catchtable-reservations-guide
- https://www.ithome.com.tw/news/171889 / https://www.cw.com.tw/article/5102319
- https://topics.amcham.com.tw/2025/10/taiwans-mobile-payments-from-boom-to-balance/
- https://www.grab.com/sg/press/others/grab-unveils-13-ai-powered-experiences-at-grabx-2026-as-southeast-asias-intelligent-everyday-guide/

## 議論の経過

- 前回 think（2026-09-25「Hello の戦略で戦えるか（HelloPay for Agents 前提）」）の結論: 事実で優位を確認できた別案は無い。決済は差に戻す。優位期間の長さは推測なので、判定は毎月の競合比較に置く。導入の順は 着信 → 決済リンク → for Agents。「日本初」は獲得理由にならず、測るのは既存利用者が追加で有料で使う率。要確認は HelloX の PBX の会議通話、ライフカードの条件書、Genspark Call For Me の実測、実原価と資金額
- 09-27 に Claude が Assistant Benchmark の表を読んで出した整理（播口は明示的に採否を言っていない）: Muse が空欄の 4 列（先回り・記憶・電話・グループ）が Hello のタブ（電話・チャットの部屋・自分の記憶）と一致し、差は測られている項目で空いている。Muse は購入 10 点なので「決済まで完結」は日本で先に出す話であって機能で勝つ話ではない。電話 10 の szn、グループ 9 の Ollie が米国に既にあり、Meta は WhatsApp を持つのでグループは時間の問題。Hello の優位は「日本語で今」「本人名義の番号」に絞られる。ツイートの「他社 38 秒」は szn の数字で、Town・Asaply は 7〜8 秒。Claude は「決済を差別化の柱として語るのはやめ、柱は電話と番号」と述べた
- hello.md の現行記述との差分（今回の調査で判明）: hello.md は Muse を「米国限定・電話は人のコールセンター」と書くが、実際は米国とカナダで提供、AI 発信のベータを 9/17 に拡大し、人の代行はロールバック済み。Instinct・Pally・szn・Shuffle・Tomo も自分の番号を持つか持ち始めており、「アシスタント名義の番号」は米国では独自でなくなりつつある
- 却下した案（09-27 の会話）: 3D セキュアの認証コードをアプリの入力欄で集めて Hello が書き込む方式。ユーザーにリスクを開示して同意を取れば可、という案も、Hello がコードを持つ瞬間の責任・発行会社による経路停止・詐欺の型と同じになる点で採らないと整理した

## 現在の仮説

播口は今回の論点（開発順序・展開国）について明示的な仮説をまだ出していない。brain に書かれている現状の方針は次の通りで、これを仮説として置く。

- 開発順序: 電話（本人名義の 050 番号、実況・途中の指示・本人の引き取り・着信）→ 部屋（友人との共有チャットにアシスタントが同居、招待 URL でバイラル）→ 記憶と委任ルール。決済は Live View で最初に出し、HelloPay for Agents を段階 1〜3 で載せる。前回 think の導入順は 着信 → 決済リンク → for Agents
- 展開国: 日本で一番最初に出す（Muse・Agent i・Google が日本で使える形になる前に Hello を選んだ人を作る）。韓国・台湾は子会社があり、HelloDining の営業順は 日本 → 韓国・台湾・香港・タイ・SG。Hello（アシスタント）の国順は未決
- 課金（番号・月額・件数）と「優位期間で何をどの順に積むか」は hello.md で「議論中（未決）」

問いたいこと:
1. 上位 10 製品の共通点（メッセンジャー内で動く・アシスタント専用の番号とメール・クラウド PC・1 回ごと承認）に照らして、Hello の開発順序（電話 → 部屋 → 記憶 → 決済）は妥当か。変えるなら何を前に、何を後ろに置くか。特に「専用アプリ＋自前のチャット」で行く前提と、LINE / iMessage / WhatsApp の中で動く前提のどちらが早く積めるか
2. 展開国の順序。日本の次を韓国・台湾にする根拠はあるか（子会社・AutoReserve の登録・LINE 台湾）。韓国は Kakao / Naver / SKT が電話代行と予約に既に手を出し、番号付与の規制が厳しい。台湾は LINE が店側の AI 音声予約を出した。香港・SG は Muse（WhatsApp）と Grab が先に来る。国ごとに「Hello が勝てる条件」と「出さない条件」を事実で示してほしい
3. 各国で決済をどう揃えるか。HelloPay for Agents（ライフカードの使い切り Visa）は日本限定の仕組み。韓国（Naver Pay / Kakao Pay）・台湾（LINE Pay）・タイ（PromptPay）は財布と QR が主で、カードのエージェント用トークンは発行会社ごとに 2026 年から検証段階。国ごとに決済の最初の方式は何にすべきか
