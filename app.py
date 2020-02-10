#!/usr/bin/env python3

import asyncio
import websockets
import random
from os import environ
from json import dumps, loads
from datetime import datetime
from 成语接龙 import 成语接龙

def disconnect(msg):
    return dumps({
        'action': "disconnect",
        'msg': msg
    },ensure_ascii=False,separators=(',',':'))

def connect(youfirst, output, extra):
    return dumps({
        'action': "connect",
        'youfirst': youfirst,
        'output': output,
        'extra': extra
    },ensure_ascii=False,separators=(',',':'))

def msg(status, output, extra):
    return dumps({
        'action': "msg",
        'status': status,
        'output': output,
        'extra': extra
    },ensure_ascii=False,separators=(',',':'))

def finish(youwin, output):
    return dumps({
        'action': "finish",
        'status': youwin,
        'output': output
    },ensure_ascii=False,separators=(',',':'))


async def cyjl(websocket:websockets.server.WebSocketServerProtocol, path):
    global maxnum, maxlist
    if path != globals()['path']: 
        await websocket.close_connection()
        return 
    await websocket.send(dumps({
        'action': 'init'
    }))
    try:
        initdict = loads(await websocket.recv())
    except Exception:
        await websocket.send(disconnect('出错'))
        await websocket.close(1001, "error")
        return
    if initdict.get('action') != "connect":
        await websocket.send(disconnect('数据异常'))
        await websocket.close(1001, "action error")
        return
    user_mode = initdict.get('mode', None)
    user_length = initdict.get('length', 0)
    user_noyd = initdict.get('noyd', False)
    try:
        if user_mode not in ['拼音', '文字']:
            await websocket.send(disconnect("接龙模式 必须为'拼音'或者'文字'。"))
            await websocket.close(1001, "mode error")
            return
        lenlimit = int(user_length)
        if lenlimit<0 or lenlimit>8:
            await websocket.send(disconnect("长度限制出错"))
            await websocket.close(1001, "limit error")
            return
        noyd = user_noyd in [True, 'True', 'true']
        del user_noyd, user_length
    except Exception:
        await websocket.send(disconnect('数据异常'))
        await websocket.close(1001, "action error")
        return

    jl = 成语接龙(lenlimit, noyd)
    jl.选择配置(user_mode)
    del lenlimit, noyd, user_mode

    if random.random() >= 0.6:
        status, output, extra = jl.电脑开局()
        await websocket.send(connect(False, output, extra))
    else:
        await websocket.send(connect(True, None, None))

    while True:
        user_input = await websocket.recv()
        if not user_input:
            await websocket.send(finish(False, "请输入一个成语"))
            await websocket.close(1000, "Finish")
            return
        status, output, extra = jl.接龙(user_input)
        if status:
            await websocket.send(msg(status, output, extra))
        else:
            await websocket.send(finish(extra in [True,'true','True'], output))
            await websocket.close(1000, "Finish")
            return

    await websocket.close(1011, "??????")

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
    pass