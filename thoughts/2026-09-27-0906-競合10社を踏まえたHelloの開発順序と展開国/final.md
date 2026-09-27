# Assistant Benchmark 上位 10 製品と日韓台の国内勢を踏まえ、Hello（パーソナルアシスタント）は何をどの順に開発し、どの国にどの順で出すべきか（アジア中心。日本・韓国・台湾・香港・SG・タイ）

日付: 2026-09-27 / 討論ラウンド: 3 / Claude: fable(xhigh) / Codex: gpt-6-astra(xhigh) / 調査: あり / 参照: hello/hello.md, hello/hello-pay.md, hello/base.md, hello/hello-dining.md, decisions.md

---

修正。優位を事実で確認できた別案は無い。順序は 電話 → 記憶・委任 → 決済 → 部屋に変える。国は 日本 → 台湾で、韓国・香港・SG（シンガポール）・タイは条件達成まで出さない。自前発行の決済は日本だけで、他国は本人が店の画面で払う。

- 専用アプリを採る（推測）。番号・記録の保持にアプリは要らない（Pally はアプリ不要で番号を持ち、HelloPay もアプリ不要の設計）。Web や既存メッセンジャーでの実装比較は無い。WhatsApp は汎用 AI ボットを禁止し、アジアに例外が無い。LINE Messaging API の同種規定は未確認なので入口候補にとどめる。
- 部屋を最後に回す。人と人の会話を運ぶ部屋は電気通信事業法の届出が要る。判定 1（社外 100 人）に招待 URL は要らない。招待 URL は部屋と同時に出す。着手条件は届出完了と判定 1 通過。
- 記憶・委任を 2 番目に置く。承認 5 択の「常に」「このサイトでは」は委任ルールに書く設計で、決済より前に要る。委任ルールは hello.md の 3 つ（曜日と時間帯・予算・食の制約）を維持し、承認の書き先を足す。部屋の自動調整もこの情報を使う。
- 日本の最初の決済は Live View（直送方式）と Respo 店への直接請求（C）。hello-pay.md の試算（推測。実料率で引き直す）では C が 1 万円あたり +100 円で唯一の黒字、使い切りカード（A）は −160 円。A は非加盟店で支払いが要る用件に限る。for Agents の段階 0〜3 は変えない。
- 課金は Web の HelloPay で件数＋月額を取る。日本の iOS はアプリ内 21〜26%、アプリ内リンク経由の Web 購入は 15%（リンク後 7 日以内）。韓国も第三者決済に 26% が乗る。
- 台湾を 2 番目にする。番号は個人に出せる（NCC（台湾の通信主管庁）の再販登録が要る）。Visa Agentic Ready 5 行と Mastercard 本番があり、子会社がある。公開条件は 3 つ。番号調達契約。台湾の中国語の音声 AI が日本語と同じ完了率。inline・LINE で終わらない用件への有料注文。
- 韓国は保留。Twilio の制限は再販業者・ISV（独立ソフトウェア事業者）向けで、国全体の禁止ではない。Naver・Kakao・SKT が予約と電話代行を持ち、SKT は 3,000 万人に実質無料。AI 基本法で利用告知と生成物ラベルが要る。条件は個人名義番号の供給契約と有料注文。韓国・台湾の子会社の 2027 年の仕事は訪日客向けに置く。日本語版に韓国語・繁体字 UI を足し、AutoReserve 海外登録 100 万に番号なしで配る。訪日客は韓国 946 万・台湾 676 万。
- 香港・SG・タイは条件達成まで出さない。香港は WhatsApp 74.7% で汎用ボット不可、+8529 携帯番号は個人申請可だが音声在庫と再販契約が未確認、広東語の音声 AI が無い。SG は国内番号（Level 3・6）が個人不可で再販に SBO 免許（通信サービス事業者免許）が要り、携帯番号は個人申請可だが音声在庫と Hello の再販条件が未確認。Meta AI（WhatsApp）と Grab AI Assistant が先行（料金は未確認）。タイは番号は個人可だがタイ語の音声 AI が無く、PromptPay の入金照合は未検証、Grab（Chope）と LINE MAN 60 万店が台帳を持ち、子会社が無い。
- 自前発行の決済は日本だけ。台湾は最低資本 NT$5 億、韓国は登録、香港は SVF（ストアドバリュー）免許、SG は MAS（シンガポール金融管理局）の免許が要る。他国は本人が店の画面（カード・Naver Pay・LINE Pay・PromptPay）で払う。海外の公開条件は店の注文 ID・金額・支払結果を Hello が照合できること。Live View は認証入力の手段で、ウォレット対応の代わりにしない。

仮説より強い可能性がある案:
- LINE 公式アカウントの中で動く Hello（電話だけアプリ）。LINE Messaging API が汎用アシスタントの公式アカウントを認め、LINE 追加→本人確認→初回有料の転換率が専用アプリの DL→有料より高いなら採る。
- カード会社が会員分を払う法人配布。ライフカード等が対象会員全員（有効化会員だけでなく）に月 100 円以上を払う予算承認済みの条件書があれば採る。
- 財布（for Agents）を電話より先に AutoReserve で配る。段階 0 の条件書で発行 API と外販が通り、外部 5 社と最低保証 GMV 付きの契約条件書が揃えば採る。
- 訪日客向け単独製品（旅行パス、Hello JP 名義のプール番号）。AR の韓台登録者への試験販売で購入率 5% 以上、1 旅行あたりの電話用件が 1 件以上、訪日客が使える本人確認方式が確認できれば採る。
- iPhone サイドボタン起動の音声版を先行。インストール者のボタン割当率と、割当者の有料率・30 日継続が文字入口より高ければ採る。
- 返品・キャンセル・返金完了の成功報酬（日本のみ）。返金可能な 200 件で申込率 10% 以上、完了 1 件の変動費 1,000 円以下、弁護士法 72 条・旅行業法に当たらないと確認できれば採る。
- 台湾で幹事だけに課金し参加者は登録なし。09-24 の「登録なしで答える経路は最初は出さない」を覆し、inline・EZTABLE の予約変更 API が第三者に開き、幹事 100 人の試用で月 1,980 円の継続が 20 人以上なら採る。
- 韓国で利用者の PC 内に記憶とログインを置く有料版。韓国語 20 タスクでローカル LLM の完了率がクラウド最上位から 10 ポイント以内、有料試用 100 人で PC 不在による未処理が 30% 未満なら採る。

残る反論:
- 判定 1 は完了率 90% と作業時間半減だけで、価格と購入率の条件が無い。通過しても追加料金を払う需要は確認できない。判定 1 に有料注文の条件を足すかは未決。

要確認:
- LINE Messaging API に汎用アシスタントの公式アカウントを禁じる規定と審査基準の有無。LINE Developers の利用規約と LINE ヤフーへの照会で取る。
- 台湾で個人向けに再販できる番号の調達先と 1 番号の月額。Hello TW から NCC 登録の番号事業者と Twilio に照会して取る。
- Hello JP の現預金と調達余力。電話・記憶・決済を 2027-06 まで並行できる額か。Hello JP の資金繰り表で取る。
- LINE 追加→本人確認→初回有料と、アプリ DL→本人確認→初回有料の段階別人数。比較試験の操作ログと請求台帳で取る。
- 国別の価格提示人数と購入人数（日本の判定 1 の 100 人、台湾のテスター、AR の韓台登録者への訪日客向け販売）。請求台帳で取る。
- 台湾の中国語の電話の試行件数・完了件数と日本語との差。HelloX の通話ログで取る。

出典:
- https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform
- https://techcrunch.com/2026/01/15/after-italy-whatsapp-excludes-brazil-from-rival-chatbot-ban
- https://pally.com/
- https://web-lawyers.net/chat_telecommunications_business_law/
- https://www.lrm.jp/security_magazine/notification_tbl/
- https://k-tai.watch.impress.co.jp/docs/column/value/2074126.html
- https://developer.apple.com/support/app-distribution-in-japan
- https://www.koreajoongangdaily.com/business/korea-finds-google-apple-violated-inapp-purchases-law/12822157
- https://www.twilio.com/en-us/guidelines/hk/regulatory
- https://www.twilio.com/en-us/guidelines/sg/regulatory
- https://www.twilio.com/en-us/guidelines/th/regulatory
- https://www.twilio.com/en-us/guidelines/tw/regulatory
- https://www.twilio.com/en-us/guidelines/kr/regulatory
- https://ncclaw.ncc.gov.tw/FLAW/FLAWDAT0201.aspx?id=FL103297
- https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=G0380237
- https://www.kimchang.com/en/insights/detail.kc?sch_section=4&idx=33646
- https://www.lexology.com/library/detail.aspx?g=809b664b-5c67-4f0a-900c-c4de357e5a25
- https://www.mas.gov.sg/contact-us/faqs/payments-faqs/payments-service-licensing-faqs
- https://www.trade.gov/market-intelligence/south-korea-ai-basic-act
- https://www.statista.com/statistics/412500/hk-social-network-penetration/
- https://techcrunch.com/2024/07/23/grab-acquires-singapores-restaurant-reservation-platform-chope
- https://www.grab.com/sg/press/others/grab-unveils-13-ai-powered-experiences-at-grabx-2026-as-southeast-asias-intelligent-everyday-guide/
- https://lmwn.com/about-us/
- https://www.jnto.go.jp/news/_files/20260121_1615.pdf
