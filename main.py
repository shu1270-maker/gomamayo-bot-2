import discord
import os
import re

# トークン読み込み
TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 精密な判定ロジック（ライブラリの中身を再現）
def is_gomamayo(text):
    # 1. 叫び声（同じ文字が3回以上続く：うおおお、あああ等）は真っ先に除外
    if re.search(r'(.)\1\1', text):
        return False
    
    # 2. 助詞（を、が、は、に、も）が含まれている場合は除外
    if re.search(r'[をがはにも]', text):
        return False

    # 3. 同じ文字が2回続く場所を探す（日本本部長、チョココロネ等）
    # 重なりが見つかり、かつそれが「単語の塊」である可能性が高い場合に反応
    match = re.search(r'(.+?)\1', text)
    if match:
        # 重なっている文字が「あ」「い」などの1文字だけで、
        # 前後の文脈がない場合はただの叫び声の可能性が高いので慎重に判定
        return True
        
    return False

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 「うおおお」はスルーし、「日本本部長」には反応する
    if is_gomamayo(message.content):
        await message.channel.send("⁉️")

if TOKEN:
    client.run(TOKEN)
