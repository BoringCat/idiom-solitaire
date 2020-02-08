import requests
from os import mkdir, path, chdir
from json import dump as json_dump
chdir(path.dirname(path.abspath(__file__)))
try:
    idiom = requests.get('https://raw.githubusercontent.com/pwxcoo/chinese-xinhua/master/data/idiom.json').json()
    idneed = list(map(lambda x:{'pinyin':x['pinyin'],'word':x['word']},idiom))
    if not path.exists('datas'):
        mkdir('datas')
    else:
        if not path.isdir('datas'):
            raise EnvironmentError('datas不是一个文件夹')
    json_dump(idneed, open('datas/idneed.json','w',encoding='UTF-8'), ensure_ascii=False,separators=(',', ':'))
    print('更新成功')
except requests.exceptions.ConnectionError as identifier:
    print("更新失败，因为接不上github.com\n└───%s" % identifier.args[0].args[1])
    exit(1)
