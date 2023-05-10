# NewBBQ

New Bing Bot for QQ

为 QQ 机器人添加 New Bing 聊天功能

## 依赖

- 新必应的逆向工程： [EdgeGPT](https://github.com/acheong08/EdgeGPT)
- cqhttp 的 go 实现，用于搭建 QQ 机器人： [go-cqhttp](https://github.com/acheong08/EdgeGPT)

## 安装及配置

按照 EdgeGPT 和 go-cqhttp 的文档安装和配置好它们。

从网上拉取 NewBBQ 的源码：

```console
$ git clone https://github.com/vaaandark/NewBBQ.git
$ cd NewBBQ
```

修改配置文件 `config.toml`：

```toml
# 接入 Bot 的群聊和私聊
[allowed]
group = [ 11, 22, 33 ]
private = [ 44, 55, 66 ]

# 对应 go-cqhttp 配置中的 servers.http.post.url
[bind]
address = "127.0.0.1"
port = 8888

# 对应 go-cqhttp 配置中的 servers.http.address
[cqhttp_api]
endpoint = "http://127.0.0.1:8889"

# 将 cookie 文件放入目标目录下
[cookies]
cookies_dir = "cookies.d"
```

将准备好的 bing.com 的 cookie 放到 cookie 目标目录 `cookies.d` 下

## 使用

启动 go-cqhttp 后再启动 bot ：

```console
$ cd NewBBQ
$ python bot.py # 配置文件默认为 config.toml
$ python bot.py {配置文件} # 如果需要指定配置文件
```

如果 QQ 帐号在 `allowed.private` 中，与 Bot 私聊，Bot 将会把所有收到的消息提交给 New Bing ，并返回 New Bing 的回答。

在群聊中与 bot 聊天需要以字母 `z` 加一个空格开头（无需 at ），以区分向 Bot 提问和普通聊天。

**值得注意的是，群聊中的每个用户的上下文是独立的，不用担心别人的消息对自己上下文的破坏。**
