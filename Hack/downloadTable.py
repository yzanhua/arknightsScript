import json
# import requests


# url = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
# r = requests.get(url, allow_redirects=True)

# with open('character_table.json', 'wb') as file:
#     file.write(r.content)

a = json.loads(open('./character_table.json', 'r', encoding='UTF-8').read())
# print(a["char_485_pallas"])