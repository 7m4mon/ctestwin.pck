''' コールサインを総務省の無線局等情報検索Web-APIで検索 '''
''' 応答結果から無線局の設置場所取得してリストを作成する '''
''' 2020/8/8 7M4MON '''

import requests
import json
import time

wait_sec = 3     # 過負荷をかけないように。4878件で5時間半程度。

# res_txt = {"musen":[{"listInfo":{"name":"＊＊＊＊＊（7M4MON）","radioStationPurpose":"アマチュア業務用","tdfkCd":"東京都中央区","no":"1","licenseDate":"2018-04-02"}}],"musenInformation":{"totalCount":"1","lastUpdateDate":"2020-08-02"}}

def get_city(callsign):
    response = requests.get('https://www.tele.soumu.go.jp/musen/list?ST=1&OF=2&OW=AT&DA=0&DC=1&SC=1&MA=' + callsign)
    if response.status_code == 200:
        res_txt =response.text    # レスポンスのHTMLを文字列で取得
        if 'tdfkCd' in res_txt:   # 存在（廃局）チェック
            d = json.loads(res_txt)                     # Json形式の文字列をdictにパース
            city = d['musen'][0]['listInfo']['tdfkCd']  # tdfkCd キーの中身を取得 
            print(city)
        else :
            city = "N/A"
    else:
        city = ""
    return city
        
        
if __name__ == '__main__':
    fr = open('./uniq_callsigns.txt', 'r')      # Shift-JIS
    fw = open('./uniq_callsigns_qth.txt', 'a')
    
    line = fr.readline()
    while line:
        callsign = line.strip() # 改行の削除
        print(callsign)
        city_name = get_city(callsign)
        print(callsign + ',' + city_name , file=fw)
        time.sleep(wait_sec)
        line = fr.readline()
    fr.close()
    fw.close()
