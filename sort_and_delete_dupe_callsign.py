'''コールサインのリストをロードして、重複を削除して標準出力に出力して保存する'''
'''2020/08/09 初版 7M4MON'''
'''2024/01/17 保存処理の追加 7M4MON'''

callsign_list = []
callsign_uniq = []

'''リストをダンプして保存'''
def dump_list(the_list, filename):
    f = open(filename, 'w')
    for x in the_list:
        f.write(str(x) + "\n")
    f.close()

'''コールサインやパーシャルチェックファイルをリストにをロードする'''
fr = open('./ctestwin_20240117.pck', 'r')

# １行ずつ読み取ってリストに保存
line = fr.readline()
while line:
    callsign = line.strip() # 改行の削除
    callsign_list.append(callsign)
    line = fr.readline()
fr.close()

callsign_uniq = list(set(callsign_list))    # 重複を削除
callsign_uniq.sort()                        # 並び替え
for callsign in callsign_uniq:
    print(callsign)
dump_list(callsign_uniq, "./uniq.pck")
