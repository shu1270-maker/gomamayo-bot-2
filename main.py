import discord
import os
import re

# トークン（Environment Variablesから取得）
TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 精密判定ロジック：音の重なりだけを狙う
def is_gomamayo(text):
    # 1. 「うおおお」などの3回以上の同じ音の連続は無視
    if re.search(r'(.)\1\1', text):
        return False
    
    # 2. 助詞（を・が・は・に・も）が挟まっていたら無視
    if re.search(r'[をがはにも]', text):
        return False

    # 3. ひらがな・カタカナでの「音の重なり」だけを判定
    # 漢字の「日本本部長」などは読みが違うので無視されます
    kana_overlap = re.search(r'([\u3040-\u309F\u30A0-\u30FF])\1', text)
    
    return True if kana_overlap else False

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return
    # ゴママヨなら「⁉️」を返す
    if is_gomamayo(message.content):
        await message.channel.send("⁉️")

if TOKEN:
    client.run(TOKEN)
