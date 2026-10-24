# Hello

HP: https://hello.ai（法人の概要・事業の説明・体制・用語は 2026-09-22 に HP から転記）

## 法人（会社）

Hello は「法人」と「事業」を分けて捉える。法人は国ごとの箱で、事業は法人をまたいで動く。

### 現在（2026-09-19）

親会社: 株式会社ハロー（Hello JP、日本）

- 英名: Hello, Inc.
- 設立: 2018年6月20日
- 資本金: 1億円
- 本社: 〒150-0013 東京都渋谷区恵比寿1-21-8 VORT恵比寿Ⅲ 2F
- 事業内容（登記上の表記）: AutoReserve、Respo by AutoReserve、HelloX の企画・開発・運用
- タグライン: Goodbye past, Hello future.
- ミッション: 社会通念や常識にとらわれず、他でもない自分たちのアイデアを信じ、まだ世の中にないものを生みだす

100%子会社:

- Hello AI Limited（Hello UK、イギリス。会社番号 15113006）: WeWork, 5 Merchant Square, London, W2 1DP（2026-10-19 Companies House で確認。旧 434 St. Ann's Road, N15 3JH）
- 주식회사 헬로한국（Hello KR、韓国）: 9F-112, 7 Teheran-ro 5-gil, Gangnam-gu, Seoul
- 哈囉台灣網路科技股份有限公司（Hello TW、台湾）: 臺北市中山區南京東路一段15號三樓

代表: 親会社・3子会社とも播口友紀（Yuki Hariguchi）

### 予定

- Hello SG 親会社化（2027年の株式交換、UK / KR / TW 子会社の Hello SG 下への移転、執行役員の SG 移住。2026-09-22 方針）は撤回（2026-10-24）。Hello JP が親会社のまま。子会社を売る計画が無く、配当の差も小さいため。decisions.md 参照
- 株主は HGSG / AWSMSG / メンバー の構成を目指す（下の 10-19 方針）。aisaac は Hello 株を持たない（2026-10-24）
- 上場は未定。するなら Nasdaq

- 2026-10-19 方針（検討中）: 株主構成を HGSG 60% / AWSMSG 20% / メンバー 20% に整理する（播口・田中の個人保有は残さない。播口個人分は出国直後に HGSG へ、2026-09-21 決定どおり）。それ以外の株主から HGSG が買い取る（2026-10-19 決定。他株主の顔ぶれ・比率は要確認。資金は HGJP → HGSG の貸付を想定、利率・外為法・SG の利子源泉は要確認）。上の「SG 法人 3社が株主」の予定との整合は要確認。背景は aisaac/base.md「資本の再編」

### 法人の役割（2026-09-22 方針。Hello SG 親会社化の撤回で見直しが要る。HelloAlpha の IP の置き場（hello/hello-alpha.md）と合わせて要確認、2026-10-24）

- Hello SG: 親会社。IP の持ち主。執行役員が経営。HelloAlpha の運用会社（LFMC）はこの下に別法人で作る
- Hello JP: 日本の事業運営。HelloDining / HelloX / HelloPay の国内売上。HelloAlpha では受託開発と日本の投資家窓口
- Hello UK: HelloAlpha の運用会社（第1段、FCA）。中核人材の SG 移住後は受託開発会社
- Hello KR / TW: 各国の事業運営

## 事業群（2026-09-22）

4事業。区分は播口による（HP は製品単位で掲載）。事業は法人をまたぐ。

HelloDining（飲食店向け事業）→ 詳細は hello/hello-dining.md

- AutoReserve: AI によるレストラン予約サイト。AI が電話で飲食店を予約する。toC。日英のほか仏・伊・西・独に対応。autoreserve.com
- Respo（Respo by AutoReserve）: 飲食店向けオールインワン（予約台帳・POS・セルフオーダー・決済）。toB。導入例に久丹、SAVOY 麻布十番、鮨 木場谷、山﨑。ぴかいちナビと連携

HelloX

- 音声 AI の電話サービス。AI エージェント＋クラウド PBX の「AI クラウドフォン」。店舗からコンタクトセンターまで。hellovoice.ai

HelloPay

- 決済代行。カード・Apple Pay・Google Pay・サブスク決済を API で提供。Respo 向けは RespoPay、端末レス決済。pay.hello.ai
- プロダクト名（2026-09-25）: HelloPay Payments（オンライン）/ HelloPay Terminal（店頭。RespoPay を含む）/ HelloPay Issuing（カード発行の基盤）/ HelloPay for Agents（エージェント決済）。詳細は hello/hello-pay.md

HelloAlpha

- ヘッジファンド事業（HP 未掲載）。hello/hello-alpha.md

## 体制（2026-09-22、HP より）

取締役

- 代表取締役 CEO: 播口友紀
- 取締役 CTO: 杉本風斗（2022年就任。元 Nota、クックパッド）
- 社外取締役: 田中和希（aisaac 共同創業者、Ruby コミッター）

事業責任者クラス（HP 掲載分）

- Chief Engineer（2018年10月入社、創業期から）
- Chief of Staff（2024年入社、元 Respo 事業責任者）
- AutoReserve 事業責任者
- Respo 事業責任者
- Respo セールスマネージャー（SMB / エンタープライズ）
- HelloX は 2026年9月時点で PdM・事業開発責任者・バックエンドエンジニアを募集中（0→1 フェーズ）

規模・働き方

- 正社員 50名規模。採用責任者の求人で 100名規模への拡大を掲げている
- 別に 200人規模の運用部隊（AutoReserve / HelloX の電話オペレーション）がある。雇用形態は要確認
- 原則週3日出社（遠隔地居住者を除く）。コアタイムなしのフレックス。副業は申請制
- 副業エンジニアの契約は hello/hr.md

## 方針・判断基準

利益の置き場（2026-09-22）

- 利益は稼いだ国で課税され、動かせるのは機能と人。売上を SG につけても取り分は変わらない
- Hello SG が本人（残余利益を取る側）になる条件は、SG の執行役員が実際に意思決定しリスクを負うこと。日本の社員が Slack で決めていると調査で崩れる
- Hello SG → Hello JP の経営指導料はコストプラス 5% 前後。役務の記録と契約書・算定根拠を先に作る
- toC の IP を Hello SG に置くなら、Hello JP から時価で移す（含み益に約 30%）。純資産マイナスの今が一番安い。DCF で見られるのでゼロにはならない。要確認
- Hello JP に欠損金がある間は、日本で稼いだ利益は税ゼロ。使い切るまでは日本に機能を残す方が残る。欠損金の額と期限は要確認

SO（2026-09-22）

- Hello SG の SO は日本の社員には非適格。行使時の差額が給与所得で最大 55%。SG 社員は最大 24%、UK は EMI が使える可能性（要確認）
- 対策は、幹部には時価が低い今のうちに生株、それ以外は Hello SG の有償 SO（外国法人の扱いは要確認）。上場しないなら SO より生株か現金の利益連動報酬

## 用語

- Hello JP / UK / KR / TW / SG: 法人の略称。正式名称は「法人」の節。会話・ドキュメントでは略称を使う
- HelloDining: 飲食店向け事業の総称。AutoReserve と Respo
- AutoReserve / Respo / HelloX / HelloPay / RespoPay: 上記「事業」
- HelloAlpha: ヘッジファンド事業
- Hello Assistant（HA）: 汎用パーソナルアシスタント。社内の呼称。消費者向けのサービス名は Hello（2026-10-16）
- 運用部隊: AutoReserve・HelloX の電話オペレーションを担う 200人規模のチーム

参考リンク

- HP: https://hello.ai / 会社情報: https://hello.ai/ja/company / 採用: https://hello.ai/ja/careers
- Tech Blog: https://tech.hello.ai / note: https://note.com/helloinc/magazines / X: https://x.com/helloaiinc
