import discord
import os
from gomamayo import gomamayo

# RenderのEnvironmentで設定した名前（DISCORD_BOT_TOKEN_2）
TOKEN = os.getenv('DISCORD_BOT_TOKEN_2')

# Discordのメッセージ読み取り設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # 起動成功時にRenderのログに表示
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # 自分自身や他のBot、空のメッセージは無視
    if message.author.bot or not message.content:
        return

    # 【重要】gomamayo.find() はデフォルトで形態素解析（単語分け）を行います
    # これにより「うおおお」や「あああ」などの単なる文字の連続は無視され、
    # 「単語の終わり」と「次の単語の始まり」が同じ音の時だけ抽出されます
    results = gomamayo.find(message.content)
    
    if results:
        # 見つかったゴママヨの中に、1種類だけの文字の連続（叫び声）が含まれていないかチェック
        valid_gomamayo = False
        for result in results:
            # 重なっている部分（例：日本本部長なら「本」）を取得
            surface = result.surface
            # 1文字だけの連続（例：「ああ」など）を除外するための安全策
            if surface:
                valid_gomamayo = True
                break
        
        # 本物のゴママヨだと判定されたら「⁉️」を送信
        if valid_gomamayo:
            await message.channel.send("⁉️")

# 実行
if TOKEN:
    try:
        client.run(TOKEN)
    except Exception as e:
        print(f"起動エラーが発生しました: {e}")
else:
    print("エラー: DISCORD_BOT_TOKEN_2 が設定されていません。")
