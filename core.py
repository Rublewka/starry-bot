# setup
import json
import os
import os.path
import asyncio
import datetime
import random
import discord
import requests
import urllib.request
import logging
import sqlite3
from logging import *
from discord import app_commands
from dislog import DiscordWebhookHandler
from roblox import AvatarThumbnailType
from src.verif_words import verification_words
from dotenv import load_dotenv
from discord.ext import commands
from roblox import Client
from roblox.utilities.exceptions import *
from roblox.utilities.iterators import SortOrder
from config import settings
#from config import roles
prefix = settings['PREFIX']

client = commands.Bot(command_prefix = commands.when_mentioned_or(settings['PREFIX']), intents=discord.Intents.all())
client.remove_command('help') 
load_dotenv()
RoClient = Client(os.getenv("ROBLOXTOKEN"))
# setup end
db_token = os.getenv("DBTOKEN")

run_nightly = True

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://starry_bot:TPth5ILO9WiJUcKU@rublewka-bot.b7dexs8.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
mclient = MongoClient(uri, server_api=ServerApi('1'))
db_raw = mclient.starry_bot
db = db_raw.users

RoConnected = None

bot_logs_webhook_url = "https://discord.com/api/webhooks/1121071054664781844/ANWk7zM02ZnXvDZibg-uNvxTtHKi6sdG5GteFLKW8k53Cuxigfd3BtCtR4J7NgEznrWe"


#logger.debug('This is a debug message')
#logger.info('This is an info message')
#logger.warning('This is a warning message')
#error('hi')
#critical('This is a critical message')

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
    client.loop.create_task(status_swap())
    dsc_err_channel = client.get_channel(1094687676151648286)
    print(f"Starting up {client.user.name}#{client.user.discriminator}")
    print(f"--Discord--")
    print(f"Bot Name:  {client.user.name}")
    print(f"Bot ID:  {client.user.id}")
    print(f"Bot Version:  {settings['VERSION']}")
    print(f"Discord session successfully initialized")
    print(f"--Roblox--")
    global start_time
    start_time = datetime.datetime.now()

    host1 = 'https://roblox.com'
    def roconnect(host=host1):
        try:
            urllib.request.urlopen(host1, timeout=15)
            return True
        except urllib.error.URLError:
            return False
    if roconnect():
        global RoConnected
        user = await RoClient.get_authenticated_user()
        print(f"Roblox ID:  {user.id}")
        print(f"Roblox Name: {user.name}")
        print(f"Roblox session successfully initialized")
        RoConnected = True
    elif roconnect() == None:
        error(f"Bot inizializition incomplete")
        RoConnected = None
    else:
        warn(f'`Could not connect to Roblox API. Try again later`')
        warn(f"Roblox session could not fully initialize")
        RoConnected = False

        

    





# startup end

# variables section

commands_ran = 0

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
        auto_archive_duration=60,
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

@client.tree.command(name="verify", description="Link your Roblox account with your Discord account")
async def verify_member(interaction: discord.Interaction):
    global commands_ran
    commands_ran += 1
    alr_verified_raw1 = db.find({"discordID": f"{interaction.user.id}"})
    alr_verified_raw2 = alr_verified_raw1.distinct(key="robloxID")
    alr_verified_raw3 = ''.join(alr_verified_raw2)
    alr_verified = alr_verified_raw3.replace("'", "")
    if len(alr_verified) == 0:
        thread = await get_verification_thread(interaction)
        await interaction.response.defer(ephemeral=True, thinking=True)
        await interaction.followup.send('Opened new verification thread for you')
        member = interaction.user
        roblox_username = await get_roblox_username(interaction, thread)
        rouser = await get_rouser_info(roblox_username, thread)

        def check(message):
            return message.author == interaction.user

        while True:
            await thread.send("If this is your account - type `Continue` to continue; If not - type `Cancel` to cancel verification.")
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
            rouser_a = await RoClient.get_user_by_username(username=f'{roblox_username}')
            if done.content.lower() == 'done' and rouser_a.description == verif_words:
                try:
                    entry = {
                    "username": f"{rouser.name}",
                    "discordID": f"{interaction.user.id}",
                    "robloxID": f"{rouser.id}"
                    }    
                    post_id = db.insert_one(entry).inserted_id
                    print(f'Verified user and created entry with ID {post_id}')
                    await thread.send("Verification process complete, enjoy your stay!")
                    await member.add_roles(discord.utils.get(member.guild.roles, name="Members"))
                    await member.edit(nick=rouser.name)
                    await thread.edit(name=f"{interaction.user.name} Verification (Completed)", locked=True)
                    break
                except discord.Forbidden:
                    await thread.send("Couldn't verify your account, contact bot developer `(Error code: 403)`")
                    await thread.edit(name=f"{interaction.user.name} Verification (Error)", locked=True)
                    break
                except discord.HTTPException:
                    await thread.send("Couldn't verify your account, contact bot developer `(Error code: 500)`")
                    await thread.edit(name=f"{interaction.user.name} Verification (Error)", locked=True)
                    break
            elif done.content.lower() == 'new words':
                continue
            elif done.content.lower() == 'cancel':
                await thread.send("Verification proccess canceled")
                await thread.edit(name=f"{interaction.user.name} Verification (Canceled)")
                break
            elif done.content.lower() == 'done' and rouser_a.description != verif_words:
                await thread.send("I couldn't find verification words in your **Roblox Profile Description**, try again!")
                continue
            else:
                await thread.send("Couldn't verify your account, please try again later")
                await thread.edit(name=f"{interaction.user.name} Verification (Failed)", locked=True)
                break
    else:
        rouser_alr_verified = await RoClient.get_user(user_id=alr_verified)
        await interaction.response.defer(ephemeral=True, thinking=True)
        await interaction.followup.send(f"You are already verified as **`{rouser_alr_verified.name}`**")



@client.tree.command(name="group-shout", description="Set new group shout")
async def group_shout(interaction: discord.Interaction, shout: str):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in interaction.user.roles):
        global commands_ran
        commands_ran += 1
        group = await RoClient.get_group(16965138)
        prev_shout = group.shout.body
        await group.update_shout(message=shout)
        new_shout = group.shout.body
        emb = discord.Embed(title="Updated group shout", colour=GREEN)
        emb.add_field(name="Previous shout:", value=f"`{prev_shout}`")
        emb.add_field(name="New shout:", value=f"`{new_shout}`")
        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(embed=emb)
        logging.info(f"@{interaction.user.name} changed group shout to `{new_shout}` (Previous group shout - `{prev_shout}`)")
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.followup.send(embed=emb)
        logging.info(f"@{interaction.user.name} tried to run `/group-shout` command, but they had no sufficient perms")

@client.command(name="deploy", description="Restarts the bot, pulls latest from GitHub")
async def deploy(ctx):
    if any(role.id in [1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        await ctx.reply("Sending **Stage** command to GitHub Actions...")
        url = 'https://api.github.com/repos/rublewka/starry-bot/actions/workflows/Stage.yml/dispatches'
        headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer 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",
        "X-GitHub-Api-Version": "2022-11-28"
        }
        payload = {
        "ref":"main"
            }
        response = requests.post(url=url, headers=headers, data=json.dumps(payload))
        print(f"{response.text}")
        await asyncio.sleep(5)
        await ctx.reply("Deploying...")
        await asyncio.sleep(15)        
        req_client = requests.session()
        url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
        req_client.get(url)  # sets cookie

        url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
        headers = {
            "Authorization": "Bearer ptlc_XXfLM4wlfgG6GvZ35VjdhLpvAy2Fs5lrgj839DsIsSZ",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "cookie": "eyJpdiI6ImRCejZqZU1ZYUwzRnVNQXl3c213bUE9PSIsInZhbHVlIjoiMy9rODRHV3V5MGsrenQrNTY0UEI0NSt4dVBHczBtZlV3YXo4Zk5FKytRWk0xbnRpcjdWME1mdG1tQ2s0ajVPdGwvaCs0UXNhSnU5S2grVjNadkgyaWpjZE1jQ3lFaUFBdVI5bThtVzNGbmREbDdZam9vMVVRS1VmbDExM0lZN3AiLCJtYWMiOiJkZTdmMzQ5OWU2Zjk4YjhkYzhhYzkzYzFhODYzOTU0MTIwMzEyNGFhZGNjNGI5ZmQ0N2FiZDBjN2Q1ZWVhOGZhIiwidGFnIjoiIn0%3D"
        }
        payload = '{"signal": "restart"}'
        await ctx.reply("Sending **Restart** signal to hosting...")
        response = req_client.request('POST', url, data=payload, headers=headers)
        print(f"{response.text}")
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687620564529283>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;deploy` command, but they had no sufficient perms")

@client.command(name="restart")
async def restart(ctx):
    if any(role.id in [1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        req_client = requests.session()
        url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
        req_client.get(url)  # sets cookie

        url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
        headers = {
            "Authorization": "Bearer ptlc_XXfLM4wlfgG6GvZ35VjdhLpvAy2Fs5lrgj839DsIsSZ",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "cookie": "eyJpdiI6ImRCejZqZU1ZYUwzRnVNQXl3c213bUE9PSIsInZhbHVlIjoiMy9rODRHV3V5MGsrenQrNTY0UEI0NSt4dVBHczBtZlV3YXo4Zk5FKytRWk0xbnRpcjdWME1mdG1tQ2s0ajVPdGwvaCs0UXNhSnU5S2grVjNadkgyaWpjZE1jQ3lFaUFBdVI5bThtVzNGbmREbDdZam9vMVVRS1VmbDExM0lZN3AiLCJtYWMiOiJkZTdmMzQ5OWU2Zjk4YjhkYzhhYzkzYzFhODYzOTU0MTIwMzEyNGFhZGNjNGI5ZmQ0N2FiZDBjN2Q1ZWVhOGZhIiwidGFnIjoiIn0%3D"
        }
        payload = '{"signal": "restart"}'
        await ctx.reply("Sending **Restart** signal to hosting...")
        response = req_client.request('POST', url, data=payload, headers=headers)
        print(f"{response.text}")
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687620564529283>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;restart` command, but they had no sufficient perms")


@client.tree.command(name="get-rank", description="Get member's current rank")
async def get_rank(interaction: discord.Interaction, user: str):
    global commands_ran
    commands_ran += 1
    group = await RoClient.get_group(16965138)
    try:
        target_user = await RoClient.get_user_by_username(user)
    except UserNotFound:
        target_user = None 
    if target_user != None:
        user = await RoClient.get_user(target_user.id)
        roles = await user.get_group_roles()
        role = None
        for test_role in roles:
            if test_role.group.id == group.id:
                role = test_role
                break
        if role == None:
            emb = discord.Embed(title="Member Info", colour=RED)
            emb.add_field(name=f"Not found", value=f"`{user.name}` is not in group!")
            emb.set_footer(text="Try checking username spelling!")
            await interaction.response.defer(ephemeral=False, thinking=True)
            await interaction.followup.send(embed=emb)
        else:
            emb = discord.Embed(title="Member Info", colour=BLUE)
            emb.add_field(name=f"{user.name}'s current rank is", value=f"`{role.name}`")
            await interaction.response.defer(ephemeral=False, thinking=True)
            await interaction.followup.send(embed=emb)
    else:
        emb = discord.Embed(title="Member Info", colour=DARK_RED)
        emb.add_field(name="Not found", value=f"Couln't find user with specified username (`{user}`)")
        emb.set_footer(text="Try checking username spelling!")
        await interaction.response.defer(ephemeral=False, thinking=True)
        await interaction.followup.send(embed=emb)


@client.tree.command(name="set-rank", description="Promote or Demote user")
@app_commands.choices(choices=[
    app_commands.Choice(name="Casuals", value="Casuals"),
    app_commands.Choice(name="Above Noobs", value="Above Noobs"),
    app_commands.Choice(name="Admin", value="Admin")
    ])
async def set_rank(interaction: discord.Interaction, user: str, choices: app_commands.Choice[str]):
    if (choices.value == "Casuals"):
        rank_raw = 1
    elif (choices.value == "Above Noobs"):
        rank_raw = 75
    elif (choices.value == "Admin"):
        rank_raw = 150
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in interaction.user.roles):
        global commands_ran
        commands_ran += 1
        await interaction.response.defer(ephemeral=False, thinking=True)
        group = await RoClient.get_group(16965138)
        GROUP_ID = 16965138
        try: 
            target_user = await RoClient.get_user_by_username(user)
        except UserNotFound:
            target_user = None
        if target_user != None:
            roles = await target_user.get_group_roles()
            role = None
            for test_role in roles:
                if test_role.group.id == GROUP_ID:
                    role = test_role
                    break
            if role == None:
                emb=discord.Embed(title="Rank update", colour=RED)
                emb.add_field(name="Not found", value=f"**`{target_user.name}`** is not in group!")
                emb.set_footer(text="Try checking username spelling!")
                await interaction.followup.send(embed=emb)
            elif role.rank == rank_raw:
                emb=discord.Embed(title="Rank update", colour=GOLD)
                emb.add_field(name="No changes were made...", value=f"**`{target_user.name}`** already have this rank!")
                await interaction.followup.send(embed=emb)
            else:
                new_rank = await group.set_rank(user=f'{target_user.id}', rank=rank_raw)
                emb=discord.Embed(title="Rank update", colour=GREEN)
                emb.add_field(name="Success!", value=f"Updated **`{target_user.name}`** rank to **{choices.value}**")
                await interaction.followup.send(embed=emb)
        else:  
            emb = discord.Embed(title="Member Info", colour=DARK_RED)
            emb.add_field(name="Not found", value=f"Couln't find user with specified username (`{user}`)")
            emb.set_footer(text="Try checking username spelling!")
            await interaction.followup.send(embed=emb)
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.followup.send(embed=emb)
        logging.info(f"@{interaction.user.name} tried to run `/set-rank` command, but they had no sufficient perms")

        
@client.tree.command(name="status", description='Shows bot\'s status')
async def status(interaction: discord.Interaction):
    # Get the websocket latency
    ping = client.ws.latency
    global commands_ran
    try:
        mclient.admin.command('ping')
        db_connected_raw= True
    except Exception:
        db_connected_raw = False
        
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
    if start_time == None:
         clock = '*not defined*'
    else:
        delta_uptime = datetime.datetime.now() - start_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        clock = f"I've been up for `{days} days, {hours} hours, {minutes} minutes and {seconds} seconds`"
    if RoConnected == True:
        con = "<:icons_online:860123643395571713> Connected to Roblox API"
    elif RoConnected == None:
        con = "<:icons_warning:908958943466893323> The bot haven\'t properly initialized, please contact bot developer"
    else:
        con = "<:icons_outage:868122243845206087> Not connected to Roblox API"
    if db_connected_raw == True:
        db_connected = "<:icons_online:860123643395571713> Connected to Database Services"
    else:
        db_connected = "<:icons_outage:868122243845206087> Not connected to Database Services"
        
    emb = discord.Embed(title="Bot Status", description=None, color=BLUE)
    emb.add_field(name="Latency", value=f"{ping_emoji} `{ping * 1000:.0f}ms`", inline=False)
    emb.add_field(name="Roblox API", value=f"{con}", inline=False)
    emb.add_field(name="Database Connection", value=db_connected, inline=False)
    emb.add_field(name="Uptime", value=f"<:clock:1113391359274000394> {clock}", inline=False)
    emb.add_field(name="Commands ran this session", value=f"<:icons_slashcmd:860133546315218944> I've ran `{commands_ran}` command(s) this session.", inline=False)
    emb.add_field(name="Version", value=f"`{settings['VERSION']}`", inline=False)
    await interaction.followup.send(embed=emb)
    commands_ran += 1

# Help
@client.tree.command(name="help", description="Show help for the bot")
async def help(interaction: discord.Interaction):
        global commands_ran
        commands_ran += 1
        await interaction.response.defer(ephemeral=False)
        await interaction.followup.send("""

<:icons_generalinfo:866599434098835486> **Basic** 
> - </help:1119362371710898308> - Shows this message
> - </version:1098672847469150248> - Shows the bot's version
> - </status:1145344954936332291> Shows the bot's status


<:roblox:1023778640145694740> **Roblox** 
> - </getuser:1114578145157320876> Get user info from Roblox
> - </verify:1119362371710898307> Verify yourself with Roblox account
> - </group-shout:1115625318238142486> Updates Roblox group shout


<:icons_warning:908958943466893323> *The Bot is still in heavy development, more commands and functions are coming in future* <:icons_warning:908958943466893323>
""")


@client.tree.command(name="version", description="Shows the bot's version")
async def version(interaction: discord.Interaction):
    global commands_ran
    commands_ran += 1
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send(f"I'm running `{settings['VERSION']}` version")

@client.command(name='dsc-cmds-sync')
async def dsc_cmds_sync(ctx):
     await ctx.reply('Syncing...')
     await client.tree.sync()
     await ctx.reply('<:checkmark:1155750377178804286> Synced!')


@client.tree.command(name="get-user", description="Get user info from Roblox")
async def get_user(interaction: discord.Interaction, user: str):
    global commands_ran
    commands_ran += 1
    if RoConnected == True:
        try:
            rouser = await RoClient.get_user_by_username(user)
        except UserNotFound:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("User not found")
            rouser = NotFound
        if rouser != NotFound: 
            if rouser.description == '':
               desc = '*None*'
            else:
                desc = rouser.description
        
            emb = discord.Embed(title='User Info', description=f"[{rouser.name} Roblox Profile](https://www.roblox.com/users/{rouser.id}/profile)", colour=GREYPLE)
            if rouser.is_banned == True:
                emb.add_field(name="Account Terminated", value=' ', inline=True)
            emb.add_field(name="Username", value=rouser.name, inline=False)
            emb.add_field(name="Display Name", value=rouser.display_name, inline=False)
            emb.add_field(name="ID", value=rouser.id, inline=True)
            created = f'<t:{str(rouser.created.timestamp())[0:10]}>'
            emb.add_field(name="Join date", value=f"{created}", inline=True)

            if rouser.description == '':
                desc = '*None*'
            else:
                desc = rouser.description
            emb.add_field(name="Description", value=desc, inline=False)
            presence = await rouser.get_presence()
            if presence.user_presence_type == 0:
                 status = 'Offline'
            elif presence.user_presence_type == 1:
                 status = 'Online'
            elif presence.user_presence_type == 2:
                 status = 'In Game'
            elif presence.user_presence_type == 3:
                 status = 'In Studio'
            else:
                 status = '*Unknown*'
            has_premium_raw = await rouser.has_premium()
            if has_premium_raw == True:
                 has_premium = 'Yes'
            else:
                 has_premium = 'No'
            emb.add_field(name='Has Premium?', value=has_premium)
            followers = await rouser.get_follower_count()
            emb.add_field(name="Followers", value=followers, inline=True)
            emb.add_field(name="Status", value=status, inline=True)
            if presence.user_presence_type > 0:
                last_online_raw = "Right now"
            else:
                last_online_raw = f'<t:{str(presence.last_online.timestamp())[0:10]}>'
            if last_online_raw == created:
                last_online = '*Unknown*'
            else:
                last_online = last_online_raw
                
            
            emb.add_field(name="Last online", value=f"{last_online}", inline=True)
            user_thumbnails = await RoClient.thumbnails.get_user_avatar_thumbnails(
                users=[rouser],
                type=AvatarThumbnailType.full_body,
                size=(720, 720)
            )
            if len(user_thumbnails) > 0:
                user_thumbnail = user_thumbnails[0]
                emb.set_image(url=user_thumbnail.image_url)
            await interaction.response.defer(ephemeral=False, thinking=True)
            await interaction.followup.send(embed=emb)
        else:
            return
    else:
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("I could not connect to Roblox. Please contact my developer. (<@1006501114419630081>)")

@client.tree.command(name='get-user-via-discord', description='Get user info via Discord')
async def get_user_via_discord(interaction: discord.Interaction, user: discord.Member):
    get_user_raw1 = db.find({"discordID": f"{user.id}"})
    get_user_raw2 = get_user_raw1.distinct(key="robloxID")
    get_user_raw3 = ''.join(get_user_raw2)
    get_user_id = get_user_raw3.replace("'", "")
    rouser = await RoClient.get_user(user_id=get_user_id)
    if rouser.description == '':
           desc = '*None*'
    else:
        desc = rouser.description
        
    emb = discord.Embed(title='User Info', description=f"[{rouser.name} Roblox Profile](https://www.roblox.com/users/{rouser.id}/profile)", colour=GREYPLE)
    if rouser.is_banned == True:
        emb.add_field(name="Account Terminated", value=' ', inline=True)
    emb.add_field(name="Username", value=rouser.name, inline=False)
    emb.add_field(name="Display Name", value=rouser.display_name, inline=False)
    emb.add_field(name="ID", value=rouser.id, inline=True)
    created = f'<t:{str(rouser.created.timestamp())[0:10]}>'
    emb.add_field(name="Join date", value=f"{created}", inline=True)

    if rouser.description == '':
        desc = '*None*'
    else:
        desc = rouser.description
    emb.add_field(name="Description", value=desc, inline=False)
    presence = await rouser.get_presence()
    if presence.user_presence_type == 0:
         status = 'Offline'
    elif presence.user_presence_type == 1:
         status = 'Online'
    elif presence.user_presence_type == 2:
         status = 'In Game'
    elif presence.user_presence_type == 3:
         status = 'In Studio'
    else:
         status = '*Unknown*'
    has_premium_raw = await rouser.has_premium()
    if has_premium_raw == True:
         has_premium = 'Yes'
    else:
         has_premium = 'No'
    emb.add_field(name='Has Premium?', value=has_premium)
    followers = await rouser.get_follower_count()
    emb.add_field(name="Followers", value=followers, inline=True)
    emb.add_field(name="Status", value=status, inline=True)
    if presence.user_presence_type > 0:
        last_online_raw = "Right now"
    else:
        last_online_raw = f'<t:{str(presence.last_online.timestamp())[0:10]}>'
    if last_online_raw == created:
        last_online = '*Unknown*'
    else:
        last_online = last_online_raw
                
            
    emb.add_field(name="Last online", value=f"{last_online}", inline=True)
    user_thumbnails = await RoClient.thumbnails.get_user_avatar_thumbnails(
        users=[rouser],
        type=AvatarThumbnailType.full_body,
        size=(720, 720)
    )
    if len(user_thumbnails) > 0:
        user_thumbnail = user_thumbnails[0]
        emb.set_image(url=user_thumbnail.image_url)
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send(embed=emb)


@client.tree.command(name='get-members', description='How many members in group')
async def get_members(interaction: discord.Interaction):
    group = await RoClient.get_group(group_id=16965138)
    members = await group.get_members().flatten()
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send(f'There are `{len(members)}` members in the group')

    
@client.command()
async def db_create_entry(ctx, discordID: int, robloxID: int, username: str):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        entry = {
            "username": f"{username}",
            "discordID": f"{discordID}",
            "robloxID": f"{robloxID}"
        }    
        post_id = db.insert_one(entry).inserted_id
        await ctx.reply(f'Created new entry with ID `{post_id}`')
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;db_create_entry` command, but they had no sufficient perms")


@client.command()
async def db_delete_entry(ctx, discordID: int):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        cur = db.find({"discordID": f"{discordID}"})
        if len(cur.distinct(key="robloxID")) > 0:
            is_there = True
        else:
            is_there = False
        if is_there == True:
            resp = db.find_one_and_delete({"discordID": f"{discordID}"})
            await ctx.reply(f'Deleted entry successfully')
        else:
            await ctx.reply('Could not find specified entry')
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;db_delete_entry` command, but they had no sufficient perms")















































































































































































if run_nightly == True:
	DISTOKEN = settings['NIGHTLY_TOKEN']
else:
	DISTOKEN = settings['TOKEN']

client.run(DISTOKEN)