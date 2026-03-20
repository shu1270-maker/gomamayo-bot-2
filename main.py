import discord
import os
import re

TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def is_gomamayo(text):
    if re.search(r'(.)\1\1', text):
        return False
    if re.search(r'[をがはにも]', text):
        return False
    # ひらがな・カタカナの音の重なりだけを判定
    match = re.search(r'([\u3040-\u309F\u30A0-\u30FF])\1', text)
    return True if match else False

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if is_gomamayo(message.content):
        await message.channel.send("⁉️")

if TOKEN:
    client.run(TOKEN)
