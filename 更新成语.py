import requests
from json import dump as json_dump
try:
    idiom = requests.get('https://raw.githubusercontent.com/pwxcoo/chinese-xinhua/master/data/idiom.json').json()
    idneed = list(map(lambda x:{'pinyin':x['pinyin'],'word':x['word']},idiom))
    json_dump(idneed, open('idneed.json','w',encoding='UTF-8'), ensure_ascii=False,separators=(',', ':'))
    print('更新成功')
except requests.exceptions.ConnectionError as identifier:
    print("更新失败，因为接不上github.com\n└───%s" % identifier.args[0].args[1])
    exit(1)
