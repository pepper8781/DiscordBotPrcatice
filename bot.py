from discord.ext import commands
import discord
import config
import random
from openai import OpenAI
import sqlite3

dbname = 'TEST.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

openai_client = OpenAI(api_key=config.API_KEY)

intents = discord.Intents.all()
discord_client = discord.Client(intents=intents)

bot = commands.Bot(
    command_prefix="&",
    case_insensitive=True, 
    intents=intents
)

@bot.event
async def on_ready():
    print("準備完了！")

@bot.event
async def on_message(message):
    
    if message.author == discord_client.user:
        return
    
    if message.author.bot:
        return
    
    # await bot.process_commands(message)
    
    if message.content.startswith('&exp'):
            await message.channel.send('メンションして聞きたいことを書いてくれたら答えます。(コマンドを使う時はメンションしなくて大丈夫です) \n &reg: ユーザー登録をすることができます \n &check: 現在登録されているプロンプトを確認できます\n &pr: プロンプトの登録、更新ができます\n &del: ユーザー登録を削除することができます')
            return
    
    if message.content.startswith('&reg'):
            user_id_to_check = message.author.id
            cur.execute('SELECT * FROM users WHERE user_id = ?', (str(user_id_to_check),))
            result = cur.fetchone()
            if result:
                await message.reply('登録済みのアカウントです。')
                return
            else:
                cur.execute('''INSERT INTO users (user_id, prompt)
                          VALUES (?, ?)''', (message.author.id, ''))
                conn.commit()
                await message.reply( f'{message.author.mention}' + 'さん、登録完了！')
                return
    
    if message.content.startswith('&check'): 
            cur.execute('SELECT prompt FROM users WHERE user_id = ?',(str(message.author.id),))
            result = cur.fetchone()
            if result:
                reply = result[0] 
                if len(reply) == 0:
                    await message.reply("プロンプトが登録されていません。&pr の後にプロンプトを記述することで登録することができます")
                    return
                else:
                    await message.reply(f"現在のプロンプト：{reply} ")
                    return
            else:
                await message.reply("ユーザー情報がありません。&reg と打つことでユーザー登録ができます。")
                return
    
    if message.content.startswith('&pr'): 
            cur.execute('SELECT prompt FROM users WHERE user_id = ?',(str(message.author.id),))
            result = cur.fetchone()
            if result:
                modified_message = message.content.replace("&pr ", "")
                cur.execute('UPDATE users SET prompt = ? WHERE user_id = ?',(modified_message,str(message.author.id),))
                conn.commit()
                await message.reply("プロンプト登録完了！")
                return

            else:
                await message.reply("ユーザー情報がありません。&reg と打つことでユーザー登録ができます。")
                return
    
    if message.content.startswith('&del'): 
            cur.execute('SELECT prompt FROM users WHERE user_id = ?',(str(message.author.id),))
            result = cur.fetchone()
            if result:
                cur.execute('DELETE FROM users WHERE user_id = ?',(str(message.author.id),))
                conn.commit()
                await message.reply("データ削除完了、またね！")
                return
            else:
                await message.reply("ユーザー情報がありません。&reg と打つことでユーザー登録ができます。")
                return


    if bot.user in message.mentions:
        cur.execute('SELECT prompt FROM users WHERE user_id = ?',(str(message.author.id),))
        result = cur.fetchone()
        if result:
                sys_content = result[0] 
                prompt = message.content
                completion = openai_client.chat.completions.create(
                  model="gpt-4",
                  messages=[
                    {"role": "system", "content": sys_content},
                    {"role": "user", "content": prompt + '返答にユーザー名を含める必要はありません'}
                  ]
                )

                await message.reply( f'{message.author.mention}' + '' + completion.choices[0].message.content)
                return
        else:
                await message.reply("ユーザー情報がありません。&reg と打つことでユーザー登録ができます。")
                return
    # else:
    #     answer_list = ["ごろーん", "構ってよー！", "そわそわ..."]
    #     answer = random.choice(answer_list)
    #     await message.channel.send(answer)

@bot.event
async def on_close():
    conn.close()

bot.run(config.DISCORD_TOKEN)