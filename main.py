import asyncio
import random
from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.sessions import StringSession
from creds import session, api_id, api_hash

replied_chats = set()  # To keep track of already replied chats

# Create a client instance using the string session
client = TelegramClient(StringSession(session), int(api_id), api_hash)

# Start the client
client.start()

# Create a list of groups from the groups.txt file
with open('groups.txt', 'r') as f:
    groups = [line.strip() for line in f if line.strip()]

# Create a list of messages from the texts.txt file
with open('texts.txt', 'r') as f:
    messages = [line.strip() for line in f if line.strip()]

# Define the send_message function with a time delay and a random message
async def send_message_with_delay_to_group(group):
    # Set the delay time in seconds between messages
    message_delay_time = 5

    # Send the random message to the target group
    random_message = random.choice(messages)
    try:
        await client.send_message(group, random_message)
    except PeerFloodError as e:
        print("Waiting for", e.seconds, "seconds due to flood...")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print("Error occurred:", e)

    # Wait for the delay time between messages
    await asyncio.sleep(message_delay_time)

# Define the auto_reply function to automatically reply to incoming messages
async def auto_reply(event):
    sender = await event.get_sender()
    if event.is_private and not sender.bot and event.chat_id not in replied_chats:
        message = event.message.message.lower()
        reply = '''Hello, watch my vip videos only at 
        https://t.me/+1BLchlZjMQM5NGNl'''
        await event.reply(reply)
        replied_chats.add(event.chat_id)

# Define the main loop that sends messages to all groups indefinitely
async def main():
    # Set the delay time in seconds between sending messages to groups
    group_delay_time = 1
    
    while True:
        for group in groups:
            await send_message_with_delay_to_group(group)
            # Wait for the delay time between sending messages to groups
            await asyncio.sleep(group_delay_time)
        
        # After sending messages to all groups, start again from the first group
        print("Finished sending messages to all groups, starting again...")
        await asyncio.sleep(5)

# Run the main loop and auto_reply concurrently until interrupted
try:
    asyncio.ensure_future(main())
    client.add_event_handler(auto_reply, events.NewMessage(incoming=True))
    client.run_until_disconnected()
except KeyboardInterrupt:
    print("Received interrupt signal, exiting...")
