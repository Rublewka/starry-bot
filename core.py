# setup
import discord
import json
import os, os.path
import sys
import asyncio
import random
import http.client, urllib.request, urllib.parse, urllib.error, time
from discord.ext import commands, tasks
from config import settings
from misc import channelsids
prefix = settings['PREFIX']
client = commands.Bot(command_prefix = commands.when_mentioned_or(settings['PREFIX']), intents=discord.Intents.all())
client.remove_command('help') 
# setup end

#startup
@client.event
async def on_ready(): 

    print (f"[Logs:startup] Logged on as ") # startup message in console
    print ("""
╔═══╗    ╔╗  ╔╗           ╔╗           ╔══╗ ╔═══╗╔════╗
║╔═╗║    ║║  ║║           ║║           ║╔╗║ ║╔═╗║║╔╗╔╗║
║╚═╝║╔╗╔╗║╚═╗║║ ╔══╗╔╗╔╗╔╗║║╔╗╔══╗     ║╚╝╚╗║║ ║║╚╝║║╚╝
║╔╗╔╝║║║║║╔╗║║║ ║╔╗║║╚╝╚╝║║╚╝╝╚ ╗║     ║╔═╗║║║ ║║  ║║  
║║║╚╗║╚╝║║╚╝║║╚╗║║═╣╚╗╔╗╔╝║╔╗╗║╚╝╚╗    ║╚═╝║║╚═╝║ ╔╝╚╗ 
╚╝╚═╝╚══╝╚══╝╚═╝╚══╝ ╚╝╚╝ ╚╝╚╝╚═══╝    ╚═══╝╚═══╝ ╚══╝ 
   """)
    print("[Logs:startup] ____=====INFO=====____")
    print(f"[Logs:startup] Bot Info: {settings['NAME BOT']}")
    print(f"[Logs:startup] Bot ID: {settings['ID']}")
    rbs = client.get_channel(1076240177032351765)
    await rbs.send(f"""
@everyone        
Successfull restart!
        """) # startup message in status channel
    print (f"[Logs:startup] Successfully sent message to Rublewka Bot Status channel")
    print ("[Logs:startup] Bot start success")
    print ("[Logs:startup] ____=====INFO=====____")
    
#    await client.change_presence(activity=discord.Game(name="with TheSkout | ;help")) # presence
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Rublewka | ;help")) # presence
#    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Apple Music | ;help")) # presence


# startup end

# status
#async def st_sw():
#    await client.wait_until_ready()

#    statuses = ["with TheSkout | ;help", "Rublewka | ;help", "Apple Music | ;help"]

#    while not client.is_closed():
#        status = random.choice(statuses)
#        await client.change_presence(activity=discord.Game(name=status))
#        await asyncio.sleep(15)
# variables section


#prohibitedwords_path = '/home/container/prohibitednames.txt'
#prohibitedwords = open(prohibitedwords_path, 'r')

#bad_words = [prohibitedwords.read()]
# _______
# metrics
api_key = 'd5c8f50a-7e74-421e-a5ad-d62ed8d3ebdb'
page_id = '1423jz25bbfm'
metric_id = 'w3bdmlxfy40f'
api_base = 'https://api.statuspage.io/v1'
# metrics end
# ___________
# colors
default = 0
teal = 0x1abc9c
dark_teal = 0x11806a
green = 0x2ecc71
dark_green = 0x1f8b4c
blue = 0x3498db
dark_blue = 0x206694
purple = 0x9b59b6
dark_purple = 0x71368a
magenta = 0xe91e63
dark_magenta = 0xad1457
gold = 0xf1c40f
dark_gold = 0xc27c0e
orange = 0xe67e22
dark_orange = 0xa84300
red = 0xe74c3c
dark_red = 0x992d22
lighter_grey = 0x95a5a6
dark_grey = 0x607d8b
light_grey = 0x979c9f
darker_grey = 0x546e7a
blurple = 0x7289da
greyple = 0x99aab5

# ___________
# variables section end

# Ping
@client.command(aliases = ['Ping', 'PING', 'pING', 'ping', ' ping', ' PING', ' pING', ' Ping'])
async def __ping(ctx): 
    ping = client.ws.latency # Получаем пинг клиента

    ping_emoji = '🟩🔳🔳🔳🔳' # Эмоция пинга, если он меньше 100ms

    if ping > 0.15000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' # Эмоция пинга, если он больше 150ms

    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' # Эмоция пинга, если он больше 200ms

    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' # Эмоция пинга, если он больше 250ms

    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩' # Эмоция пинга, если он больше 300ms

    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧' # Эмоция пинга, если он больше 350ms

    if ping > 0.40000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' # Эмоция пинга, если он больше 400ms

    message = await ctx.reply('Пожалуйста, подождите. . .') # Переменная message с первоначальным сообщением
    await message.edit(content = f'Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:') # Редактирование первого сообщения на итоговое (На сам пинг)
    print(f'[Logs:utils] Пинг сервера был выведен | {prefix}ping') # Информация в консоль, что команда "ping" была использована
    print(f'[Logs:utils] На данный момент пинг == {ping * 1000:.0f}ms | {prefix}ping') # Вывод пинга в консоль
    # Ping end

# statuspage.io
# metrics
# need at least 1 data point for every 5 minutes
# submit random data for the whole day
# need 1 data point every 5 minutes
# submit random data for the whole day
import httplib, urllib, time, random, json

# the following 4 are the actual values that pertain to your account and this specific metric
# need 1 data point every 5 minutes
# submit random data for the whole day
total_points = (60 / 5 * 24)
for i in range(total_points):
  ts = int(time.time()) - (i * 5 * 60)
  value = random.randint(0, 99)
  params = json.dumps({
      "data": {
          "timestamp": ts,
          "value": value
      }
  })
  headers = {"Content-Type": "application/json", "Authorization": "OAuth " + api_key}

  conn = httplib.HTTPSConnection(api_base)
  conn.request("POST", "/pages/" + page_id + "/metrics/" + metric_id + "/data.json", params, headers)
  response = conn.getresponse()

  if (response.status >= 400):
    print f"Error encountered. Please ensure that your page code and authorization key are correct."
    print(response.read())
    break
  else:
    print "Submitted point " + str(i + 1) + " of " + str(total_points)
    time.sleep(1)

# metrics end
# statuspage.ip end
# voice channels


# Help
@client.command(aliases = ['Help', 'help', 'HELP', 'hELP', 'хелп', 'Хелп', 'ХЕЛП', 'хЕЛП'])
async def __help (ctx):
    emb = discord.Embed( title = 'Навигация по командам', description = '**ВНИМАНИЕ!** Бот ещё в разработке!', colour = teal )
    # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски
    emb.set_author(name=f"{ctx.author}",icon_url=ctx.author.avatar.url)
    # Отображает Аватар отправителя
    emb.add_field( name = ';help', value = f'`Отображает эту команду`', inline=False)
    # TODO - `{prefix}server` `{prefix}profile` 
    emb.add_field( name = ';ping', value = f'`Отображает задержку бота в миллисекундах (ms)`', inline=False)
    # TODO - emb.add_field( name = 'Модерирование', value = f'`{prefix}mute` `{prefix}unmute` `{prefix}ban` `{prefix}kick` `{prefix}clear` ', inline=False)
    emb.set_thumbnail(url = client.user.avatar.url)
    emb.set_footer( icon_url = client.user.avatar.url, text = f'Rublewka BOT © Copyright 2023 | Все права защищены' )

    await ctx.reply ( embed = emb)
    # преобразование embed 

    print(f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ')
    # Информация, что команда "help" была использована

# Filter
#@client.event
#async def on_message( message ):
#    await client.process_commands( message )
#    msg = message.content.lower()
#    with open('prohibitednames.txt') as bad_words:
#    if msg in bad_words:
#        await message.delete()
#        await message.author.send(f'{message.author.name}, на сервере **Rublewka** не разрешается использовать/употреблять настоящие имена')
#        print('[Logs:moderation] Message {message} has been deleted due to filter violations')
#_______________
# level system

#_______________

#Не работает/в разработке
#\/\/\/

#Kick
#@client.command(aliases = ['Kick', 'kICK', 'KICK', 'kick'])
#@commands.has_permissions ( administrator = True ) # Команда только для пользователей имеющих роль с правами "Администратор"
#async def __kick(ctx, member: discord.Member, *, reason = None): # Асинхронная функция __kick(ctx, member: discord.Member, *, reason = None)
    #Аргументы: ctx - отправка сообщения с помощью команды (Обязательно)
    #Аргументы: member: discord.Member - "member" ----- может быть любой текст, но для удобства использую member (Discord.Member - для получения id указанного пользователя)
    #Аргументы: * - предыдущий аргумент необходим
    #Аргументы: reason = None - "reason" ----- может быть любой текст, но для удобства использовал reason, "None" - значение по умолчанию
#    await ctx.message.add_reaction('✅') # Добавляет реакцию к сообщению с командой
#    await member.kick( reason = reason ) # Кикнуть пользователя по причине (Преобразует причину бота в причину дискорда)
#    emb = discord.Embed( title = 'Kicked', description = f'Пользователь {member}  был кикнут по причине { reason } ', colour = discord.Color.red() )
#    emb.set_author( name = client.user.name )
#    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
#    emb.set_thumbnail(url = client.user.avatar_url)

#    await ctx.send( embed = emb )

#    print(f'[Logs:moderation] Пользователь {member} был кикнут по причине {reason} | {prefix}kick ')


#@__kick.error
#async def kick_error(ctx, goodbye):
	#if isinstance ( goodbye, commands.MissingRequiredArgument):
		#emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		#emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		#emb.add_field( name = 'Использование', value = "!кик <@⁣Участник | ID>", inline=False)
		#emb.add_field( name = 'Пример', value = "`!кик @⁣Участник`\n┗ Кикнет указаного участника.", inline=False)
		#emb.set_thumbnail(url = client.user.avatar_url)
		#emb.set_footer( icon_url = client.user.avatar_url, text = f"Rublewka BOT  © Copyright 2023 | Все права защищены"   )
		#await ctx.send ( embed = emb)
		#print(f"[Logs:error] Необходимо указать участника | {prefix}kick")

	#if isinstance (goodbye, commands.MissingPermissions):
		#emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		#emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		#emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		#emb.set_thumbnail(url = client.user.avatar_url)
		#emb.set_footer( icon_url = client.user.avatar_url, text = f"Rublewka BOT  © Copyright 2023 | Все права защищены"   )
		#await ctx.send ( embed = emb)
		#print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался кикнуть | {prefix}kick")














































































































































































































client.run (settings['TOKEN']) #DON'T TOUCH IT