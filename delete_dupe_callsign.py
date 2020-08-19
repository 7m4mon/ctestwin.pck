'''コールサインのリストをロードして、重複を削除して標準出力に出力する'''
'''2020/08/09 7M4MON'''

callsign_list = []
callsign_uniq = []

'''コールサインをリストにをロードする'''
fr = open('./allja_2019-2014_callsign.txt', 'r')

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

