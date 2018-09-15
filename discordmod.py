import threading
import discord
import asyncio
import re

from priv import token


class DiscordBot():
    client = discord.Client()

    def __init__(self):
        self.queue = asyncio.Queue()
        self.start()

    def start(self):
        self.discord_thread = threading.Thread(target=self.handle_discord)
        self.discord_thread.start()

    def handle_discord(self):
        self.client.loop.create_task(self.message_handler())
        self.client.run(token)

    @client.event
    async def on_message(message):
        print(message.content)

    async def message_handler(self):
        await self.client.wait_until_ready()
        channel = discord.Object(id='490192503597694986')
        while not self.client.is_closed:
            msg = await self.queue.get()
            await self.client.send_message(channel, msg)

    def handle(self, server, line):
        msg = re.search(r'<(.*)> (.*)$', line)
        if msg:
            # server.send_command('say {}'.format(msg.group(2)))
            self.queue.put_nowait('<{}> {}'.format(msg.group(1), msg.group(2)))
