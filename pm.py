from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
from creds import session, api_id, api_hash

replied_chats = set()  # To keep track of already replied chats

with TelegramClient(StringSession(session), api_id, api_hash) as client:
    @client.on(events.NewMessage(incoming=True))
    async def auto_reply(event):
        sender = await event.get_sender()
        if event.is_private and not sender.bot and event.chat_id not in replied_chats:
            message = event.message.message.lower()
            reply = '''Hello, watch my vip videos only at 
            https://t.me/+1BLchlZjMQM5NGNl'''
            await event.reply(reply)
            replied_chats.add(event.chat_id)

    client.start()
    client.run_until_disconnected()
