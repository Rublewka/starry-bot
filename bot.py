import discord
from discord.ext import commands
from config import settings

prefix = settings['PREFIX']

client = commands.Bot(command_prefix = settings['PREFIX'], intents=discord.Intents.all())

client.remove_command('help') 

@client.event
async def on_ready(): 

    print (f"Logged on as {settings['NAME BOT']}") # bot-readiness

    await client.change_presence(status=discord.Status.dnd) #bot-status
# Ping
@client.command(aliases = ['Ping', 'PING', 'pING', 'ping'])
#@client.command - объявление команды | (aliases = ['Ping', 'PING' ...]) - Альтернативное название команды
async def __ping(ctx): # Объявление асинхронной функции __ping с возможностью публикации сообщения
    ping = client.ws.latency # Получаем пинг клиента

    ping_emoji = '🟩🔳🔳🔳🔳' # Эмоция пинга, если он меньше 100ms

    if ping > 0.10000000000000000:
        ping_emoji = '🟧🟩🔳🔳🔳' # Эмоция пинга, если он больше 100ms

    if ping > 0.15000000000000000:
        ping_emoji = '🟥🟧🟩🔳🔳' # Эмоция пинга, если он больше 150ms

    if ping > 0.20000000000000000:
        ping_emoji = '🟥🟥🟧🟩🔳' # Эмоция пинга, если он больше 200ms

    if ping > 0.25000000000000000:
        ping_emoji = '🟥🟥🟥🟧🟩' # Эмоция пинга, если он больше 250ms

    if ping > 0.30000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟧' # Эмоция пинга, если он больше 300ms

    if ping > 0.35000000000000000:
        ping_emoji = '🟥🟥🟥🟥🟥' # Эмоция пинга, если он больше 350ms

    message = await ctx.send('Пожалуйста, подождите. . .') # Переменная message с первоначальным сообщением
    await message.edit(content = f'Понг! {ping_emoji} `{ping * 1000:.0f}ms` :ping_pong:') # Редактирование первого сообщения на итоговое (На сам пинг)
    print(f'[Logs:utils] Пинг сервера был выведен | {prefix}ping') # Информация в консоль, что команда "ping" была использована
    print(f'[Logs:utils] На данный момент пинг == {ping * 1000:.0f}ms | {prefix}ping') # Вывод пинга в консоль
    #Итог: https://prnt.sc/uogljj

# Help
@client.command(aliases = ['Help', 'help', 'HELP', 'hELP', 'хелп', 'Хелп', 'ХЕЛП', 'хЕЛП'])
async def __help (ctx):
    emb = discord.Embed( title = 'ДОСТУПНЫЕ КОМАНДЫ:', description = 'ВНИМАНИЕ! Бот ещё в разработке!', colour = discord.Color.red() )
     title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски

    emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
    # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
    emb.add_field( name = 'Информация', value = f'`{prefix}хелп` `{prefix}инфо` `{prefix}сервер` `{prefix}профиль` `{prefix}авторы` ', inline=False)
    emb.add_field( name = 'Модерирование', value = f'`{prefix}мут` `{prefix}размут` `{prefix}бан` `{prefix}кик` `{prefix}очистить` ', inline=False)
    # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name" | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False - Блоки текста будут один под другим (https://prnt.sc/uogx3t)
    emb.set_thumbnail(url = client.user.avatar_url)
     emb.set_thumbnail - Добавляет картинку около текста (Например: emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/elegantthemes/beautiful-flat-one-color/128/unlocked-icon.png") (NOAD) добавит картинку замка (https://prnt.sc/uogztb)) | client.user.avatar_url - Отображает аватарку бота
    emb.set_footer( icon_url = client.user.avatar_url, text = f'{client.user.name} © Copyright 2020 | Все права защищены' )
     emb.set_thumbnail - Добавляет картинку под текстом | client.user.avatar_url - Аватарка бота | ctx.guild.name - Имя сервера

    await ctx.send ( embed = emb)
    # Отправляет сообщение и так же преобразует emb в embed

    print(f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ')
    # Информация, что команда "help" была использована
    # Итог: https://prnt.sc/uoh6v6

# Добавление аргументов асинхронной функции, реакции на сообщение:
#Kick
@client.command(aliases = ['Kick', 'kICK', 'KICK', 'kick'])
@commands.has_permissions ( administrator = True ) # Команда только для пользователей имеющих роль с правами "Администратор"
async def __kick(ctx, member: discord.Member, *, reason = None): # Асинхронная функция __kick(ctx, member: discord.Member, *, reason = None)
    #Аргументы: ctx - отправка сообщения с помощью команды (Обязательно)
    #Аргументы: member: discord.Member - "member" ----- может быть любой текст, но для удобства использую member (Discord.Member - для получения id указанного пользователя)
    #Аргументы: * - предыдущий аргумент необходим
    #Аргументы: reason = None - "reason" ----- может быть любой текст, но для удобства использовал reason, "None" - значение по умолчанию
    await ctx.message.add_reaction('✅') # Добавляет реакцию к сообщению с командой
    await member.kick( reason = reason ) # Кикнуть пользователя по причине (Преобразует причину бота в причину дискорда)
    emb = discord.Embed( title = 'Kicked', description = f'Пользователь {member}  был кикнут по причине { reason } ', colour = discord.Color.red() )
    emb.set_author( name = client.user.name )
    emb.set_footer( text = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_thumbnail(url = client.user.avatar_url)

    await ctx.send( embed = emb )

    print(f'[Logs:moderation] Пользователь {member} был кикнут по причине {reason} | {prefix}kick ')
    # Итог: https://prnt.sc/uohdqh

@__kick.error
async def kick_error(ctx, goodbye):
	if isinstance ( goodbye, commands.MissingRequiredArgument):
		emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'Использование', value = "!кик <@⁣Участник | ID>", inline=False)
		emb.add_field( name = 'Пример', value = "`!кик @⁣Участник`\n┗ Кикнет указаного участника.", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = client.user.avatar_url, text = f"{settings['OWNER NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:error] Необходимо указать участника | {prefix}kick")

	if isinstance (goodbye, commands.MissingPermissions):
		emb = discord.Embed( title = f'**Команда "{prefix}кик"**', description = f'Изгоняет указаного участника с сервера с возможностью возвращения ', colour = discord.Color.red() )
		emb.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
		emb.add_field( name = 'ОШИБКА!', value = "У вас недостаточно прав!", inline=False)
		emb.set_thumbnail(url = client.user.avatar_url)
		emb.set_footer( icon_url = client.user.avatar_url, text = f"{settings['OWNER NAME']} © Copyright 2020 | Все права защищены"   )
		await ctx.send ( embed = emb)
		print(f"[Logs:Error] [Ошибка доступа] Пользователь [{ctx.author}] попытался кикнуть | {prefix}kick")














































































































































































































client.run (settings['TOKEN']) #Убираем в самый конец файла и больше не трогаем