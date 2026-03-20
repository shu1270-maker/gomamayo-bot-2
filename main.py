import discord
import os
import re

# トークン読み込み
TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 精密判定ロジック：読みの重なりを重視
def is_gomamayo(text):
    # 1. 「うおおお」などの3回以上の同じ音の連続は無視（叫び声対策）
    if re.search(r'(.)\1\1', text):
        return False
    
    # 2. 助詞（を・が・は・に・も）が挟まっていたら無視
    if re.search(r'[をがはにも]', text):
        return False

    # 3. ひらがな・カタカナでの「音の重なり」だけを判定
    # 漢字の「日本本部長」などは読みが違うので、この条件で自動的にスルーされます。
    # 反応する例：「チョココロネ」「ねここねる」「ごまマヨ」
    kana_overlap = re.search(r'([\u3040-\u309F\u30A0-\u30FF])\1', text)
    
    if kana_overlap:
        return True
        
    return False

@client.event
async def on_ready():
    # Renderのログにこれが出ればオンライン成功！
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Bot自身の発言は無視
    if message.author.bot:
        return

    # ゴママヨ判定を実行
    if is_gomamayo(message.content):
        await message.channel.send("⁉️")

if TOKEN:
    client.run(TOKEN)
