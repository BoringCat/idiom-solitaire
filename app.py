#!/usr/bin/env python3

import asyncio
import websockets
import random
from os import environ
from json import dumps
from 成语接龙 import 成语接龙

CLOSE_CODES = {
    1000: "OK",
    1001: "going away",
    1002: "protocol error",
    1003: "unsupported type",
    # 1004 is reserved
    1005: "no status code [internal]",
    1006: "connection closed abnormally [internal]",
    1007: "invalid data",
    1008: "policy violation",
    1009: "message too big",
    1010: "extension required",
    1011: "unexpected error",
    1015: "TLS failure [internal]",
}

async def cyjl(websocket:websockets.server.WebSocketServerProtocol, path):
    print(path)
    print(globals()['path'])
    if path != globals()['path']: 
        await websocket.close_connection()
        return 
    await websocket.send('选择模式')
    mode = await websocket.recv()
    if mode not in ['拼音', '文字']:
        await websocket.send('接龙模式 必须为\'拼音\' 或者 \'文字\'。')
        await websocket.close(1001, "mode error")
    jl = 成语接龙(4)
    jl.选择配置(mode)

    if random.random() >= 0.6:
        status, output, extra = jl.电脑开局()
        await websocket.send(dumps({'status': status, 'output':output, 'extra': extra},ensure_ascii=False))
    else:
        await websocket.send(dumps({'status': True, 'output':None, 'extra': None},ensure_ascii=False))
    
    while True:
        user_input = await websocket.recv()
        if not user_input:
            return
        status, output, extra = jl.接龙(user_input)
        await websocket.send(dumps({'status': status, 'output':output, 'extra': extra},ensure_ascii=False))
        if not status:
            await websocket.close(1000, "Finish")
            return

    await websocket.close(1011, "??????")

addr = environ.get('APP_LISTEN', 'localhost')
port = int(environ.get('APP_PORT', '8765'))
path = environ.get('APP_PATH', '/')

start_server = websockets.serve(cyjl, addr, port)

asyncio.get_event_loop().run_until_complete(start_server)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass