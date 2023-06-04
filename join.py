import asyncio
import time
import random
from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import PeerFloodError, FloodWaitError
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import JoinChannelRequest

from creds import session, api_id, api_hash

# Create a client instance using the string session
client = TelegramClient(StringSession(session), int(api_id), api_hash)

# Start the client
client.start()

# Create empty list to store successfully joined groups
joined_groups = []

# Create a list of groups from the groups.txt file
with open('groups.txt', 'r') as f:
    groups = [line.strip() for line in f if line.strip()]

# Define join_group that will join given group name and skips if already joined
async def join_group(group):
    global joined_groups

    if group in joined_groups:
        # If group is already joined, skip it and move on to the next group
        return

    try:
        await client(JoinChannelRequest(group))
        print(f'{group} Joined!')
        # Add the successfully joined group to the list
        joined_groups.append(group)
        # Wait for the delay time between joining groups
        await asyncio.sleep(2500)
    except FloodWaitError as e:
        # Wait for the flood wait time and retry joining the same group
        print(f'Joining {group} failed due to flooding. Waiting for {e.seconds} seconds...')
        await asyncio.sleep(e.seconds)
        await join_group(group)
    except SessionPasswordNeededError:
        # Catch SessionPasswordNeededError exception and prompt for the two-factor authentication password
        print(f'Two-factor authentication is enabled for {group}. Please enter the password')
        password = input("Enter the two-factor authentication password: ")
        await client(JoinChannelRequest(group, password=password))
        print(f'{group} Joined!')
        # Add the successfully joined group to the list
        joined_groups.append(group)
        # Wait for the delay time between joining groups
        await asyncio.sleep(2500)
    except Exception as e:
        # Catch all other exceptions and print the error message
        print(f'Error joining {group}. Details: {e}')

# Define the main loop that joins all groups in the list
async def main():
    for group in groups:
        await join_group(group)

# Run the main loop until interrupted
with client:
    client.loop.run_until_complete(main())