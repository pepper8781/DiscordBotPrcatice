from discord.ext import commands
import discord
import config
import random
from openai import OpenAI

openai_client = OpenAI(api_key=config.API_KEY)

intents = discord.Intents.all()
discord_client = discord.Client(intents=intents)

bot = commands.Bot(
    command_prefix="$", # $コマンド名　でコマンドを実行できるようになる
    case_insensitive=True, # コマンドの大文字小文字を区別しない ($hello も $Hello も同じ!)
    intents=intents # 権限を設定
)

@bot.event
async def on_ready():
    print("準備できたよー！")

@bot.event
async def on_message(message):
    # ボット自身のメッセージは無視する
    if message.author == discord_client.user:
        return
    
    # 他のボットのメッセージは無視する
    if message.author.bot:
        return

    # メンションされた場合の処理
    if bot.user in message.mentions:
        prompt = message.content
        completion = openai_client.chat.completions.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": "就活を手伝ってくれる優秀なアシスタントです。返信にユーザー名を含める必要はありません。"},
            {"role": "user", "content": prompt}
          ]
        )

        await message.reply( f'{message.author.mention}' + completion.choices[0].message.content)
    else:
        answer_list = ["何かお手伝いできることはありますか？", "何でも聞いてみてください！", "作業中..."]
        answer = random.choice(answer_list)
        await message.channel.send(answer)

bot.run(config.DISCORD_TOKEN)