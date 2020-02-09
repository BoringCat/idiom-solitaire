#!/usr/bin/env python3

import asyncio
import websockets
import random
from os import environ
from json import dumps, dump
import signal
from datetime import datetime
from 成语接龙 import 成语接龙

def save_history(*args):
    global issave, maxlist
    if issave: return
    if not maxlist: return
    with open('datas/max_history_%s.json' % datetime.now().strftime('%Y-%m-%d_%H:%M:%S'), 'w', encoding='UTF-8') as f:
        dump(maxlist,f,ensure_ascii=False,separators=(',',':'))
        f.flush()
    issave = True

async def cyjl(websocket:websockets.server.WebSocketServerProtocol, path):
    global maxnum, maxlist
    if path != globals()['path']: 
        await websocket.close_connection()
        return 
    await websocket.send('选择模式')
    raw = (await websocket.recv()).split(',', maxsplit=1)
    if len(raw) == 2:
        mode, noyd = raw
    else:
        noyd = False
        mode = raw[0]
    noyd = noyd in [True, 'True', 'true']
    if mode not in ['拼音', '文字']:
        await websocket.send('接龙模式 必须为\'拼音\' 或者 \'文字\'。')
        await websocket.close(1001, "mode error")
    jl = 成语接龙(4, noyd)
    jl.选择配置(mode)
    num = 0
    userlist = []

    if random.random() >= 0.6:
        status, output, extra = jl.电脑开局()
        await websocket.send(dumps({'status': status, 'output':output, 'extra': extra},ensure_ascii=False))
        num += 1
        userlist.append(output)
    else:
        await websocket.send(dumps({'status': True, 'output':None, 'extra': None},ensure_ascii=False))

    while True:
        user_input = await websocket.recv()
        if not user_input:
            await websocket.close(1000, "Finish")
            if maxnum < num and num > 1:
                maxnum = num
                maxlist = userlist.copy()
            return
        status, output, extra = jl.接龙(user_input)
        await websocket.send(dumps({'status': status, 'output':output, 'extra': extra},ensure_ascii=False))
        if not status:
            if extra:
                num+=1
                userlist.append(user_input)
            await websocket.close(1000, "Finish")
            if maxnum < num and num > 1:
                maxnum = num
                maxlist = userlist.copy()
            return
        if user_input!=output:
            num += 2
            userlist.append(user_input)
            userlist.append(output)

    await websocket.close(1011, "??????")

signal.signal(signal.SIGTERM, save_history)

addr = environ.get('APP_LISTEN', 'localhost')
port = int(environ.get('APP_PORT', '8765'))
path = environ.get('APP_PATH', '/')
issave = False
maxlist = []
maxnum = 0

start_server = websockets.serve(cyjl, addr, port)

asyncio.get_event_loop().run_until_complete(start_server)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    save_history()