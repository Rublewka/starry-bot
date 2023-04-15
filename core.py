# setup
import json
import os
import os.path
from random import randrange
import discord
import requests
import openai
from src.aclient import client as aclient
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from roblox import Client
from config import settings
from src import log, art, personas, responses
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
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\033[1;35m"
    CYAN = "\033[1;36m"
    GRAY = "\033[1;30m"
    PURPLE = "\033[1;35m"
    RESET = "\033[0m"
    logger.info(f"Logged on as") # startup message in console
    logger.info(F"""

{YELLOW}██████╗ ██╗   ██╗██████╗ ██╗     ███████╗██╗    ██╗██╗  ██╗ █████╗     ██████╗  ██████╗ ████████╗
██╔══██╗██║   ██║██╔══██╗██║     ██╔════╝██║    ██║██║ ██╔╝██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║██████╔╝██║     █████╗  ██║ █╗ ██║█████╔╝ ███████║    ██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║██╔══██╗██║     ██╔══╝  ██║███╗██║██╔═██╗ ██╔══██║    ██╔══██╗██║   ██║   ██║   
██║  ██║╚██████╔╝██████╔╝███████╗███████╗╚███╔███╔╝██║  ██╗██║  ██║    ██████╔╝╚██████╔╝   ██║   
{CYAN}╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   {RESET}

""")
    logger.info(f"{PURPLE}Discord{RESET}")
    logger.info(f"{RED}Bot Name:{RESET}  {settings['NAME BOT']}")
    logger.info(f"{RED}Bot ID:{RESET}  {settings['ID']}")
#    rbs = client.get_channel(1076240177032351765)
#    await rbs.send("Successfull restart") # startup message in status channel
#    logger.info("Successfully sent message to Rublewka Bot Status channel")
    logger.info(f"{YELLOW}Discord session{RESET} {GREEN}successfully{RESET} {CYAN}initialized{RESET}")
    logger.info(f"{PURPLE}Roblox{RESET}")
    user = await RoClient.get_authenticated_user()
    logger.info(f"{RED}ID:{RESET}  {user.id}")
    logger.info(f"{RED}Name:{RESET}  {user.name}")
    logger.info(f"{GRAY}Roblox session{RESET} {GREEN}successfully{RESET} {CYAN}initialized{RESET}")
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

@client.tree.command(name="chat", description="Have a chat with ChatGPT")
async def chat(interaction: discord.Interaction, *, message: str):
    if aclient.is_replying_all == "True":
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(
            "> **WARN: You already on replyAll mode. If you want to use the Slash Command, switch to normal mode by using `/replyall` again**")
        logger.warning("\x1b[31mYou already on replyAll mode, can't use slash command!\x1b[0m")
        return
    if interaction.user == client.user:
        return
    username = str(interaction.user)
    channel = str(interaction.channel)
    logger.info(
        f"\x1b[31m{username}\x1b[0m : /chat [{message}] in ({channel})")
    await aclient.send_message(interaction, message)


@client.tree.command(name="private", description="Toggle private access")
async def private(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    if not aclient.isPrivate:
        aclient.isPrivate = not aclient.isPrivate
        logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
        await interaction.followup.send(
            "> **INFO: Next, the response will be sent via private reply. If you want to switch back to public mode, use `/public`**")
    else:
        logger.info("You already on private mode!")
        await interaction.followup.send(
            "> **WARN: You already on private mode. If you want to switch to public mode, use `/public`**")

@client.tree.command(name="public", description="Toggle public access")
async def public(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    if aclient.isPrivate:
        aclient.isPrivate = not aclient.isPrivate
        await interaction.followup.send(
            "> **INFO: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
        logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
    else:
        await interaction.followup.send(
            "> **WARN: You already on public mode. If you want to switch to private mode, use `/private`**")
        logger.info("You already on public mode!")


@client.tree.command(name="replyall", description="Toggle replyAll access")
async def replyall(interaction: discord.Interaction):
    aclient.replying_all_discord_channel_id = str(interaction.channel_id)
    await interaction.response.defer(ephemeral=False)
    if aclient.is_replying_all == "True":
        aclient.is_replying_all = "False"
        await interaction.followup.send(
            "> **INFO: Next, the bot will response to the Slash Command. If you want to switch back to replyAll mode, use `/replyAll` again**")
        logger.warning("\x1b[31mSwitch to normal mode\x1b[0m")
    elif aclient.is_replying_all == "False":
        aclient.is_replying_all = "True"
        await interaction.followup.send(
            "> **INFO: Next, the bot will disable Slash Command and responding to all message in this channel only. If you want to switch back to normal mode, use `/replyAll` again**")
        logger.warning("\x1b[31mSwitch to replyAll mode\x1b[0m")


#    @client.tree.command(name="chat-model", description="Switch different chat model")
#    @app_commands.choices(choices=[
#        app_commands.Choice(name="Official GPT-3.5", value="OFFICIAL")
#    ])

#    async def chat_model(interaction: discord.Interaction, choices: app_commands.Choice[str]):
#        await interaction.response.defer(ephemeral=False)
#        original_chat_model = client.chat_model
#        original_openAI_gpt_engine = client.openAI_gpt_engine

#        try:
#            if choices.value == "OFFICIAL":
#                client.openAI_gpt_engine = "gpt-3.5-turbo"
#                client.chat_model = "OFFICIAL"
#            else:
#                raise ValueError("Invalid choice")
#
#            client.chatbot = client.get_chatbot_model()
#            await interaction.followup.send(f"> **INFO: You are now in {client.chat_model} model.**\n")
#            logger.warning(f"\x1b[31mSwitch to {client.chat_model} model\x1b[0m")
#
#        except Exception as e:
#            client.chat_model = original_chat_model
#            client.openAI_gpt_engine = original_openAI_gpt_engine
#            client.chatbot = client.get_chatbot_model()
#            await interaction.followup.send(f"> **ERROR: Error while switching to the {choices.value} model, check that you've filled in the related fields in `.env`.**\n")
#            logger.exception(f"Error while switching to the {choices.value} model: {e}")


@client.tree.command(name="reset", description="Clear ChatGPT conversation history (Please note: It does not clear message history in channel)")
async def reset(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        if aclient.chat_model == "OFFICIAL":
            aclient.chatbot = aclient.get_chatbot_model()
        elif aclient.chat_model == "UNOFFICIAL":
            aclient.chatbot.reset_chat()
            await aclient.send_start_prompt()
        elif aclient.chat_model == "Bard":
            aclient.chatbot = aclient.get_chatbot_model()
            await aclient.send_start_prompt()
        elif aclient.chat_model == "Bing":
            await aclient.chatbot.close()
            aclient.chatbot = aclient.get_chatbot_model()
            await aclient.send_start_prompt()
        await interaction.followup.send("> **INFO: I have forgotten everything.**")
        personas.current_persona = "standard"
        logger.warning(
            f"\x1b[31m{aclient.chat_model} bot has been successfully reset\x1b[0m")

@client.tree.command(name="help", description="Show help for the bot")
async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send(""":star: **BASIC COMMANDS** \n
        - `/chat [message]` Chat with ChatGPT!
        - `/draw [prompt]` Generate an image with the Dalle2 model
        - `/private` ChatGPT switch to private mode
        - `/public` ChatGPT switch to public mode
        - `/reset` Clear ChatGPT conversation history (Please note: It does not clear message history in channel)""")

        logger.info(
            "\x1b[31mSomeone needs help!\x1b[0m")

@client.tree.command(name="draw", description="Generate an image with the Dalle2 model")
async def draw(interaction: discord.Interaction, *, prompt: str):
        if interaction.user == client.user:
            return

        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : /draw [{prompt}] in ({channel})")

        await interaction.response.defer(thinking=True, ephemeral=aclient.isPrivate)
        try:
            path = await art.draw(prompt)

            file = discord.File(path, filename="image.png")
            title = f'**Promt: `{prompt}`**'
            desc = f'Requested by {interaction.user.mention}'
            embed = discord.Embed(title=title, description=desc)
            embed.set_image(url="attachment://image.png")

            await interaction.followup.send(file=file, embed=embed)

        except openai.InvalidRequestError:
            await interaction.followup.send(
                "> **ERROR: Inappropriate request**")
            logger.info(
            f"\x1b[31m{username}\x1b[0m made an inappropriate request.!")

        except Exception as e:
            await interaction.followup.send(
                "> **ERROR: Something went wrong**")
            logger.exception(f"Error while generating image: {e}")


@client.tree.command(name="switchpersona", description="Switch between optional chatGPT jailbreaks")
@app_commands.choices(persona=[
        app_commands.Choice(name="Random", value="random"),
        app_commands.Choice(name="Standard", value="standard"),
        app_commands.Choice(name="Do Anything Now 11.0", value="dan"),
        app_commands.Choice(name="Superior Do Anything", value="sda"),
        app_commands.Choice(name="Evil Confidant", value="confidant"),
        app_commands.Choice(name="BasedGPT v2", value="based"),
        app_commands.Choice(name="OPPO", value="oppo"),
        app_commands.Choice(name="Developer Mode v2", value="dev"),
        app_commands.Choice(name="DUDE V3", value="dude_v3"),
        app_commands.Choice(name="AIM", value="aim"),
        app_commands.Choice(name="UCAR", value="ucar"),
        app_commands.Choice(name="Jailbreak", value="jailbreak")
    ])
async def switchpersona(interaction: discord.Interaction, persona: app_commands.Choice[str]):
        if interaction.user == client.user:
            return

        await interaction.response.defer(thinking=True)
        username = str(interaction.user)
        channel = str(interaction.channel)
        logger.info(
            f"\x1b[31m{username}\x1b[0m : '/switchpersona [{persona.value}]' ({channel})")

        persona = persona.value

        if persona == personas.current_persona:
            await interaction.followup.send(f"> **WARN: Already set to `{persona}` persona**")

        elif persona == "standard":
            if aclient.chat_model == "OFFICIAL":
                aclient.chatbot.reset()
            elif aclient.chat_model == "UNOFFICIAL":
                aclient.chatbot.reset_chat()
            elif aclient.chat_model == "Bard":
                aclient.chatbot = aclient.get_chatbot_model()
            elif aclient.chat_model == "Bing":
                aclient.chatbot = aclient.get_chatbot_model()

            personas.current_persona = "standard"
            await interaction.followup.send(
                f"> **INFO: Switched to `{persona}` persona**")

        elif persona == "random":
            choices = list(personas.PERSONAS.keys())
            choice = randrange(0, 6)
            chosen_persona = choices[choice]
            personas.current_persona = chosen_persona
            await responses.switch_persona(chosen_persona, aclient)
            await interaction.followup.send(
                f"> **INFO: Switched to `{chosen_persona}` persona**")


        elif persona in personas.PERSONAS:
            try:
                await responses.switch_persona(persona, aclient)
                personas.current_persona = persona
                await interaction.followup.send(
                f"> **INFO: Switched to `{persona}` persona**")
            except Exception as e:
                await interaction.followup.send(
                    "> **ERROR: Something went wrong, please try again later!**")
                logger.exception(f"Error while switching persona: {e}")

        else:
            await interaction.followup.send(
                f"> **ERROR: No available persona: `{persona}` **")
            logger.info(
                f'{username} requested an unavailable persona: `{persona}`')

@client.event
async def on_message(message):
    if aclient.is_replying_all == "True":
        if message.author == client.user:
            return
        if aclient.replying_all_discord_channel_id:
            if message.channel.id == int(aclient.replying_all_discord_channel_id):
                username = str(message.author)
                user_message = str(message.content)
                channel = str(message.channel)
                logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
                await aclient.send_message(message, user_message)
#    else:
#        logger.exception("replying_all_discord_channel_id not found, please use the commnad `/replyall` again.")




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