import asyncio
import random
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.sessions import StringSession
from telethon.tl.functions.channels import InviteToChannelRequest

from creds import session, api_id, api_hash

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
    message_delay_time = 270

    # Send the random message to the target group
    random_message = random.choice(messages)
    try:
        await client.send_message(group, random_message)
    except PeerFloodError as e:
        print("Waiting for", e.seconds, "seconds due to flood...")
        await asyncio.sleep(e.seconds)

    # Wait for the delay time between messages
    await asyncio.sleep(message_delay_time)

# Define the main loop that sends messages to all groups indefinitely
async def main():
    # Set the delay time in seconds between sending messages to groups
    group_delay_time = 270
    
    while True:
        for group in groups:
            await send_message_with_delay_to_group(group)
            # Wait for the delay time between sending messages to groups
            await asyncio.sleep(group_delay_time)
        
        # After sending messages to all groups, start again from the first group
        print("Finished sending messages to all groups, starting again...")
        await asyncio.sleep(5)

# Run the main loop until interrupted
with client:
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Received interrupt signal, exiting...") 
