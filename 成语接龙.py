from json import load as 加载配置
from random import choice as 随机选择
from sys import argv as 外部输入

class 成语接龙():
    def __init__(self, length = None):
        try:
            self.成语字典 = 加载配置(open('datas/idneed.json','r',encoding='UTF-8'))
        except FileNotFoundError as e:
            raise FileNotFoundError('找不到成语字典，请使用"更新成语.py"获取最新成语字典', *e.args)
        self.程序输出 = ''
        self.头部字典 = {}
        self.尾部字典 = {}
        self.length = length
        self.接龙 = lambda 用户输入: (False, "接个屁啊，你还没选择模式", None)

    def _拼音接龙(self, 用户输入):
        if not self.尾部字典.get(用户输入,None):
            return False, '%s不是一个成语' % 用户输入, None
        用户拼音头, 用户拼音尾 = self.尾部字典.get(用户输入)
        _, 程序拼音尾 = self.尾部字典.get(self.程序输出,[None,None])
        if self.程序输出 and 程序拼音尾 != 用户拼音头:
            return False, '"%s"接不上"%s"呢（%s—>%s）' % (用户输入, self.程序输出, 程序拼音尾, 用户拼音头), None
        可接列表 = self.头部字典.get(用户拼音尾,[])
        if not 可接列表:
            return False, '卧槽(＃°Д°)我居然接不上来？？！！！', True
        self.程序输出 = 随机选择(可接列表)
        return True, self.程序输出, None if bool(self.头部字典.get(self.尾部字典[self.程序输出][-1], None)) else "\n我觉得你接不上来:)"

    def _文字接龙(self, 用户输入):
        结尾 = self.尾部字典.get(用户输入, None)
        if not 结尾:
            return False, '%s不是一个成语' % 用户输入, None
        if self.程序输出 and self.程序输出[-1] != 用户输入[0]:
            return False, '"%s"接不上"%s"呢（%s—>%s）' % (用户输入, self.程序输出, self.程序输出[-1], 用户输入[0]), None
        self.程序输出 = 随机选择(self.头部字典.get(结尾, [None]))
        if not self.程序输出:
            return False, '卧槽(＃°Д°)我居然接不上来？？！！！', True
        return True, self.程序输出, (None if self.头部字典.get(self.程序输出[-1], None) else "\n我觉得你接不上来:)")

    def 电脑开局(self):
        self.程序输出 = 随机选择(self.成语字典)['word']
        if self.接龙 == self._文字接龙:
            return True, self.程序输出 , (None if self.头部字典.get(self.程序输出[-1], None) else "\n我觉得你接不上来:)")
        elif self.接龙 == self._拼音接龙:
            return True, self.程序输出 , (None if self.头部字典.get(self.尾部字典[self.程序输出][-1], None) else "\n我觉得你接不上来:)")

    def 选择配置(self, 接龙模式):
        if 接龙模式 == '文字':
            self.头部字典 = {}
            for 成语 in self.成语字典:
                if self.length:
                    if len(成语['word']) != self.length: continue
                列表 = self.头部字典.get(成语['word'][0],[])
                列表.append(成语['word'])
                self.头部字典[成语['word'][0]] = 列表
            self.尾部字典 = dict(
                filter(
                    lambda x:bool(x),
                    map(
                        lambda 成语: (成语['word'],成语['word'][-1]) if not self.length or len(成语['word']) == self.length else None,
                        self.成语字典
                    )
                )
            )
            self.接龙 = self._文字接龙
        elif 接龙模式 == '拼音':
            self.头部字典 = {}
            for 成语 in self.成语字典:
                if self.length:
                    if len(成语['word']) != self.length: continue
                拼音 = 成语['pinyin'].split()[0]
                列表 = self.头部字典.get(拼音,[])
                列表.append(成语['word'])
                self.头部字典[拼音] = 列表
            self.尾部字典 = dict(
                filter(
                    lambda x:bool(x),
                    map(
                        lambda 成语: (成语['word'],[成语['pinyin'].split()[0],成语['pinyin'].split()[-1]])if not self.length or len(成语['word']) == self.length else None, 
                        self.成语字典
                    )
                )
            )
            self.接龙 = self._拼音接龙
        else:
            raise ValueError('接龙模式 必须为\'拼音\' 或者 \'文字\'。')

if __name__ == "__main__":
    try:
        模式 = 外部输入[1] if len(外部输入) >= 2 else None
        接龙 = 成语接龙()
        接龙.选择配置(模式 if 模式 else input('选择接龙模式(拼音/文字): '))
        while True:
            status, output, extra = 接龙.接龙(input('输入你的成语: '))
            if status:
                print('我接:', output)
                print(extra) if extra else None
            else:
                print(output)
                print(extra) if extra else None
                raise KeyboardInterrupt()
    except KeyboardInterrupt:
        pass
    except ValueError as ve:
        print('ValueError:',ve)
        print('食用方法: python3 成语接龙.py [接龙模式]')