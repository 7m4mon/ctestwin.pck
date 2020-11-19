# ctestwin.pck
Partial Check file for Ctestwin (Amateur Radio Contest Logging Software)

## 公開情報からパーシャルチェックリストを作成する

2020年現在、日本のアマチュア無線局数はおよそ40万局ですが、このうち、JARLの国内4大コンテスト（ALL JA, 6m & Down, Field Day, 全市全郡）に 2015-2019の5年間で書類を提出した局は、およそ6000局（7M4MON 調べ）です。  
コールサインのアルファベット・数字の組み合わせは膨大な数がありますが、コンテストに参加する局は、ほとんど上記の6000局のコールサインです。  
そのため、過去の交信履歴等からある程度の予測と省力化が可能です。  
コンテストロギングソフトでは、コールサインの一部を入力すると交信相手のコールサイン候補が表示されるパーシャルチェックという機能があります。  
パーシャルチェックではコールサインだけではなくコンテストナンバーの候補も表示されます。  
上記の国内4大コンテストのコンテストナンバーは RS(T) ＋ 運用地の都府県・北海道地域番号または市郡区番号＋空中線電力を表すアルファベット１文字です。  
総務省の無線免許状検索ではコールサインで検索すると常置場所の市区町村名まで分かりますので、コンテスト書類提出局のコールサインとつき合わせて、パーシャルチェックのデータベースを作成しました。

### 使い方
Ctestwin の「表示」メニューから「パーシャルチェック表示」を選択し、「新規読込するパーシャルチェックファイルを指定してください」のダイアログでダウンロードした ctestwin.pck を選択してください。

![](https://github.com/7m4mon/ctestwin.pck/blob/master/ctestwin.pck.png)

### 作り方
1. JARLのコンテスト結果「書類提出局全リスト」ページの内容をサクラエディタにコピペする。
1. キーマクロ `pickup_callsigns_from_contest_result_page.mac` をツール→マクロの読み込みして実行する。
1. (複数コンテスト処理時)  `sort_and_delete_dupe_callsign.py` でダブリを削除する。(ついでに並び替え)
1. `get_qth.py` で総務省データベースから住所を取得する。
1. `get_cgnum.py` で住所と市郡区番号を紐付けて ctestwin.pck を作成する。
1. (追記時) 1,2の手順を実施後、`pickup_uniq_callsign.py` でパーシャルチェックファイルにないコールサインを抽出し、4,5の手順を実行、3で並び替え

中身についての詳しい解説は、[別冊CQ ham radio QEX Japan No.37](https://shop.cqpub.co.jp/hanbai/books/MBC/MBC202012.html) をご参照ください。

