# 連絡先とチャットをパーソナルアシスタント基盤の新しい体験に置き換え、ローンチ後にバイラルで広がる前提で、Hello は LINE を disrupt できるか

日付: 2026-09-24 / 討論ラウンド: 3 / Claude: fable(xhigh) / Codex: gpt-6-astra(xhigh) / 調査: あり / 参照: hello/hello-dining.md, hello/hello.md, decisions.md

---

修正。連絡先とチャットの置き換えは捨てる。取る位置は、店も客も電話番号で届く形。10 月に Respo 顧客連絡（SMS・AI 電話・AR 通知）を entry の有料オプションで 100 店に売り、店の LINE 公式アカウント支出を置き換える。11〜12 月に LINE 公式アカウント + LIFF で会社の飲み会の幹事予約を取り、出欠回答で SMS 認証の電話番号を取る。K は「幹事 1 人あたり招待人数 × 招待された人が 60 日以内に別グループで初の有料予約を成立させた率」。課金は大人数・個室の条件予約 500 円/件（仮置き）。2027-02 に K≧1 かつ有人引取の変動費が手数料以下なら、SMS で受け付ける Hello 自社のアプリと Web 受付を作る。汎用アシスタントの開発はそれまで止める。例外は委任回答で、12 月の出欠回答のトグル選択率が 30% 以上（仮置き）なら K の判定を待たずに作る。

- LINE 利用率は全年代 91〜95%、10 代も 9 割超、MAU 1 億。+メッセージは 4,000 万配布、Threads は Meta の配布力でも 1 か月で DAU −79%、招待リンク型の Partiful は 5 年で MAU 50 万・売上 0。推測: バイラル単独で 1 億人の習慣は動かない。委任回答を足した場合の成立可能性は先例では否定できない
- 第三者が LINE ユーザーに届く経路は shareTargetPicker と公式アカウントだけ。EU が法で強制した WhatsApp の相互接続も 3 年で 2 社。日本に LINE を開かせる法は未確認。既存の LINE のトークには入れない
- エージェント同士のチャットは他人の通信の媒介に当たり、電気通信事業法 16 条の届出と通信の秘密が付く。既存の LINE・Instagram のトークから「大事なものだけエスカレ」の判定材料は取れない。本人が Hello 上で条件を登録し、Hello 経由の新規依頼への回答だけ委任する形はこの制約に当たらない
- iPhone の電話帳からの一括招待は Apple 審査規約 5.1.2(v) で禁止。電話帳の件数を招待数に置けない
- 比較値: Kakao は 1 MAU 年 約 4 万 5,600 ウォン（広告・コマース）、Meta の WhatsApp は店側の送信課金で年換算 20 億ドル超。消費者課金は LYP プレミアム 637 万人・Truecaller の継続収入 49% の実績があるが、チャット単独への支払意思の実測は無い
- 配布費は PayPay 型で 1 人 約 2,500 円。Hello JP は純資産マイナスで、現預金・調達余力は未提示。出せるかは今週の数字で決まる
- 店側は支出が既にある。LINE 公式アカウント有償 49.3 万件、店の支払い月 5,000〜15,000 円 + 3 円/通。台帳導入店でも予約の 45〜49% が電話。Respo に予約者番号が残る経路の範囲は未確認（entry は他台帳と併用可）。推測: 顧客連絡は方針 1 の延長で開発工数が小さい
- 10 月の採用条件: 導入店の LINE 公式アカウント請求額が 3 か月で減り、かつ AR の指名予約手数料の減少分を差し引いた Hello 全体の利益が増えること。配信通数の減少では認めない
- 12 月は電話予約件数が年間最多、1 組 4.1 人。Agent i in chat は年内予定・第三者 API 未公表・収益貢献は 2027 年度以降。12 月の招待はトークルーム内に LINE 自身のエージェントが無い状態で出せるが、60 日観測の判定（2027-02）は Agent i in chat 提供後になる
- 日本語電話の優位は居住者にも効く。Muse・Instinct・Google の電話は米国・英語のみ。SMS 認証の番号があれば次の招待は Hello の SMS から始まり、K の観測が LINE 側の自己申告に依らない
- 12 月に同時に測るもの: 委任回答トグルの選択率、条件予約 500 円の有料成立率、総依頼数に対する有人対応件数と変動費。K だけでは採否を決めない

仮説より強い可能性がある案:
- デフォルト通話・SMS アプリ（iOS 18.2 のデフォルト設定に Hello の AI 電話を置き、連絡先は端末の電話帳）: 日本の携帯番号への着信を転送・番号変更なしで AI が受けて本人へ引き継げる実機検証が通り、有料会員 1 人あたり月額収入（480 円、仮置き）が有人・通信・推論・決済の変動費を上回るなら採る
- 委任回答（出欠と同時に「この相手なら条件内で代理回答を任せる」を設定）: 上記の例外条件で開発に入る。選択率だけでは「返信を任せられることが招待の理由になる」効果は K に乗らず、K の上振れは実装後に測る
- 訪日客の Web 電話代行（7 日 2,500 円か 1 件 500 円、仮置き）: 欧米豪の訪日客への実販売で購入率・選択率を取り、提携先の紹介料を引いた限界利益が正なら 2027 に採る
- 法人手配（Slack・Teams に Hello 秘書、会社払い）: 500 円/席と 800 円/件を並べた契約選択率と、有料 1 社を取る総費用・日数が出て、entry の無料獲得原価と分けて採算が立つなら採る
- グループ月額で予約・支払いを委任（幹事 1,500 円/月、仮置き）: 09-23 のユーザー月額課金却下を覆す判断が要る。100 グループ 8 週間で、条件内でも毎回の最終確認を要求する率が過半数未満なら試す
- 月 3 万円の有人秘書: LINE の置き換えにはならない。単独商品として、1 人あたり月 5 時間以内の有人稼働で処理でき、既存 AR 上位 1% に月 3 万円相当を払う層がいるなら試す
- 来店報酬付き提案（店が 1 人 1,000 円、客 500 円・Hello 500 円）: 09-23「店選びに金を入れない」と当たる。AR 検索ログで条件検索の比率が伸び、Respo で来店確認できる店の LINE 公式アカウント支出が月 2 万円を超えることが出るまで採らない
- 企業負担の世帯向け代行（世帯 1,000 円/月）: Hello・aisaac・A2Z・Rise の従業員世帯で有料試験し、月の依頼件数と有人引取率が世帯 500 円以内に収まり、更新する企業があるなら採る
- 席の保証買い取り: 純資産マイナスを理由にした棄却は現預金未提示なので保留に戻す。Hello JP の月次資金繰りで月 2.4 億の保証を負えること、Respo 導入店の曜日別空席率、09-23 の独占却下を覆す事実が揃うまで採らない

残る反論:
- 60 日観測中に Agent i in chat が出れば、K は「LINE にエージェントが無い環境」の数字にならない。1 世代でも 2 世代でも消えず、1〜2 月の閑散期の季節補正も無い。K≧1 の閾値の扱いは未決着
- 委任回答トグルを付けても、代理回答そのものは 12 月に提供しない。K<1 でも「委任付きなら K が上がる」可能性は否定できない。未決着

要確認:
- 運用部隊の時間単価と、人が引き取った電話 1 件の平均処理時間。人事の契約と HelloX・AR の通話ログ
- 総依頼数と有人対応件数（運用ログ）、通信・推論・決済の費用（請求明細）。全案の変動費と有人比率はこの 2 つと上の単価で決まる
- Hello JP の現預金と追加調達余力。PayPay 型配布費 1 人 2,500 円 × 100 万人 = 25 億（仮置き）を出せるか。財務
- LINE 経由予約の電話番号保存率、Respo 顧客連絡導入店の導入前後 3 か月の LINE 公式アカウント請求額、同期間の AR 指名予約手数料の増減。連携予約データと Respo 顧客記録の突合、店の請求書、AR の手数料ログ
- K の集計条件: 60 日以内・別グループ・初の有料予約成立・同一人物と同一グループの重複除外・紹介報酬なし。LIFF の招待元と予約履歴の突合

出典:
- https://www.lycorp.co.jp/ja/news/release/020775/
- https://www.soumu.go.jp/menu_news/s-news/01iicp01_02000125.html
- https://www.soumu.go.jp/johotsusintokei/whitepaper/ja/r07/html/nd111120.html
- https://ja.wikipedia.org/wiki/+メッセージ
- https://petapixel.com/2023/07/24/threads-daily-active-users-fall-by-staggering-70/
- https://sacra.com/c/partiful/
- https://about.fb.com/news/2025/11/messaging-interoperability-whatsapp-enables-third-party-chats-for-users-in-europe/
- https://www.soumu.go.jp/main_content/000477428.pdf
- https://www.ppc.go.jp/files/pdf/14_dekyo_shishin.pdf
- https://developer.apple.com/app-store/review/guidelines/#data-use-and-sharing
- https://www.kakaocorp.com/page/detail/11812?lang=ENG
- https://www.marketingbrew.com/stories/2026/01/29/meta-s-ad-revenue-climbs-ai-capex
- https://corporate.truecaller.com/newsroom/press-release/sequential-growth-across-all-revenue-streams?id=AF7CD16BDA563CF7
- https://about.paypay.ne.jp/pr/20181213/01/
- https://www.lycorp.co.jp/ja/ir/library/presentations/main/013/teaserItems2/04/linkList/02/link/jp2025q4_presentation.pdf
- https://www.lycbiz.com/jp/service/line-official-account/plan/
- https://www.lycbiz.com/jp/news/line-official-account/20260216/
- https://prtimes.jp/main/html/rd/p/000000083.000038464.html
- https://www.ebica.jp/news/press/reservation-report-2024-detail/
- https://www.nikkei.com/article/DGXZQOUC0884M0Y6A500C2000000/
- https://blog.google/products-and-platforms/products/shopping/how-to-agentic-calling-let-google-call/
- https://9to5mac.com/2025/03/27/whatsapp-default-app-iphone/
- https://calendly.com/pricing
- https://www.sec.gov/Archives/edgar/data/1581760/000158176026000142/a360q226resultspresentat.htm
