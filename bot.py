from bson import ObjectId
import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['1.1.1.1', '1.0.0.1']
import json
import os
import os.path
import asyncio
import datetime
import random
import discord
import requests
import logging
from logging import *
from discord import app_commands
from roblox import AvatarThumbnailType
from src.verif_words import verification_words
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Button, View
from roblox import Client
from roblox.utilities.exceptions import *
from config import settings
import urllib.request
prefix = settings['PREFIX']

client = commands.Bot(command_prefix = commands.when_mentioned_or(settings['PREFIX']), intents=discord.Intents.all())
client.remove_command('help') 
load_dotenv()

run_nightly = bool(os.getenv("RUN_NIGHTLY"))         
db_token = os.getenv("DBTOKEN")


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://starry_bot:TPth5ILO9WiJUcKU@rublewka-bot.b7dexs8.mongodb.net/?retryWrites=true&w=majority"
dbclient = MongoClient(uri, server_api=ServerApi('1'))
db = dbclient.starry_bot


async def status_push():
    while True:
        ping = f'{client.ws.latency * 1000:.0f}'
        push_url = f"https://status.immosmp.ru/api/push/MAgoOEp31tOPbEuhLctE6hi4VNsAEKlW?status=up&msg=OK&ping={ping}"
        interval = 40
        r = requests.get(url=push_url)
        await asyncio.sleep(interval)

ro_token = db.env.find_one({"_id": ObjectId('65ba990cab2d2b68695abb85')})
ROBLOSECURITY = str(ro_token.get('ROBLOSECURITY'))

RoClient = Client(token=ROBLOSECURITY)
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
    client.loop.create_task(status_push())
    print(f"Starting up {client.user.name}#{client.user.discriminator}")
    print(f"--Discord--")
    print(f"Bot Name:  {client.user.name}")
    print(f"Bot ID:  {client.user.id}")
    print(f"Bot Version:  {settings['VERSION']}")
    print(f"Discord session successfully initialized")
    print(f"--Roblox--")
    global start_time
    start_time = datetime.datetime.now()
    def roconnect():
        try:
            r = requests.head("https://auth.roblox.com")
            return r.status_code
        except requests.ConnectionError:
            warning("Failed to connect")
            return None
    if roconnect() == 200:
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
        warning(f'`Could not connect to Roblox API. Try again later`')
        warning(f"Roblox session could not fully initialize")
        RoConnected = False

        

    





# startup end

# variables section

commands_ran = 0

rvr_token = 'rvr2b087uhj4acpftd2hgnya450sqjoar2lce6wk9mppsiy59f80uxuc37tvsuh99cef'
blx_token = 'd28965c0-dce1-40ef-99de-a5411b32e5b4'

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

@client.tree.command(name='update', description='Update user\'s roles and nick in this server')
async def user_update(interaction: discord.Interaction):
    user = interaction.user
    alr_verified_raw1 = db.users.find({"discordID": f"{user.id}"})
    alr_verified_raw2 = alr_verified_raw1.distinct(key="robloxID")
    alr_verified_raw3 = ''.join(alr_verified_raw2)
    alr_verified = alr_verified_raw3.replace("'", "")
    try:
        rouser = await RoClient.get_user(user_id=alr_verified)
        rouser_found = True
    except UserNotFound:
        rouser_found = False
    role_casual = interaction.guild.get_role(1155893908501442702)
    role_above = interaction.guild.get_role(1155894250010050601)
    role_admin = interaction.guild.get_role(1155894433250811984)
    if rouser_found:
        group_id = 16965138
        roles = await rouser.get_group_roles()
        role = None
        for test_role in roles:
            if test_role.group.id == group_id:
                role = test_role.rank
                break
        emb = discord.Embed(title='Update Complete')
        if rouser.display_name != rouser.name:
            nick = f'{rouser.display_name} ({rouser.name})'
        else:
            nick = f'{rouser.name}'
        match role:
            case 1:
                try:
                    await user.edit(nick=nick)
                    await user.add_roles(role_casual)
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155893908501442702>')
                except discord.Forbidden:
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155893908501442702>')
                    emb.add_field(name='Error', value='Some roles or username failed to process (403)')
                await interaction.response.send_message(embed=emb)
            case 75:
                try:
                    await user.edit(nick=nick)
                    await user.add_roles(role_above)
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155894250010050601>')
                except discord.Forbidden:
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155894250010050601>')
                    emb.add_field(name='Error', value='Some roles or username failed to process (403)')
                await interaction.response.send_message(embed=emb)
            case 150:
                try:
                    await user.edit(nick=nick)
                    await user.add_roles(role_admin)
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155894433250811984>')
                except discord.Forbidden:
                    emb.add_field(name='Username', value=f'{nick}', inline=False)
                    emb.add_field(name='Role added', value='<@&1155894433250811984>')
                    emb.add_field(name='Error', value='Some roles or username failed to process (403)')
                await interaction.response.send_message(embed=emb)
            


            

@client.tree.command(name='verify', description='Link your Roblox account with Discord account')
async def verify(interaction: discord.Interaction, username: str):
    alr_verified_raw1 = db.users.find({"discordID": f"{interaction.user.id}"})
    alr_verified_raw2 = alr_verified_raw1.distinct(key="robloxID")
    alr_verified_raw3 = ''.join(alr_verified_raw2)
    alr_verified = alr_verified_raw3.replace("'", "")
    if len(alr_verified) == 0:
        button_ingame = Button(label='Game (Recommended)', custom_id='ingame', style=discord.ButtonStyle.green)
        button_desc = Button(label='Profile Description', custom_id='desc', style=discord.ButtonStyle.blurple)
        button_thirdparty = Button(label='Third party', style=discord.ButtonStyle.blurple)
        async def verify_ingame(interaction=interaction):
            try:
                rouser = await RoClient.get_user_by_username(username=username)
                rouser_found = True
            except UserNotFound:
                await interaction.response.edit_message(content=f'Could\'t find specified user `{username}` \nTry again!', view=None)
                rouser_found = False
            if rouser_found:
                emb = discord.Embed(title='Check your account info')
                emb.add_field(name='Username', value=f'{rouser.name}')
                if rouser.description == '':
                    desc = '*None*'
                else:
                    desc = rouser.description
                emb.add_field(name='Description', value=f'{desc}')
                emb.add_field(name='ID', value=f'{rouser.id}')
                user_thumbnails = await RoClient.thumbnails.get_user_avatar_thumbnails(
                    users=[rouser],
                    type=AvatarThumbnailType.full_body,
                    size=(720, 720)
                    )
                if len(user_thumbnails) > 0:
                    user_thumbnail = user_thumbnails[0]
                    emb.set_image(url=user_thumbnail.image_url)
                created = f'<t:{str(rouser.created.timestamp())[0:10]}>'
                emb.add_field(name='Joined platform', value=f'{created}')
            
                button_me = Button(label='It\'s me', custom_id='button_me', style=discord.ButtonStyle.green)
                button_notme = Button(label='No, It\'s not me', custom_id='button_notme', style=discord.ButtonStyle.danger)
            async def verif_ingame_notme(interaction=interaction):
                await interaction.response.edit_message(content=f"Verification cancelled. Try again", view=None, embed=None)
            async def verif_ingame_me(interaction=interaction):
                db_verif = db.pending_verifications
                entry = {
                    "username": f"{rouser.name}",
                    "discordUsername": f"{interaction.user.name}",
                    "discordID": f"{interaction.user.id}",
                    "robloxID": f"{rouser.id}",
                    "confirmed": "False"
                }
                db_verif.insert_one(entry)

                async def verif_ingame_done(interaction=interaction):
                    done_check_raw = db_verif.find({"discordID": f"{interaction.user.id}"})
                    done_check = ''.join(done_check_raw.distinct(key="confirmed"))
                    if done_check == 'True':
                        entry = {
                            "username": f"{rouser.name}",
                            "discordID": f"{interaction.user.id}",
                            "robloxID": f"{rouser.id}"
                            }
                        db.users.insert_one(entry)
                        if rouser.display_name != rouser.name:
                            nick = f'{rouser.display_name} ({rouser.name})'
                        else:
                            nick = f'{rouser.name}'
                        try:
                            await interaction.user.edit(nick=f'{nick}')
                            await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}**', view=None)
                            role = interaction.guild.get_role(1094687628357537852)
                            await interaction.user.add_roles(role)
                        except discord.Forbidden:
                            await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}** \nSomething went wrong while updating your nickname and roles (403); ping an online <@&1094687621411786772>', view=None)
                        db_verif.find_one_and_delete({"discordID": f"{interaction.user.id}"})
                    elif done_check == 'Cancelled':
                        await interaction.response.edit_message(content='Verification was cancelled ingame', view=None)
                        db_verif.find_one_and_delete({"discordID": f"{interaction.user.id}"})
                    else:
                        await interaction.response.edit_message(content='Couldn\'t verify you, please try again..', view=None)
                        db_verif.find_one_and_delete({"discordID": f"{interaction.user.id}"})
                button_done = Button(label='Done', style=discord.ButtonStyle.green)
                button_done.callback = verif_ingame_done    
                view = View()
                view.add_item(button_done)
                await interaction.response.edit_message(content='Join [this](https://www.roblox.com/games/15055138791/Starry-Bot-Verification-Place) game and follow instructions in there', view=view, embed=None)
                
            button_me.callback = verif_ingame_me
            button_notme.callback = verif_ingame_notme
            view = View()
            view.add_item(button_me)
            view.add_item(button_notme)
            await interaction.response.edit_message(content=None, view=view, embed=emb)

        async def verify_desc(interaction=interaction):
            try:
                rouser = await RoClient.get_user_by_username(username=username)
                rouser_found = True
            except UserNotFound:
                await interaction.response.edit_message(content=f'Could\'t find specified user `{username}` \nTry again!', view=None)
                rouser_found = False
            if rouser_found:
                emb = discord.Embed(title='Check your account info')
                emb.add_field(name='Username', value=f'{rouser.name}')
                if rouser.description == '':
                    desc = '*None*'
                else:
                    desc = rouser.description
                emb.add_field(name='Description', value=f'{desc}')
                emb.add_field(name='ID', value=f'{rouser.id}')
                user_thumbnails = await RoClient.thumbnails.get_user_avatar_thumbnails(
                    users=[rouser],
                    type=AvatarThumbnailType.full_body,
                    size=(720, 720)
                    )
                if len(user_thumbnails) > 0:
                    user_thumbnail = user_thumbnails[0]
                    emb.set_image(url=user_thumbnail.image_url)
                created = f'<t:{str(rouser.created.timestamp())[0:10]}>'
                emb.add_field(name='Joined platform', value=f'{created}')
            
                button_me = Button(label='It\'s me', custom_id='button_me', style=discord.ButtonStyle.green)
                button_notme = Button(label='No, It\'s not me', custom_id='button_notme', style=discord.ButtonStyle.danger)
                async def verif_desc_notme(interaction=interaction):
                    await interaction.response.edit_message(content=f"Verification cancelled. Try again", view=None, embed=None)
                async def verif_desc_me(interaction=interaction):
                    for i in range(1):
                        verif_words_raw = random.choices(verification_words, k=6)
                        verif_words = ', '.join(verif_words_raw)
                    async def verif_desc_done(interaction=interaction):
                        rouser = await RoClient.get_user_by_username(username=username)
                        if verif_words in rouser.description:
                            entry = {
                            "username": f"{rouser.name}",
                            "discordID": f"{interaction.user.id}",
                            "robloxID": f"{rouser.id}"
                            }    
                            db.users.insert_one(entry)
                            if rouser.display_name != rouser.name:
                                nick = f'{rouser.display_name} ({rouser.name})'
                            else:
                                nick = f'{rouser.name}'
                            try:
                                await interaction.user.edit(nick=f'{nick}')
                                await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}**', view=None)
                                role = interaction.guild.get_role(1094687628357537852)
                                await interaction.user.add_roles(role)
                            except discord.Forbidden:
                                await interaction.response.edit_message(content=f'Successfully verified you as {rouser.name} \nSomething went wrong while updating your nickname and roles (403); ping an online <@&1094687621411786772>', view=None)
                    
                    button_done = Button(label='Done', style=discord.ButtonStyle.green)
                    button_done.callback = verif_desc_done
                    view = View()
                    view.add_item(button_done)
                    await interaction.response.edit_message(content=f'Paste these words into your Roblox profile description \n`{verif_words}`', view=view, embed=None)

                button_me.callback = verif_desc_me
                button_notme.callback = verif_desc_notme
                view = View()
                view.add_item(button_me)
                view.add_item(button_notme)

                await interaction.response.edit_message(content=None, embed=emb, view=view)

        async def verify_third_party(interaction=interaction):
            button_thirdparty_rover = Button(label='RoVer')
            button_thirdparty_bloxlink = Button(label='Bloxlink')
            async def verify_thirdparty_rover(interaction=interaction):
                r = requests.get(
                                f'https://registry.rover.link/api/guilds/1018415075255668746/discord-to-roblox/{interaction.user.id}',
                                headers={'Authorization': f'Bearer {rvr_token}'},
                                timeout=10)
                data = r.json()
                json_str = json.dumps(data)
                resp = json.loads(json_str)
                if 'robloxId' in resp:
                    try:
                        rouser = await RoClient.get_user(user_id=resp['robloxId'])
                        ro_found = True
                    except UserNotFound:
                        ro_found = False
                        await interaction.response.edit_message(content='Couldn\'t find your Roblox account via RoVer, try again', view=None)
                else:
                    ro_found = False
                    await interaction.response.edit_message(content='Couldn\'t find your Roblox account via RoVer, try again', view=None)
                if ro_found:
                    entry = {
                            "username": f"{rouser.name}",
                            "discordID": f"{interaction.user.id}",
                            "robloxID": f"{rouser.id}"
                            }    
                    db.users.insert_one(entry)
                    if rouser.display_name != rouser.name:
                        nick = f'{rouser.display_name} ({rouser.name})'
                    else:
                        nick = f'{rouser.name}'
                    try:
                        await interaction.user.edit(nick=f'{nick}')
                        await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}**', view=None)
                        role = interaction.guild.get_role(1094687628357537852)
                        await interaction.user.add_roles(role)
                    except discord.Forbidden:
                        await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}** \nSomething went wrong while updating your nickname and roles (403); ping an online <@&1094687621411786772>', view=None)
            async def verify_thirdparty_bloxlink(interaction=interaction):
                r = requests.get(
                                f'https://api.blox.link/v4/public/guilds/1018415075255668746/discord-to-roblox/{interaction.user.id}',
                                headers={'Authorization': f'{blx_token}'},
                                timeout=10)
                data = r.json()
                json_str = json.dumps(data)
                resp = json.loads(json_str)
                if 'robloxID' in resp:    
                    try:
                        rouser = await RoClient.get_user(user_id=resp['robloxID'])
                        ro_found = True
                    except UserNotFound:
                        ro_found = False
                        await interaction.response.edit_message(content='Couldn\'t find your Roblox account via Bloxlink, try again', view=None)
                else:
                    ro_found = False
                    await interaction.response.edit_message(content='Couldn\'t find your Roblox account via Bloxlink, try again', view=None)

                if ro_found:
                    entry = {
                            "username": f"{rouser.name}",
                            "discordID": f"{interaction.user.id}",
                            "robloxID": f"{rouser.id}"
                            }    
                    db.users.insert_one(entry)
                    if rouser.display_name != rouser.name:
                        nick = f'{rouser.display_name} ({rouser.name})'
                    else:
                        nick = f'{rouser.name}'
                    try:
                        await interaction.user.edit(nick=f'{nick}')
                        await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}**', view=None)
                        role = interaction.guild.get_role(1094687628357537852)
                        await interaction.user.add_roles(role)
                    except discord.Forbidden:
                        await interaction.response.edit_message(content=f'Successfully verified you as **{rouser.name}** \nSomething went wrong while updating your nickname and roles (403); ping an online <@&1094687621411786772>', view=None)

            button_thirdparty_rover.callback = verify_thirdparty_rover
            button_thirdparty_bloxlink.callback = verify_thirdparty_bloxlink
            view = View()
            view.add_item(button_thirdparty_rover)
            view.add_item(button_thirdparty_bloxlink)
            await interaction.response.edit_message(content='Choose Third Party provider below', view=view)
        button_ingame.callback = verify_ingame
        button_desc.callback = verify_desc
        button_thirdparty.callback = verify_third_party
        view = View()
        view.add_item(button_ingame)
        view.add_item(button_desc)
        view.add_item(button_thirdparty)
        await interaction.response.send_message(f'# Hello, welcome to verification! You are verifying as **`{username}`** \n## Please choose verification method below', ephemeral=True, view=view)
    else:
        rouser = await RoClient.get_user(user_id=alr_verified)
        button = Button(label='Reverify')
        await interaction.response.send_message(f'You are already verified as `{rouser.name}`')


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
        os.system("sudo reboot")
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687620564529283>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;deploy` command, but they had no sufficient perms")

@client.command(name="restart")
async def restart(ctx):
    if any(role.id in [1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        os.system("sudo reboot")
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
        dbclient.admin.command('ping')
        db_connected_raw = True
    except Exception:
        db_connected_raw = False
    temp = "N/A"
#    try:
#        with open(r"/sys/class/thermal/thermal_zone0/temp") as File:
#            temp = File.readline()
#    except:
#        CurrentTemp = "N/A"
    # Define the green bar emoji as the default
    ping_emoji = '<:starry_gudping:1171806377371521095>' # 100ms
    
    # Check if ping is greater than 250ms and if so, update the emoji
    if ping > 0.25000000000000000:
        ping_emoji = '<:starry_medping:1171806470552174603>' # 250ms

    # Check if ping is greater than 400ms and if so, update the emoji
    if ping > 0.40000000000000000:
        ping_emoji = '<:starry_badping:1171806521823342664>' # 400ms
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
        con = "<:starry_online:1171807873458770003> Connected to Roblox API"
    elif RoConnected == None:
        con = "<:starry_warn:1171811103714586674> The bot haven\'t properly initialized, please contact bot developer"
    else:
        con = "<:starry_outage:1171807914323878020> Not connected to Roblox API"
    if db_connected_raw == True:
        db_connected = "<:starry_online:1171807873458770003> Connected to Database Services"
    else:
        db_connected = "<:starry_outage:1171807914323878020> Not connected to Database Services"
    emb = discord.Embed(title="Bot Status", description=None, color=BLUE)
    emb.add_field(name="Latency", value=f"{ping_emoji} `{ping * 1000:.0f}ms`", inline=False)
    emb.add_field(name="Roblox API", value=f"{con}", inline=False)
    emb.add_field(name="Database Connection", value=db_connected, inline=False)
    emb.add_field(name="Uptime", value=f"<:starry_clock:1113391359274000394> {clock}", inline=False)

    emb.add_field(name="Commands ran this session", value=f"<:starry_cmd:1171807971274149908> I've ran `{commands_ran}` command(s) this session.", inline=False)
    emb.add_field(name="Version", value=f"`{settings['VERSION']}`", inline=False)
    await interaction.followup.send(embed=emb)
    commands_ran += 1



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


@client.tree.command(name="who-is-via-username", description="Get user info from Roblox by their username")
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

@client.tree.command(name='who-is-via-discord', description='Get user info via Discord')
async def get_user_via_discord(interaction: discord.Interaction, user: discord.Member):
    get_user_raw1 = db.users.find({"discordID": f"{user.id}"})
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

@client.tree.command(name='who-is-via-roblox', description='Get user verified with specified Roblox account')
async def who_is_via_discord(interaction: discord.Interaction, user: str):
    if user.isdigit() == True:
        try:
            rouser = await RoClient.get_user(user_id=user)
            rouser_found = True
        except UserNotFound:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await interaction.followup.send(f'Couldn\'t find specified user (`{user}`)')
            rouser_found = False
        if rouser_found:
            cur = db.users.find({"robloxID": f"{user}"})
            dscuser = cur.distinct(key="discordID")
            if len(dscuser) > 0:
                append_str1 = '<@'
                append_str2 = '>' 
                users1 = [append_str1 + sub + append_str2 for sub in dscuser]
                users = ', '.join(users1)
                emb = discord.Embed(title='User lookup via Roblox')
                emb.add_field(name=f'Following users verified as `{rouser.name}`', value=f'{users}')
                await interaction.response.defer(ephemeral=False, thinking=True)
                await interaction.followup.send(embed=emb)
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)
                await interaction.followup.send(f'Couldn\'t find anyone verified as `{rouser.name}`')
    elif user.isdigit() == False:
        try:
            rouser = await RoClient.get_user_by_username(username=user)
            rouser_found = True
        except UserNotFound:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await interaction.followup.send(f'Couldn\'t find specified user (`{user}`)')
            rouser_found = False
        
        if rouser_found :    
            cur = db.users.find({"robloxID": f"{rouser.id}"})
            dscuser = cur.distinct(key="discordID")
            if len(dscuser) > 0:
                append_str1 = '<@'
                append_str2 = '>' 
                users1 = [append_str1 + sub + append_str2 for sub in dscuser]
                users = ', '.join(users1)
                emb = discord.Embed(title='User lookup via Roblox')
                emb.add_field(name=f'Following users verified as `{rouser.name}`', value=f'{users}')
                await interaction.response.defer(ephemeral=False, thinking=True)
                await interaction.followup.send(embed=emb)
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)
                await interaction.followup.send(f'Couldn\'t find anyone verified as `{rouser.name}`')
    else:
        await interaction.response.defer(ephemeral=True, thinking=False)
        await interaction.followup.send('Please specify **Roblox username** or **ID**')


@client.tree.command(name='get-members', description='How many members in group')
async def get_members(interaction: discord.Interaction):
    group = await RoClient.get_group(group_id=16965138)
    members = await group.get_members().flatten()
    await interaction.response.defer(ephemeral=False, thinking=True)
    await interaction.followup.send(f'There are `{len(members)}` members in the group')

@client.command()
async def db_create_entry(ctx, discordID: int, robloxID: int, username: str):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        alr_verified_raw1 = db.users.find({"discordID": f"{discordID}"})
        alr_verified_raw2 = alr_verified_raw1.distinct(key="robloxID")
        alr_verified_raw3 = ''.join(alr_verified_raw2)
        alr_verified = alr_verified_raw3.replace("'", "")
        print(alr_verified)
        if len(alr_verified) == 0:
            entry = {
                "username": f"{username}",
                "discordID": f"{discordID}",
                "robloxID": f"{robloxID}"
            }    
            post_id = db.users.insert_one(entry).inserted_id
            await ctx.reply(f'Created new entry with ID `{post_id}`')
        else:
            await ctx.reply('Entry for this user already exists')
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;db_create_entry` command, but they had no sufficient perms")


@client.command()
async def db_delete_entry(ctx, discordID: int):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        cur = db.users.find({"discordID": f"{discordID}"})
        if len(cur.distinct(key="robloxID")) > 0:
            is_there = True
        else:
            is_there = False
        if is_there == True:
            resp = db.users.find_one_and_delete({"discordID": f"{discordID}"})
            await ctx.reply(f'Deleted entry successfully')
        else:
            await ctx.reply('Could not find specified entry')
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;db_delete_entry` command, but they had no sufficient perms")


@client.command()
async def db_get_entry(ctx, discordID: int):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in ctx.author.roles):
        cur = db.users.find({"discordID": f"{discordID}"})
        if len(cur.distinct(key="robloxID")) > 0:
            is_there = True
        else:
            is_there = False
        if is_there == True:
            dscID_raw1 = cur.distinct(key="discordID")
            dscID_raw2 = ''.join(dscID_raw1)
            dscID = dscID_raw2.replace("'", "")
            roID_raw1 = cur.distinct(key="robloxID")
            roID_raw2 = ''.join(roID_raw1)
            roID = roID_raw2.replace("'", "")
            roUSNM_raw1 = cur.distinct(key="username")
            roUSMN_raw2 = ''.join(roUSNM_raw1)
            roUSNM = roUSMN_raw2.replace("'", "")
            emb = discord.Embed(title='Database export')
            emb.add_field(name='Discord ID', value=f'{dscID}', inline=False)
            emb.add_field(name='Discord user', value=f'<@{dscID}>', inline=False)
            emb.add_field(name='Roblox ID', value=f'{roID}', inline=False)
            emb.add_field(name='Roblox Username', value=f'{roUSNM}', inline=False)
            await ctx.reply(embed=emb)
        else:
            await ctx.reply('Could not find specified entry')
    else:
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await ctx.reply(embed=emb)
        logging.info(f"@{ctx.author.name} tried to run `;db_get_entry` command, but they had no sufficient perms")  













@client.tree.command(name='gban', description='Ban user from server with database record')
async def gban(interaction: discord.Interaction, user: discord.Member, reason: str|None):
    if any(role.id in [1094687621411786772, 1094687620564529283, 1137847962186289184] for role in interaction.user.roles):
        get_user_raw1 = db.users.find({"discordID": f"{user.id}"})
        get_user_raw2 = get_user_raw1.distinct(key="robloxID")
        get_user_raw3 = ''.join(get_user_raw2)
        get_user_id = get_user_raw3.replace("'", "")
        db_bans = db.banned_users
        rouser = await RoClient.get_user(user_id=get_user_id)
        entry = {
            'username': f"{rouser.name}",
            'discordId': f"{user.id}",
            'robloxId': get_user_id,
            'reason': reason,
            'moderator': f"@{interaction.user.name}"
            }
        db_bans.insert_one(entry)
        await interaction.response.defer(ephemeral=False, thinking=False)
        

        user_dm = await user.create_dm()
        if reason:
            emb1 = discord.Embed(title="You have been banned in Immortals Squad")
            emb1.add_field(name='Reason', value=f"{reason}")
            emb1.add_field(name='Moderator', value=f"<@{interaction.user.id}>", inline=False)
            emb2 = discord.Embed(title=f"User `@{user.name}` has been banned")
            emb2.add_field(name='Reason', value=f"{reason}")
            emb2.add_field(name='Moderator', value=f"<@{interaction.user.id}>", inline=False)
            await user_dm.send(embed=emb1)
            await interaction.followup.send(embed=emb2)
        else:
            emb1 = discord.Embed(title="You have been banned in Immortals Squad")
            emb1.add_field(name='Reason', value="*`No reason provided`*")
            emb1.add_field(name='Moderator', value=f"<@{interaction.user.id}>", inline=False)
            emb2 = discord.Embed(title=f"User `@{user.name}` has been banned")
            emb2.add_field(name='Reason', value="*`No reason provided`*")
            emb2.add_field(name='Moderator', value=f"<@{interaction.user.id}>", inline=False)
            await user_dm.send(embed=emb1)
            await interaction.followup.send(embed=emb2)
    else:
        await interaction.response.defer(ephemeral=True, thinking=False)
        emb = discord.Embed(title="Uh-uh", colour=RED)
        emb.add_field(name="Access Denied!", value="Minimum rank required to run this command: <@&1094687621411786772>")
        await interaction.followup.send(embed=emb)
        logging.info(f"@{interaction.user.name} tried to run `/gban` command, but they had no sufficient perms")



#TODO facts
#TODO moderation




































































































































































if run_nightly == True:
    DISTOKEN = settings['NIGHTLY_TOKEN']
else:
	DISTOKEN = settings['TOKEN']

client.run(DISTOKEN)
