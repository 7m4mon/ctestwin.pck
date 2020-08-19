'''4858件で1秒程度'''
'''市町村名から市郡コードを検索し、コールサインとくっつけて、CtestWinのパーシャルチェックファイル ctestwin.pck を作る'''
'''2020/08/06 7M4MON'''

import csv

cgnum_list = []

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

    cgnum_str = '99999'
    list_hit = False

    if 'N/A' in city_name:
        cgnum_str = '99998'
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
        country_name = 'NIL ' + city_name

    print(cgnum_str+ " " + country_name)
    return cgnum_str
    
        
'''最初に市郡コードをロードする'''
def load_cgnum_list():
    with open('./pref_acag.csv.txt','r',encoding="SHIFT-JIS") as f_in:
        reader = csv.reader(f_in)
        for row in reader:
            cgnum_list.append(row)
            

if __name__ == '__main__':
    fw = open('./ctestwin_j.pck', 'a')
    load_cgnum_list()
    with open('./uniq_callsigns_qth_j.txt','r',encoding="SHIFT-JIS") as f_in:
        reader = csv.reader(f_in)
        i = 0
        for row in reader:
            callsign = row[0]
            city_name = row[1]
            city_code = get_cgnum(city_name)
            print(str(i) + ' ' + callsign + ' ' + city_code + ' '+ city_name)   #途中経過確認用
            print(callsign + ' ' + city_code + ' '+ city_name , file=fw)
            i += 1
    fw.close()
    


