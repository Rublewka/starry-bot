# setup
import json
import os
import os.path
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands
from roblox import Client
from config import settings
from src import log
prefix = settings['PREFIX']
client = commands.Bot(command_prefix = commands.when_mentioned_or(settings['PREFIX']), intents=discord.Intents.all())
client.remove_command('help') 
load_dotenv()
RoClient = Client(os.getenv("ROBLOXTOKEN"))
logger = log.setup_logger(__name__)
# setup end

#startup
@client.event
async def on_ready(): 
    logger.info("Logged on as") # startup message in console
    logger.info("""

██████╗ ██╗   ██╗██████╗ ██╗     ███████╗██╗    ██╗██╗  ██╗ █████╗     ██████╗  ██████╗ ████████╗
██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝██║    ██║██║ ██╔╝██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝██║     █████╗  ██║ █╗ ██║█████╔╝ ███████║    ██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║██╔══██╗██║     ██╔══╝  ██║███╗██║██╔═██╗ ██╔══██║    ██╔══██╗██║   ██║   ██║   
██║  ██║╚██████╔╝██████╔╝███████╗███████╗╚███╔███╔╝██║  ██╗██║  ██║    ██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   

""")
    logger.info(" ____=====Discord=====____")
    logger.info("Bot Info: %s", settings['NAME BOT'])
    logger.info("Bot ID: %s", settings['ID'])
#    rbs = client.get_channel(1076240177032351765)
#    await rbs.send("Successfull restart") # startup message in status channel
#    logger.info("Successfully sent message to Rublewka Bot Status channel")
    logger.info("Bot start success")
    logger.info("____=====Roblox=====____")
    user = await RoClient.get_authenticated_user()
    logger.info("ID: %s", user.id)
    logger.info("Name: %s", user.name)
    logger.info("Roblox session successfully initialized")
# startup end

# variables section

rvr_token = 'rvr2b087uhj4acpftd4vs7dbvgyow4a5ujfz2hkvs0w4j5nzzq8gdftgcadrewulalkx'

# ___________
# colors
DEFAULT = 0
TEAL = 0x1abc9c
DARK_TEAL = 0x11806a
GREEN = 0x2ecc71
DARK_GREEN = 0x1f8b4c
BLUE = 0x3498db
DARK_BLUE = 0x206694
PURPLE = 0x9b59b6
DARK_PURPLE = 0x71368a
MAGENTA = 0xe91e63
DARK_MAGENTA = 0xad1457
GOLD = 0xf1c40f
DARK_GOLD = 0xc27c0e
ORANGE = 0xe67e22
DARK_ORANGE = 0xa84300
RED = 0xe74c3c
DARK_RED = 0x992d22
LIGHTER_GREY = 0x95a5a6
DARK_GREY = 0x607d8b
LIGHT_GREY = 0x979c9f
DARKER_GREY = 0x546e7a
BLURPLE = 0x7289da
GREYPLE = 0x99aab5

# ___________
# variables section end

# Ping
@client.command(aliases = ['Ping', 'PING', 'pING', 'ping', ' ping', ' PING', ' pING', ' Ping'])
async def __ping(ctx): 
    ping = client.ws.latency

    ping_emoji = '🟩🔳🔳🔳🔳' # 100ms

    if ping > 0.15000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' # 150ms

    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' # 200ms

    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' # 250ms

    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩' # 300ms

    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧' # 350ms

    if ping > 0.40000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' # 400ms

    message = await ctx.reply('Please wait a little bit. . .')
    await message.edit(content = f'Pong! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:')
#    print(f'[Logs:utils] Bot\'s ping was showen | {prefix}ping')
#    print(f'[Logs:utils] Bot\'s current ping == {ping * 1000:.0f}ms | {prefix}ping')
    # Ping end

# Help
@client.command(aliases = ['Help', 'help', 'HELP', 'hELP', 'хелп', 'Хелп', 'ХЕЛП', 'хЕЛП'])
async def __help (ctx):
#    emb.add_field(name = f'{prefix}help', value = f'`Отображает эту команду`', inline=False)
    emb = discord.Embed( title = 'Command navigaation | Help', description = f'**Attention!** Bot is still i development! | Bot\'s prefix: `{prefix}`', colour = TEAL )
    # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски
    emb.set_author(name=f"{ctx.author}",icon_url=ctx.author.avatar.url)
    # Отображает Аватар отправителя
    emb.add_field(name = f'{prefix}help', value = '`Shows this command`', inline=False)
    emb.add_field(name = f'{prefix}ping', value = '`Shows Bot\'s delay in milliseconds (ms)`', inline=False)
    emb.set_thumbnail(url = client.user.avatar.url)
    emb.set_footer( icon_url = client.user.avatar.url, text = 'Rublewka BOT © Copyright 2023 | Все права защищены' )

    await ctx.reply ( embed = emb)
#    print(f'[Logs:info] Help command used | {prefix}help ')


@client.command(aliases = ['getuser', 'GETUSER', ' Getuser'])
async def __getuser(ctx):
    for user_mentioned in ctx.message.mentions:
        discordId = user_mentioned.id
    r = requests.get(
        f'https://registry.rover.link/api/guilds/1018415075255668746/discord-to-roblox/{discordId}',
        headers={'Authorization': f'Bearer {rvr_token}'},
        timeout=10)
    data = r.json()
    json_str = json.dumps(data)
    resp = json.loads(json_str)
    print(resp) #use if debug needed
#    user = await RoClient.get_user(resp['robloxId'])
#    if user.description == '':
#        desc = '*None*'
#    else:
#        desc = user.description



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