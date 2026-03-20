import discord
from discord.ext import commands
import pykakasi
import os
from flask import Flask
from threading import Thread

# --- UptimeRobot用の設定 ---
app = Flask('')
@app.route('/')
def home(): return "Bot-2 is Alive!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# --- ゴママヨ判定ロジック ---
kks = pykakasi.kakasi()
def count_pure_gomamayo(text):
    result = kks.convert(text)
    valid_words = [item['hira'] for item in result if item['pos'] not in ['助詞', '助動詞', '記号', '接頭辞', '空白']]
    count = 0
    for i in range(len(valid_words) - 1):
        if valid_words[i] and valid_words[i+1]:
            if valid_words[i][-1] == valid_words[i+1][0]:
                count += 1
    return count

# --- Botの設定 ---
TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    count = count_pure_gomamayo(message.content)
    if count > 0:
        await message.channel.send('⁉️' * count)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
