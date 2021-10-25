'''
公開情報からパーシャルチェックリストを作成する

updaet_ctestwin_pck.py
2021.Oct.25 7M4MON

2020年現在、日本のアマチュア無線局数はおよそ40万局ですが、
このうち、JARLの国内4大コンテストに 2015-2019の5年間で書類を提出した局は、
およそ6000局（7M4MON 調べ）です。
コールサインのアルファベット・数字の組み合わせは膨大な数がありますが、
コンテストに参加する局は、ほとんど上記の6000局のコールサインです。
そのため、過去の交信履歴等からある程度の予測と省力化が可能です。
コンテストロギングソフトでは、コールサインの一部を入力すると
交信相手のコールサイン候補が表示されるパーシャルチェックという機能があります。
パーシャルチェックではコールサインだけではなくコンテストナンバーの候補も表示されます。
上記の国内4大コンテストのコンテストナンバーは RS(T) ＋ 運用地の都府県・北海道地域番号または
市郡区番号＋空中線電力を表すアルファベット１文字です。
総務省の無線免許状検索ではコールサインで検索すると常置場所の市区町村名まで分かりますので、
コンテスト書類提出局のコールサインとつき合わせて、パーシャルチェックのデータベースを作成しました。

* プログラムの流れ
1.コンテストの結果ページを読み込んで、コールサインを抜き出す
2.既存の ctestwin.pck を読み込んで、コールサインを抜き出す
3. 1と2を結合し、重複を削除し、ソートする
4.総務省の免許状検索データベースから常置場所を取得する
5.常置場所の市町村名から市郡区番号を取得する
6. 3と4と5を結合して、ctestwin.pckを作成

以前は新規参加局を追記していくスタイルでしたが、時間経過とともに
廃局されたり常置場所を変更されたりする局が増えてきますので、
全てのコールサインを再検索して、最新の常置場所に置き換えるとともに
免許状検索に登録されていない局はリストから削除する方針に変更しました。
'''

contest_result_url = "https://www.jarl.org/Japanese/1_Tanoshimo/1-1_Contest/all_ja/2021/entry.html"
read_pck_filename = "./ctestwin_20210416.pck"       # 前回作成したパーシャルチェックファイル名
write_pck_filename = "./ctestwin_20211024.pck"      # 今回作成するパーシャルチェックファイル名
new_callsign_filename = "./2021_allja_new.txt"      # 今回のコンテストの新規参加局
read_acag_filename = './pref_acag.csv.txt'          # 市町村郡名とコードの対照表（.csvだとExcelで開いたときに先頭の 0 が消えるのを嫌って .txtにしてある)
wait_sec = 3                                        # 過負荷をかけないようにするための、1件あたりのウェイト時間。3のとき4878件で5時間半程度。

import requests, re, json, time, csv, datetime

'''コールサイン抜き出し用正規表現'''
cs_re = '[J|7][A-S][0-9][A-Z]+? '           # Jまたは7で始まり、2文字目がAからSのアルファベット、3文字目が数字、4文字目からアルファベットが続き、末尾にデリミタの半角スペース
#cs_re = ' (J[A-S][0-9]|[7-8])[A-Z]+? '     #サクラエディタではOKだがpythonだとだめ
#cs_re = ' (J[A-S][0-9][A-Z]+?|[7-8][A-Z]+?) '

'''コンテストの結果ページからコールサインを抜き出す（末尾に半角スペースあり）'''
def read_callsign_resultpage(url):
    res = requests.get(url)
    callsign_list = re.findall(cs_re,res.text)
    return callsign_list

'''過去の ctestwin.pck からコールサインを抜き出す（末尾に半角スペースあり）'''
def read_callsign_pckfile(pck_filename):
    pckfile = open(pck_filename, 'r')
    pckstr = pckfile.read()
    pckfile.close()
    callsign_list_pck = re.findall(cs_re,pckstr)
    return callsign_list_pck

'''コンテストの参加局で過去のデータベースに登録のない局を抜き出す'''
def pickup_new_cs(test_cs, pck_cs):
    new_cs = []
    for cs in test_cs:
        if (cs in pck_cs) == False :
            new_cs.append(cs)
    return new_cs

'''リストをダンプして保存'''
def dump_list(the_list, filename):
    f = open(filename, 'w')
    for x in the_list:
        f.write(str(x) + "\n")
    f.close()

''' コールサインを総務省の無線局等情報検索Web-APIで検索 '''
''' 応答結果から無線局の設置場所取得して市町村名を返す '''
''' get_qth.py から移植'''
# res_txt = {"musen":[{"listInfo":{"name":"＊＊＊＊＊（7M4MON）","radioStationPurpose":"アマチュア業務用","tdfkCd":"東京都中央区","no":"1","licenseDate":"2018-04-02"}}],"musenInformation":{"totalCount":"1","lastUpdateDate":"2020-08-02"}}
def get_city(callsign):
    response = requests.get('https://www.tele.soumu.go.jp/musen/list?ST=1&OF=2&OW=AT&DA=0&DC=1&SC=1&MA=' + callsign)
    city = ""
    if response.status_code == 200:
        res_txt =response.text    # レスポンスのHTMLを文字列で取得
        if 'tdfkCd' in res_txt:   # 存在（廃局）チェック
            d = json.loads(res_txt)                     # Json形式の文字列をdictにパース
            city = d['musen'][0]['listInfo']['tdfkCd']  # tdfkCd キーの中身を取得 
            print(city)
        else :
            pass    #コールサインがデータベースにない
    else:
        pass        #サーバー応答なし
    return city


'''市町村名から市郡コードを返す'''
'''get_cgnum.py から移植'''
cgnum_list = [] # 町村郡名とコードの対照表を保持しておくリスト
# 北海道のダブリ郡の例外処理。コードが後の郡の町名だったらコードを直す。
hokkaido_dupe_code = ['01006','01014','01022','01042','01045','01050','01073']  # 先にあるコードのリスト
abuta_iburi = ['豊浦町','洞爺湖町']
uryu_kamikawa = ['幌加内町']    #例外中の例外
kamikawa_kamikawa = ['鷹栖町','東神楽町','当麻町','比布町','愛別町','上川町','東川町','美瑛町','和寒町','剣淵町','下川町']
sorachi_kamikawa = ['上富良野町','中富良野町','南富良野町']
teshio_souya = ['豊富町','幌延町']
nakagawa_tokachi = ['幕別町','池田町','豊頃町','本別町']
yuufutsu_kamikawa = ['占冠村']
hokkaido_dupe_towns = [abuta_iburi, uryu_kamikawa,kamikawa_kamikawa,sorachi_kamikawa,teshio_souya,nakagawa_tokachi,yuufutsu_kamikawa]
hokkaido_dupe_county = ['北海道虻田郡(胆振)','北海道雨竜郡(上川)','北海道上川郡(上川)','北海道空知郡(上川)','北海道天塩郡(宗谷)','北海道中川郡(十勝)','北海道勇払郡(上川)']

def get_cgnum(city_name):
    # 町村名は不要なので〇〇郡までを抜き出す。
    if '郡' in city_name:   # 愛知県蒲郡市, 福岡県小郡市, 奈良県大和郡山市, 福島県郡山市も含まれてしまうが削っても被らないので問題なし
        full_city_name = city_name  #バックアップ
        city_name = full_city_name[0:city_name.find('郡') + 1]  # 前方から検索
        town_name = full_city_name[city_name.find('郡') + 1:]  
        print (town_name)

    cgnum_str = ""
    list_hit = False

    # 郡市区名を探す
    for cg_item in cgnum_list:
        if city_name in cg_item[1]:
            list_hit = True
            break

    if list_hit == True:    # （表記ゆれや合併などで名前が変わってなければ）必ずあるはず
        cgnum_str = cg_item[0]
        country_name = cg_item[1]
        '''北海道のダブリ郡を処理する'''
        if cgnum_str in hokkaido_dupe_code :
            print('dupe code:' + country_name)
            dupe_index = hokkaido_dupe_code.index(cgnum_str)
            if town_name in hokkaido_dupe_towns[dupe_index] :   #例外の町がある
                country_name = hokkaido_dupe_county[dupe_index]
                print('北海道の例外')
                if dupe_index == 1 : # 例外中の例外 北海道雨竜郡(上川)幌加内町
                    cgnum_str = '01081'
                    print ('中の例外 北海道雨竜郡(上川)幌加内町')
                else: 
                    cgnum_str = str(int(cgnum_str) + 1).zfill(5) # 幌加内町以外は＋１すれば良い
    else:   #not in list
        pass

    print(cgnum_str + '\n')
    return cgnum_str
    

'''処理開始時に市郡コードを cgnum_list[] にロードしておく'''
def load_cgnum_list():
    with open(read_acag_filename,'r',encoding="SHIFT-JIS") as f_in:
        reader = csv.reader(f_in)
        for row in reader:
            cgnum_list.append(row)
            

'''メインの処理'''
if __name__ == '__main__':
    start_date = datetime.datetime.now()
    cs_list = read_callsign_resultpage(contest_result_url)
    cs_list.sort()
    print("対象局数: " + str(len(cs_list)))
    cs_list_pck = read_callsign_pckfile(read_pck_filename)
    print("既登録局数: " + str(len(cs_list_pck)))
    cs_new = pickup_new_cs(cs_list, cs_list_pck)
    print("新規局数: " + str(len(cs_new)))
    dump_list(cs_new, new_callsign_filename)
    cs_list.extend(cs_list_pck)
    dup = [x for x in set(cs_list) if cs_list.count(x) > 1]
    print("重複局数: " + str(len(dup)))
    uniq_cs_list = list(set(cs_list))       #重複を削除
    uniq_cs_list.sort()
    print("実行件数: " + str(len(uniq_cs_list)))
    fw = open(write_pck_filename, 'a')
    load_cgnum_list()
    i = 0
    qrt = 0
    no_cgnum = 0
    for cs in uniq_cs_list:
        callsign = cs.strip()   #改行やスペースの削除
        print(str(i) + " " + callsign)
        city_name = get_city(callsign)
        if city_name != "" :
            cgnum_str = get_cgnum(city_name)
            print(callsign + ' ' + cgnum_str + ' '+ city_name , file=fw)
            if cgnum_str == "" :
                no_cgnum += 1   #表記ゆれや合併などで市町村名が変わっている
        else:
            qrt += 1            #廃局などでコールサインが総務省のデータベースにない
        time.sleep(wait_sec)    #総務省のデータベースに過負荷をかけないようにちょっと待つ
        i += 1
    print('IDX:' + str(i) + ' QRT:' + str(qrt) + ' NIL:'+ str(no_cgnum) , file=fw)    #最後に結果を追記
    fw.close()
    stop_date = datetime.datetime.now()
    print('処理時間: '+ str(stop_date - start_date ))
