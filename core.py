# setup
import json
import os
import os.path
import asyncio
import datetime
import random
from random import randrange
import discord
import requests
import urllib.request
import openai
from roblox import AvatarThumbnailType
from src.verif_words import verification_words
from src.aclient import client as aclient
from dotenv import load_dotenv
from discord.ext import commands
from discord.abc import PrivateChannel
from discord.utils import get
from discord import app_commands, ChannelType
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

RoConnected = None



async def status_swap():
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"v{settings['VERSION']}"))
        await asyncio.sleep(15)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"with my friends"))
        await asyncio.sleep(15)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"with {settings['OWNER']}"))
        await asyncio.sleep(15)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"Roblox"))
        await asyncio.sleep(15)
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"/help"))
        await asyncio.sleep(15)

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
    client.loop.create_task(status_swap())
    dsc_err_channel = client.get_channel(1094687676151648286)
    logger.info(f"Starting up {client.user.name}#{client.user.discriminator}")
    logger.info(f"--{PURPLE}Discord{RESET}--")
    logger.info(f"{RED}Bot Name:{RESET}  {client.user.name}")
    logger.info(f"{RED}Bot ID:{RESET}  {client.user.id}")
    logger.info(f"{RED}Bot Version:{RESET}  {settings['VERSION']}")
    await client.tree.sync()
    logger.info(f"{YELLOW}Discord session{RESET} {GREEN}successfully{RESET} {CYAN}initialized{RESET}")
    logger.info(f"--{MAGENTA}Roblox{RESET}--")
    global start_time
    start_time = datetime.datetime.now()

    host1 = 'https://roblox.com'
    def roconnect(host=host1):
        try:
            urllib.request.urlopen(host1)
            return True
        except urllib.error.URLError:
            return False
    if roconnect():
        global RoConnected
        user = await RoClient.get_authenticated_user()
        logger.info(f"{RED}Roblox ID:{RESET}  {user.id}")
        logger.info(f"{RED}Roblox Name:{RESET} {user.name}")
        logger.info(f"{YELLOW}Roblox session{RESET} {GREEN}successfully{RESET} {CYAN}initialized{RESET}")
        RoConnected = True
    elif roconnect() == None:
        logger.error(f"{YELLOW}Bot inizialize{RESET} {RED}incomplete{RESET}")
        RoConnected = None
    else:
        message = f'`Could not connect to Roblox Gateway. Please check your internet connection and try again.`'
        await dsc_err_channel.send(message)
        logger.error(f"{YELLOW}Roblox session{RESET} {RED}could not initialize{RESET}")
        RoConnected = False
        

    





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




async def get_verification_thread(interaction: discord.Interaction) -> discord.Thread:
    user = interaction.user
    channel = interaction.channel
    thread_name = f"{user.name} Verification"
    thread = await channel.create_thread(
        name=thread_name,
        auto_archive_duration=1440,
        type=discord.ChannelType.private_thread,
        invitable=False
    )
    await thread.add_user(user)
    return thread


async def get_roblox_username(interaction: discord.Interaction, thread: discord.Thread) -> str:
    user = interaction.user

    def check(message):
        return message.author == user

    await thread.send(f"{interaction.user.mention} please type in your Roblox Username to verify")
    user_message = await client.wait_for('message', check=check)
    return user_message.content


async def get_rouser_info(roblox_username: str, thread: discord.Thread) -> dict:
    rouser = await RoClient.get_user_by_username(roblox_username)
    emb = discord.Embed(
        title="Check your account info",
        description="""If this is your account - type `Continue` to continue; 
        If not - type `Back` to go back."""
    )
    emb.add_field(name="Username", value=rouser.name, inline=False)
    emb.add_field(name="Display Name", value=rouser.display_name, inline=False)
    emb.add_field(name="ID", value=rouser.id, inline=False)
    if rouser.description == '':
        desc = '*None*'
    else:
        desc = rouser.description
    emb.add_field(name="Description", value=desc, inline=False)
    emb.add_field(name="Created At", value=rouser.created, inline=False)
    user_thumbnails = await RoClient.thumbnails.get_user_avatar_thumbnails(
        users=[rouser],
        type=AvatarThumbnailType.full_body,
        size=(420, 420)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        emb.set_thumbnail(url=user_thumbnail.image_url)
    await thread.send(embed=emb)
    return rouser

#@client.tree.command(name="verify", description="Link your Roblox account with your Discord account")
async def verify_member(interaction: discord.Interaction, member: discord.Member):
    thread = await get_verification_thread(interaction)

    roblox_username = await get_roblox_username(interaction, thread)
    rouser = await get_rouser_info(roblox_username, thread)

    def check(message):
        return message.author == interaction.user

    while True:
        await thread.send("If this is your account - type `Continue` to continue; If not - type `Back` to go back.")
        con = await client.wait_for('message', check=check)
        if con.content.lower() == 'continue':
            break
    
    words = verification_words
    random_words = []
    for i in range(5):
        word = random.choice(words)
        random_words.append(word)
    verif_words = ", ".join(random_words)
    emb = discord.Embed(
        title=f"Verification words for {interaction.user.name}",
        description='Please paste these verification words into your Roblox Profile Description'
    )
    emb.add_field(name="Verification words", value=f'`{verif_words}`', inline=False)
    emb.set_footer(text="If Roblox Filtered these verification words, type \"New words\" to get a new ones")
    await thread.send(embed=emb)

    while True:
        await thread.send(f"Type `Done` when you are done")
        done = await client.wait_for('message', check=check)
        if done.content.lower() == 'done' and rouser.description == verif_words:
            try:
                await member.add_roles(discord.utils.get(member.guild.roles, name="Members"))
                await member.edit(nick=rouser.name)
                await thread.send("Verification process complete, enjoy your stay!")
                await thread.edit(name=f"{interaction.user.name} Verification (Completed)", locked=True)
                break
            except discord.Forbidden:
                await thread.send("Couldn't verify your account, contact bot developer `(Error code: 403)`")
                await thread.edit(name=f"{interaction.user.name} Verification (Error)", locked=True)
                await thread.send("@TheSkout#8213")
                break
            except discord.HTTPException:
                await thread.send("Couldn't verify your account, contact bot developer `(Error code: 500)`")
                await thread.edit(name=f"{interaction.user.name} Verification (Error)", locked=True)
                await thread.send("@TheSkout#8213")
                break
        elif done.content.lower() == 'new words':
            continue
        else:
            await thread.send("Couldn't verify your account, please try again later")
            await thread.edit(name=f"{interaction.user.name} Verification (Failed)", locked=True)
            break


#@client.tree.command(name="commands-sync", description="force tree commands sync")
async def sync(interaction: discord.Interaction):
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    CYAN = "\033[1;36m"
    RESET = "\033[0m"
    await interaction.response.defer(ephemeral=True, thinking=True)
    await client.tree.sync()
    await interaction.followup.send(f"Slash commands synced")
    logger.info(f"{YELLOW}Discord{RESET} application commands {CYAN}synced{RESET} {GREEN}successfully{RESET}")

#@client.tree.command(name='rename', description='Rename Bot')
async def rename(interaction: discord.Interaction, name: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    await client.user.edit(username=name)
    await interaction.followup.send(f'Renamed bot to {name}')

# Ping
@client.tree.command(name="status", description='Shows bot\'s status')
async def status(interaction: discord.Interaction):
    # Get the websocket latency
    ping = client.ws.latency

    # Define the green bar emoji as the default
    ping_emoji = '<:icons_goodping:880113406915538995>' # 100ms


    # Check if ping is greater than 250ms and if so, update the emoji
    if ping > 0.25000000000000000:
        ping_emoji = '<:icons_idelping:880113405720145990>' # 250ms

    # Check if ping is greater than 400ms and if so, update the emoji
    if ping > 0.40000000000000000:
        ping_emoji = '<:icons_badping:880113405007114271>' # 400ms

    # Send a message back to the user with the ping emoji and the ping time in milliseconds
    await interaction.response.defer(ephemeral=False, thinking=True)
    delta_uptime = datetime.datetime.now() - start_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if RoConnected == True:
        con = "<:icons_online:860123643395571713> Connected to Roblox"
    elif RoConnected == None:
        con = "<:icons_warning:908958943466893323> The bot haven\'t properly initialized, please contact bot developer"
    else:
        con = "<:icons_outage:868122243845206087> Roblox connection not established"
    emb = discord.Embed(title="Bot Status", description=None, color=BLUE)
    emb.add_field(name="Latency", value=f"{ping_emoji} `{ping * 1000:.0f}ms`", inline=False)
    emb.add_field(name="Roblox", value=f"{con}", inline=False)
    emb.add_field(name="Uptime", value=f"<:clock:1113391359274000394> I've been up for `{days} days, {hours} hours, {minutes} minutes and {seconds} seconds`", inline=False)
    emb.add_field(name="Version", value=f"`{settings['VERSION']}`", inline=False)
    await interaction.followup.send(embed=emb)

# Help
#@client.tree.command(name="help", description="Show help for the bot")
async def help(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("""

<:icons_generalinfo:866599434098835486> **Basic** 
> - `/help` Shows this message
> - `/version` Shows the bot's version
> - `/status` Shows the bot's status


<:roblox:1023778640145694740> **Roblox** 
> - `/getuser` Get user info from Roblox

<:gpt:1099041860971933767> **ChatGPT** 
> - `/chat [message]` Chat with ChatGPT!
> - `/draw [prompt]` Generate an image with the Dalle2 model
> - `/private` ChatGPT switch to private mode
> - `/public` ChatGPT switch to public mode
> - `/reset` Clear ChatGPT conversation history (Please note: It does not clear message history in channel)


<a:warningbug:905560995886411806> *The Bot is still in heavy development, more commands and functions are coming in future* <a:warningbug:905560995886411806>
""")


@client.tree.command(name="version", description="Shows the bot's version")
async def version(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send(f"{client.user.mention} current version: `{settings['VERSION']}`")

#@client.tree.command(name="getuser", description="Get user info from Roblox")
async def getuser(interaction: discord.Interaction, user: discord.User):
    if RoConnected == True:
        await interaction.response.defer(ephemeral=False, thinking=True)
        discordId = user.id
        r = requests.get(
            f'https://registry.rover.link/api/guilds/1018415075255668746/discord-to-roblox/{discordId}',
            headers={'Authorization': f'Bearer {rvr_token}'},
            timeout=10)
        data = r.json()
        json_str = json.dumps(data)
        resp = json.loads(json_str)
#        print(resp) #use if debug needed
        ruser = await RoClient.get_user(resp['robloxId'])
        if ruser.description == '':
           desc = '*None*'
        else:
           desc = ruser.description
        emb = discord.Embed(title=None, description=f"{user.mention} Roblox Profile", colour=GREYPLE)
        emb.add_field(name="Roblox ID", value=ruser.id, inline=False)
        emb.add_field(name="Roblox Username", value=ruser.name, inline=False)
        emb.add_field(name="Roblox Display Name", value=ruser.display_name, inline=False)
        emb.add_field(name="Roblox Description", value=desc, inline=False)
        await interaction.followup.send(embed=emb)
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("The bot couldn't connect to Roblox. Please contact bot developer.")






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


@client.tree.command(name="switchpersona", description="Switch between optional ChatGPT personas")
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