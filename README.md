# 成语接龙

## 成语来源
[**成语词典 - Google Play 上的应用**](https://play.google.com/store/apps/details?id=com.qiushui.android.app.idiom)

## 本地使用方法
|服务端|客户端|
|:--:|:--:|
|`python app.py`| `python -m websockets ws://localhost:8765`|

## 部署方法
``` shell
$ export APP_LISTEN='::'
$ export APP_PORT='8765'
$ export APP_PATH='/'
$ python app.py
```

## Docker Compose
``` yaml
version: '2'
services:
  idiom-solitaire:
    build:
      context: .
      dockerfile: Dockerfile
    restart: unless-stopped
    environment:
      APP_LISTEN: '::'
      APP_PORT: 8765
      APP_PATH: '/'
    image: $(你喜欢)
    ports:
      - 127.0.0.1:8765:8765
    volumes:
      - ./datas:/app/datas
```

## English Version?
**What? This is Chinese idiom. :(**