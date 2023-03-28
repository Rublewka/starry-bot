# setup
import discord
import json
import os, os.path
import sys
import functools
import itertools
import math
import random
import asyncio
import ffmpeg
import yt_dlp
import http.client
import urllib3
import time
import requests
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
from config import settings
from async_timeout import timeout
from roblox import Client
from discord import FFmpegPCMAudio
from discord import TextChannel
from yt_dlp import YoutubeDL
prefix = settings['PREFIX']
client = commands.Bot(command_prefix = commands.when_mentioned_or(settings['PREFIX']), intents=discord.Intents.all())
client.remove_command('help') 
load_dotenv()
RoClient = Client(os.getenv("ROBLOXTOKEN"))
# setup end

#startup
@client.event
async def on_ready(): 
    print (f"[Logs:startup] Logged on as ") # startup message in console
    print ("""

██████╗ ██╗   ██╗██████╗ ██╗     ███████╗██╗    ██╗██╗  ██╗ █████╗     ██████╗  ██████╗ ████████╗
██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝██║    ██║██║ ██╔╝██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝██║     █████╗  ██║ █╗ ██║█████╔╝ ███████║    ██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║██╔══██╗██║     ██╔══╝  ██║███╗██║██╔═██╗ ██╔══██║    ██╔══██╗██║   ██║   ██║   
██║  ██║╚██████╔╝██████╔╝███████╗███████╗╚███╔███╔╝██║  ██╗██║  ██║    ██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   

""")
    print("[Logs:startup] ____=====Discord=====____")
    print(f"[Logs:startup] Bot Info: {settings['NAME BOT']}")
    print(f"[Logs:startup] Bot ID: {settings['ID']}")
#    rbs = client.get_channel(1076240177032351765)
#    await rbs.send("Successfull restart") # startup message in status channel
    print(f"[Logs:startup] Successfully sent message to Rublewka Bot Status channel")
    print("[Logs:startup] Bot start success")
    print("[Logs:startup] ____=====Roblox=====____")
    user = await RoClient.get_authenticated_user()
    print("ID:", user.id)
    print("Name:", user.name)
# startup end

# variables section

rvr_token = 'rvr2b087uhj4acpftd2dc32kw5z7uzcryf9rg21figqs6byvnyrky8q8q7ygc7jrea6o'

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
# voice

# ❗ ❗ ❗ ❗ ❗ 
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        vchan = ctx.message.author.voice.channel
        await vchan.connect()
        await ctx.reply("Успешно подключился к голосовому каналу")
    else:
        await ctx.reply("Вы должны быть в голосовом канале, чтобы использовать эту команду")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.reply("Успешно отключился от голосового канала")
    else:
        await ctx.reply("Я не в голосовом канале")

# music

@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
#        await ctx.reply('Bot is playing')

# check if the bot is already playing
#    else:
#        await ctx.reply("Bot is already playing")
#        return


# command to resume voice if it is paused
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
#        await ctx.reply('Bot is resuming')


# command to pause voice if it is playing
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
#        await ctx.reply('Bot has been paused')


# command to stop voice
@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
#        await ctx.reply('Stopping...')


# Help
@client.command(aliases = ['Help', 'help', 'HELP', 'hELP', 'хелп', 'Хелп', 'ХЕЛП', 'хЕЛП'])
async def __help (ctx):
#    emb.add_field(name = f'{prefix}help', value = f'`Отображает эту команду`', inline=False)
    emb = discord.Embed( title = 'Навигация по командам', description = f'**ВНИМАНИЕ!** Бот ещё в разработке! | Префикс бота : `{prefix}`', colour = teal )
    # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски
    emb.set_author(name=f"{ctx.author}",icon_url=ctx.author.avatar.url)
    # Отображает Аватар отправителя
    emb.add_field(name = f'{prefix}help', value = f'`Отображает эту команду`', inline=False)
    # TODO - `{prefix}server` `{prefix}profile` 
    emb.add_field(name = f'{prefix}ping', value = f'`Отображает задержку бота в миллисекундах (ms)`', inline=False)
    emb.add_field(name = f'{prefix}join', value = f'`Подключение бота к голосовому каналу`', inline=False)
    emb.add_field(name = f'{prefix}leave', value = f'`Отключение бота от голосового канала`', inline=False)
    emb.add_field(name = f'{prefix}play <youtube link>', value = f'`Проигрывание музыки; Использование: {prefix}play <ссылка на YouTube видеоролик>`', inline=False)
    emb.add_field(name = f'{prefix}pause', value = f'`Приостанавливает воспроизведение музыки`', inline=False)
    emb.add_field(name = f'{prefix}resume', value = f'`Возобновляет воспроизведение музыки`', inline=False)
    emb.add_field(name = f'{prefix}stop', value = f'`Останавливает воспроизведение музыки`', inline=False)
    # TODO - emb.add_field( name = 'Модерирование', value = f'`{prefix}mute` `{prefix}unmute` `{prefix}ban` `{prefix}kick` `{prefix}clear` ', inline=False)
    emb.set_thumbnail(url = client.user.avatar.url)
    emb.set_footer( icon_url = client.user.avatar.url, text = f'Rublewka BOT © Copyright 2023 | Все права защищены' )

    await ctx.reply ( embed = emb)
    # преобразование embed 

    print(f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ')
    # Информация, что команда "help" была использована

@client.command(aliases = ['promote', 'Promote', ' promote'])
async def __promote(ctx):
    headers = {'Authorization': f'Bearer {rvr_token}'}
#    memberID = user_mentioned.id for user_mentioned in ctx.message.mentions
    r = requests.get(
        f'https://registry.rover.link/api/guilds/1008577770097496125/discord-to-roblox/1006501114419630081',
        headers={'Authorization': f'Bearer {rvr_token}'})
    data = r.json()
    json_str = json.dumps(data)
    resp = json.loads(json_str)
    user = await RoClient.get_user(resp['robloxId'])
    print(resp['robloxId'])
    print("Name:", user.name)
    print("Display Name:", user.display_name)
    print("Description:", user.description)


# Filter
#@client.event
#async def on_message( message ):
#    await client.process_commands( message )
#    msg = message.content.lower()
#    if msg in bad_words:
#        await message.delete()
#        await message.author.send(f'{message.author.name}, на сервере **Rublewka** не разрешается использовать/употреблять настоящие имена')
#        print(f'[Logs:moderation] Message sent by {message.author.username} has been deleted due to filter violations')
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