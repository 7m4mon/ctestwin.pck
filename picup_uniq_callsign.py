'''コールサインのリストを既存のパーシャルチェックファイルと比較し、ユニークなコールサインを標準出力に出力する'''
'''処理時間：4558件vs4878件で2秒程度'''
'''2020/08/06 7M4MON'''

import csv

pck_list = []

def uniq_check(callsign):
    is_uniq = True
    for callsign_item in pck_list:
        if callsign in callsign_item[0]:
            is_uniq = False
            break
    return is_uniq
    
        
'''最初にPCKファイルをロードする'''
def load_pck_list():
    with open('./ctestwin.pck','r',encoding="SHIFT-JIS") as f_in:
        reader = csv.reader(f_in, delimiter=' ')
        for row in reader:
            pck_list.append(row)
            

if __name__ == '__main__':
    load_pck_list()
    fr = open('./callsignlist_6m_fd.txt', 'r')
    line = fr.readline()
    i = 0
    j = 0
    while line:
        callsign = line.strip() # 改行の削除
        # print (j)   #途中経過確認用
        # j += 1
        if uniq_check(callsign) :
            print (callsign)
            i += 1
        line = fr.readline()
    fr.close()
    print ("uniq_callsign:" + str(i))

