from aiohttp import web
import asyncio
import nb_api as api

msg_fifo = []
lock = asyncio.Lock()

allowed_group = api.allowed_group
allowed_private = api.allowed_private
address = api.address
port = api.port

async def handle(request):
  data = await request.json()
  # 如果不是消息则无视
  if data["post_type"] != "message":
    return web.Response(text="OK")

  uid = data["sender"]["user_id"]
  msg = data["raw_message"]
  msg_id = data["message_id"]

  # go-cqhttp 的 bug : 一个消息被多次收到
  # WORKAROUND: 如果消息处理过则无视
  global msg_fifo
  global lock
  async with lock:
    if msg_id in msg_fifo:
      print("Found repetition: ", msg_id)
      return web.Response(text="OK")
    else:
      msg_fifo.append(msg_id)
    if len(msg_fifo) > 100:
      msg_fifo.pop(0)

  # 私聊消息
  if data["message_type"] == "private":
    print("PRIVATE [{}] {} | {}".format(uid, msg_id, msg))
    if uid in allowed_private:
      await asyncio.gather(api.chat_private(uid, msg, msg_id))
  # 群聊消息
  elif data["message_type"] == "group":
    gid = data["group_id"]
    print("GROUP   [{}] {} | {}".format(gid, msg_id, msg))
    if gid in allowed_group:
      await asyncio.gather(api.chat_ingroup(gid, uid, msg, msg_id))

  return web.Response(text="OK")

app = web.Application()
app.add_routes([web.post('/', handle)])
web.run_app(app, host=address, port=port)
