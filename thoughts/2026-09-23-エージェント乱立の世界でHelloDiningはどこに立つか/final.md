# 汎用エージェントが乱立し、OS 側が「呼ばれる位置」を持つ世界で、HelloDining はどこに立つのが一番儲かるか

日付: 2026-09-23 / 討論ラウンド: 3 / Claude: fable(xhigh) / Codex: gpt-6-astra(xhigh) / 調査: あり / 参照: hello/hello-dining.md, decisions.md

---

修正。Shopify 型 × B を採る。10 案のうち事実で落ちたものは無く、現仮説との優劣は数字で未決。直すのは「会計を AR で完結」の売り方、店側課金の分け方と請求条件、接続順の根拠。

- Google は自社台帳を持たず、認定台帳 8 社経由で予約を店の手数料なしで通す。脅威が「台帳を取られること」より「認定から外れること」にあるのは推測で、Google が台帳に参入しない根拠は無い。
- LINE ヤフーはトレタ（約 2 万店）を子会社化し、LINE 経由の予約手数料は 0 円。LINE は接続先でなく競合台帳を持つ側。接続順は OS・Google の後。
- Amex は Resy・Tock を保有、TheFork 買収を契約（7 億ドル、年内クローズ予定）、Resy 台帳と Toast POS の接続を 2026 年中の計画として公表。完了すれば 3 台帳 75,000 店で加盟店は米欧のみ。台帳＋POS＋決済の同じ形を先に選んでいる。
- 決済と成果報酬は別建てにする。総額を 200 円/人に制限して束ねると、客単価 6,667 円超で決済 3% だけで 200 円を超え、成果報酬が消える。
- 成果報酬の請求条件は現行どおり「AR が選んだ初めての客がまた来たら」。初回来店課金は採らない（収入が学習正解「また行った率」から切れる）。請求開始は AR 提案経由の初回来店と再訪が数字で出てから。AR は今「他で決めた店を予約する場所」で需要を作っていない。
- それまで店側の金は決済と HelloPay のデポジット・ノーショー課金で立てる。原資は無断キャンセル損害 年約 2,000 億円（2018 年時点）。
- 主決済を売る理由は「台帳・POS・決済を 1 社で入れる」で、料率は既存端末と同率（約 3%）。ノーショー課金は現行 HelloPay の範囲で済み、会計移管の理由にならない。Dojo は台帳にカード登録を同梱して Google 認定 8 社に入り、Toast は POS＋決済で 18 万拠点。退店時自動精算の実績は両社に無く、1 社同梱が Respo で効くかは推測。
- 決済の取り分の参照値: Toast の決済テイクレート 50bp、融資込みフィンテック粗利は決済額の約 0.59%、粗利総テイクレート 98bp。Hello の決済単独の取り分は仕入料率と Connect（0.25%＋250 円/入金）で決まり、0.5〜1% に置くのは推測。
- 接続の費用: App Intents は費用ゼロで順位は Apple が決める（確定）。ChatGPT の 4% は Shopify の商品購入の料率で、飲食予約の支払料率は未確認。Google は店に手数料を課さないが、台帳パートナーの接続料率は未確認。OS を先に開き、Google・ChatGPT は飲食予約の料率を確認してから並べる。
- Apple 3.1.3(e) は飲食代を IAP でなくカード払いにさせる。AR の会計に IAP 手数料は掛からない。IAP 以外の Apple の手数料の有無は未確認。

仮説より強い可能性がある案:
- ノーショー保証・Hello 引受（保証料 150 円/件は仮置き）。採る条件は Respo 実測で予約 1 件の回収後損失＋処理費が 150 円未満、かつ店 1 店あたりの（保証料 − 損失 − 処理費）が決済純取り分（月 GMV × 純料率）を上回ること。デポジット撤廃後の損失増を同じ店・同じ条件で測る。
- ノーショー保証・保険会社引受（Hello 利用料は対象予約額の 0.2%、仮置き）。採る条件は対象予約に限った回収後補償額＋保険会社経費が対象予約額の 0.6% 未満で引受が成立し、かつ利用料が決済純取り分を上回ること。
- 人気店有料台帳＋台帳買収（月 3 万円＋前払い 3%）。採る条件は 2 つ。競合が POS・電話 AI まで 0 円同梱で出ること。有料試験の 12 か月継続率と店舗当たり利益で、継続店 1 店あたり取得費（買収対価＋統合費）の回収が 5 年以内（5 年は仮置き）。買収資金は要調達（推測）。
- 国境をまたぐ客に限定（訪日客・出国する日本人）。採る条件は獲得後 12 か月利益（予約・決済・店課金 − 獲得費 − 対応原価）で訪日客が国内客を上回り、HelloPay 訪日決済の決済・為替原価控除後料率が 2% 以上。
- Respo 卸（他社 POS・決済会社に月 5,000 円/店、仮置き）。採る条件は最低保証付き契約の 3 年累積キャッシュフローが、同じ開発・営業予算を直販に使う場合を上回ること。店側記録は AR に集まらない。
- 与信（台帳・POS・決済の売上記録で将来売上買取か貸付）。HelloPay 決済額が立った後の 2 段目。採る条件は年 300 万円・手数料 10% で審査通過する Respo 店の割合と、回収終了案件の貸倒・資金調達・審査・回収費控除後の資金 1 億円あたり年間利益が正であること。
- カード網で来店・支出を確定（店側の全店獲得をやめる）。採る条件は日本のカードネットワークが第三者に加盟店名つき取引通知を出す基盤を開放していること（未確認）、登録者の飲食支出のうち本人の来店まで照合できる割合、店負担 8% で獲得費控除後に利益が出ること。Respo の店側記録を捨てるので現方針の強みと両立しない。
- カード発行会社向け飲食特典（年 240 円/会員、仮置き）。採る条件は対照群試験で発行会社の年間増分粗利が特典原資＋240 円/会員を上回ること。会計記録は Respo に残らない。
- 食目的の旅行商品（Hello 受取 1 人 3 万円、仮置き）。採る条件は有料販売で 1 人 3 万円を確保し、販売費・直接原価控除後に黒字。AR の 6 言語に中韓台が無く対象は欧米客に限られる（推測）。
- 飲食店買収（50 店、仮置き）。採る条件は創業者の労働を市場給与に置き換え、設備更新費を計上しても店舗利益が残ること。所有店を AR の店選びに載せると「金で順位を動かす」と同じ問題になる。白ロンドンの店舗別営業利益率で先に測れる。

残る反論:
- 現仮説の店 1 店あたり実測粗利が無い。10 案との優劣は売上目標と仮置き粗利の比較で、数字で決まっていない。
- 同率の HelloPay に店が主決済を替える理由は 1 社同梱の推測。Dojo・Toast はカード登録と POS 決済の先例で、退店時自動精算の実績は無い。
- Google が台帳を自作しない前提は推測。参入すれば認定台帳の位置も消える。

要確認:
- Respo 台帳のノーショー率、予約 1 件の回収後損失＋処理費、デポジットあり・なしの差。Respo の予約・来店・請求記録と店の回収明細。
- Reserve with Google の日本の認定台帳一覧と Respo の認定可否（Google に確認）。別に、Respo 稼働店のうち 30 日以上の枠・1 秒未満の空席応答・オンライン取消を満たす店数と割合（予約枠・応答時間・取消対応の実測）。
- HelloPay 主決済 1 店の 12 か月粗利。実決済額・入金回数（決済明細）、仕入料率と Connect 0.25%＋250 円/入金（決済会社の見積もり）、エージェントへの支払（接続契約）、導入対応費（導入原価台帳）。
- 国内客・訪日客別の獲得後 12 か月利益（AR 予約ログ・決済明細・原価台帳）、訪日決済の決済・為替原価控除後料率（決済会社の見積もり）。
- OpenAI 飲食予約の支払料率、Google 台帳パートナーの接続料率（各社の契約条件）。
- 国内飲食 POS・決済上位 5 社の稼働飲食店数と自社・親会社の台帳・電話 AI の有無（各社 IR・製品ページ）。卸先が残るか。

出典:
- https://www.semrush.com/blog/ai-mode-agentic-restaurant-booking/
- https://winbuzzer.com/2026/04/13/google-ai-mode-rolls-out-restaurant-booking-to-8-countries-xcxwbn/
- https://developers.google.com/actions-center/verticals/reservations/e2e/policies/integration-policies
- https://www.watch.impress.co.jp/docs/news/2082138.html
- https://toreta.in/news/2026-08-25/
- https://www.lycbiz.com/jp/service/line-official-account/restaurant-reservation-plan/
- https://ir.tripadvisor.com/news-releases/news-release-details/tripadvisor-enters-agreement-sell-thefork-american-express-700
- https://www.americanexpress.com/en-us/newsroom/articles/travel-and-dining/resy-announces-next-phase-of-its-reservation-and-dining-platform.html
- https://owner.tabelog.com/home/net_reservation/
- https://forbesjapan.com/articles/detail/81993
- https://dojo.tech/accept-card-payments/restaurant/
- https://www.sec.gov/Archives/edgar/data/1650164/000165016426000057/tost-20251231.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/11/toast-tost-q2-2026-earnings-call-transcript/
- https://stripe.com/jp/connect/pricing
- https://www.pymnts.com/news/ecommerce/2026/shopify-merchants-to-pay-4percent-fee-on-sales-made-through-chatgpt-checkout/
- https://developers.openai.com/plugins/guides/restaurant-reservation-conversion-spec
- https://www.techtimes.com/articles/318005/20260608/wwdc-2026-app-intents-replaces-sirikit-gemini-siri-migration-clock-starts.htm
- https://developer.apple.com/jp/app-store/review/guidelines/
