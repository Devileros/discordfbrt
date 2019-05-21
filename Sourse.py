import discord, asyncio, time, json, os
from discord.ext import commands
from discord.ext.commands import Bot

muterole_name = 'Muted' # Название роли, которая будет выдаватся замученным людям
warned_role = 'Warned'

report_file = 580126546568675354  # int. Вставить id канала репортов, обязательно

logfile = 580126398384177152 # int. Вставить id канала логов, обязательно
botid = 579976940996395028 # int. Вставить id бота, обязательно
token = "NTc5OTc2OTQwOTk2Mzk1MDI4.XOQu-Q.qIxL29sWrXs90Y6VWzs2uvRZIPY"  # Тут надо вставить свой токен, его можно узнать на https://discordapp.com/developers/applications/

msg_cnt = """Приветствуем вас на сервере!!!\nДомик Котика, это место куда вы попали. Домик Котика - Кошачий дом, где каждый может найти себе кошку или же кота""" # Сообщение которое будет писатся при заходе на сервер в лс

colors = [0xFF0000, 0x9102f0, 0x00FF00]

channellis = [579456506794213397, 579445102284374026,579408546781724675, 579444096075169792, 579444141386104833, 579444203919245322, 579430751682953231, 579430894352203786, 579412799017582602, 579413084901212170, 579412873953148969, 579413003049631767, 579412943209234613, 579436825337397268, 579747836233646091, 579748173917192226, 579742381490962462, 579762985900310550, 579432556248694812, 579432593745772545, 579432636053717022, 579414211789193226, 579414372682825730, 579449892057907215, 579413594161152019] # Каналы которых надо подсчитать

allsch = 580088129231388703

prefix = 'n/' # Знак который будет перед коммандой, можно изменить
Bot = commands.Bot(command_prefix= prefix) # Выставление префикса коммандам
Bot.remove_command("help") # Удаление стоковой команды help

@Bot.event
async def on_member_join(member): # Когда человек зайдет, ему в ЛС отправится сообщение
	role = discord.utils.get(member.guild.roles, name= 'Новенький')
	await member.add_roles(role)
	msg = discord.Embed(title= "Привет!", description= msg_cnt, color= colors[0]) # Создание рамки
	await member.send(embed= msg) # отправка рамки


@Bot.event
async def on_message(message): # лог обычных сообщений
	await Bot.process_commands(message) # Проверяет, если сообщение это команда, то команда все равно выполнится
	channel = Bot.get_channel(logfile) # Поиск канала с id который вы указали выше
	if message.guild is None: # Проверяет, отправленно сообщение с сервера, или в ЛС боту
		pass
	else:
		if message.author.id == botid: # Проверяет, автор бот? Что-бы небыло спама и зацикливания, логи логов не делаюстся, так же как и сообщения бота
			pass
		else:
			msg_embed = discord.Embed(title="Send message", description=f'**Пользователь:**\n<@{message.author.id}>  `ID: {message.author.id}`\n\n**Канал:**\n<#{message.channel.id}>\n\n**Сообщение:**\n`{message.content}`', colour= colors[1]) # Создание рамки
			msg_embed.set_footer(text=message.created_at.strftime('%Y.%m.%d-%H:%M:%S')) # Присоединение таблички с временем создания сообщения
			await channel.send(embed= msg_embed) # отправка таблички
		
@Bot.event
async def on_message_delete(message): # Лог удаления сообщений
	channel = Bot.get_channel(logfile) # Поиск канала с id который вы указали выше
	if message.guild is None: # Проверяет, отправленно сообщение с сервера, или в ЛС боту
		pass
	else:
		if message.author.id == botid: # Проверяет, автор бот? Что-бы небыло спама и зацикливания, логи логов не делаюстся, так же как и сообщения бота
			pass
		del_msg_embed = discord.Embed(title="Delete message", description= f'**Пользователь:**\n<@{message.author.id}>  `ID: {message.author.id}`\n\n**Канал:**\n<#{message.channel.id}>\n\n**Сообщение:**\n`{message.content}`', colour= colors[1]) #  Создание рамки
		del_msg_embed.set_footer(text=message.created_at.strftime('%Y.%m.%d-%H:%M:%S')) # Присоединение таблички с временем создания сообщения
		await channel.send(embed= del_msg_embed) # отправка таблички
		
@Bot.event
async def on_message_edit(msg_before, msg_after): # Лог изменения сообщений
	channel = Bot.get_channel(logfile) # Поиск канала с id который вы указали выше
	if msg_before.guild is None: # Проверяет, отправленно сообщение с сервера, или в ЛС боту
		pass
	else:
		ed_msg_embed=discord.Embed(title="Edit message", description= f'**Пользователь:**\n<@{msg_before.author.id}>  `ID: {msg_before.author.id}`\n\n**Канал:**\n<#{msg_before.channel.id}>\n\n**Сообщение до:**\n`{msg_before.content}`\n\n**Сообщение после:**\n`{msg_after.content}`', colour= colors[1]) # Создание рамки
		ed_msg_embed.set_footer(text= '{} | {}'.format(msg_before.created_at.strftime('%Y.%m.%d-%H:%M:%S'), msg_after.edited_at.strftime('%Y.%m.%d-%H:%M:%S'))) # Присоединение таблички с временем создания и изменения сообщения
		await channel.send(embed= ed_msg_embed) # отправка таблички


@Bot.command()
async def go_to_work(ctx, time = 12):
	await ctx.message.delete()
	with open('bank.json', 'r') as f:
		accounts = json.load(f)
	status = accounts[str(ctx.author.id)]['is_work']
	if status == 0:
		await ctx.send(f"{ctx.author} пошел(шла) на работу!")
		await ctx.author.send(f"```Вы пошли на работу на {time} игровых часов!```")
		accounts[str(ctx.author.id)]['is_work'] = 1
		with open('bank.json', 'w') as f:
			json.dump(accounts, f)
		t = (int(time) * 60)
		await asyncio.sleep(t)
		await payday(users, ctx.author, time)
		accounts[str(ctx.author.id)]['is_work'] = 0 
		with open('bank.json', 'w') as f:
			json.dump(users, f)   
	elif status == 1:
		await ctx.send("Вы и так на работе!")

async def payday(users, user, hours):
	payday_on_hour = accounts[str(user.id)]['payday']
	payday = payday_on_hour * hours
	accounts[str(user.id)]['money'] += payday

	with open('bank.json', 'w') as f:
		json.dump(users, f) 


@Bot.command()
async def create_card(ctx, password):
	await ctx.message.delete()
	with open('bank.json', 'r') as f:
		accounts = json.load(f)

	await create_account(accounts, ctx.author, password)

	with open('bank.json', 'w') as f:
		json.dump(accounts, f)

async def create_account(accounts, user, password):
	if not str(user.id) in accounts:
		accounts[str(user.id)] = {}
		accounts[str(user.id)]['password'] = str(password)
		accounts[str(user.id)]['money'] = 30
		accounts[str(user.id)]['payday'] = 5
		accounts[str(user.id)]['position'] = "Безработный"
		accounts[str(user.id)]['is_work'] = 0

@Bot.event
async def on_ready():
    print("бульк")

@Bot.event
async def on_voice_state_update(member, before, after):
	guild = member.guild
	cat = Bot.get_channel(579442043122614272)
	# cat = discord.utils.get(member.guild.voice_channels, name= ':wedding:Создать домик:wedding:')
	try:
		if after.channel.id == 579442043122614272:
			namechannel = '🎩 ' + member.name
			await guild.create_voice_channel(name= namechannel, category= cat.category)
			channel = discord.utils.get(member.guild.voice_channels, name= namechannel)
			channel_id = channel.id
			overwrite = discord.PermissionOverwrite()
			overwrite.manage_channels = True
			await channel.set_permissions(member, overwrite=overwrite)
			await asyncio.sleep(0.1)
			await member.edit(voice_channel= channel)
			status = True
			global channellis
			channellis.append(channel_id)

			while status:
				await asyncio.sleep(0.1)
				channel = Bot.get_channel(channel_id)
				namelist = list(channel.name)
				if namelist[0] != '🎩':
					namechannel = '🎩 ' + channel.name
					await channel.edit(name= namechannel)
				if len(channel.members) == 0:
					channellis.remove(channel_id)
					await channel.delete()
					status = False
	except AttributeError:
		pass


@Bot.command()
async def report(ctx, member: discord.Member, *, reason): # Отправка репорта на игрока, который по вашему мнению нарушил правило
    channel = Bot.get_channel(report_file) # Поиск канала с id который вы указали выше
    author = ctx.author # Это сделанно для моего удобства xD
    if ctx.message.guild is None: # Проверяет, отправленно сообщение с сервера, или в ЛС боту
        pass
    else:
        await ctx.message.delete() # Удаление сообщения с командой

        try:
            log_report_embed = discord.Embed(title= "⚠ Report",  description= f"**Пользователь:**\n<@{member.id}>  `ID: {member.id}`\n\n**Причина:**\n`{reason}`\n\n**Канал:**\n<#{ctx.message.channel.id}>", colour= colors[2]) # Создание таблички
            log_report_embed.set_author(name= f'{ctx.message.author}  ({ctx.message.author.id})', icon_url=ctx.message.author.avatar_url) # Доюавление строки с автором
            log_report_embed.set_footer(text=ctx.message.created_at.strftime('%Y-%m-%d %H:%M:%S')) # добавление строки с временем отправки сообщения
            await channel.send(embed= log_report_embed) # Отправка сообщения в канал с жалобами

            report_embed=discord.Embed(description= f'Ваша жалоба на <@{member.id}> принята.', colour=colors[2]) # Создание таблички
            report_embed.set_footer(text='Большая просьба воздержаться от спама, 1 жалобы на пользователя вполне достаточно.') # Добавление строки
            await author.send(embed= report_embed) # отправка сообщения в ЛС игроку, написавшему жалобу
        except:
            try:
                await author.send(embed= discord.Embed(description='⚠ Произошла ошибка. обратитесь к главному создателю!', colour= colors[2])) # отправка сообщения в ЛС игроку, написавшему жалобу, но при случившейся ошибке
            except:
                pass

@Bot.command()
@commands.has_permissions(administrator= True)
async def clear(ctx, amount: int):			# Очистка на определенное количество сообщений
    await ctx.channel.purge(limit=amount)

@Bot.command()
@commands.has_permissions(administrator= True)
async def mute(ctx, member: discord.Member = None, tm = "infinite", *, reason = "Не указанна"): # Мут игрока на определенное время, Пример - #mute @HaCsO#9577 10(в минутах) Оскорбления
	if not member: # Проверка, указан игрок которому будет выдан мут, или нет
		await ctx.message.delete() # Удаления сообщения с командой
		ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал

	else: # Выводится при наличии игрока
		await ctx.message.delete() # Удаления сообщения с командой
		if tm == "infinite": # Проверка, если срок навечно, то выполняется этот блок
			membern = member.nick # Взятие ника игрока в переменную
			if member.nick == None: # Проверка наличия самого ника
				membern = member.name # изменение ника на имя аккаунта
			mute_cnt = f"Пользователь {membern} быз замучен на неопределенный срок админом {ctx.author}\nПричина:\n**{reason}!**" # Переменная с текстом
			mute = discord.Embed(title= "Mute", description= mute_cnt, colour= colors[2]) # Создание таблицы
			role = discord.utils.get(ctx.message.guild.roles, name= muterole_name) # Поиск вышеуказанной роли для мута
			await member.add_roles(role) # Выдача этой роли указанному игроку
			await ctx.send(embed= mute) # Сообщение в чат о успешном муте
		else:
			membern = member.nick # Взятие ника игрока в переменную
			if member.nick == None: # Проверка наличия самого ника
				membern = member.name # изменение ника на имя аккаунта
			mute_cnt = f"Пользователь {membern} быз замучен на {tm} минут админом {ctx.author}\nПричина:\n**{reason}!**" # Переменная с текстом
			unmute_cnt = f"Пользователь {membern} быз раззамучен!" # Переменная с текстом
			role = discord.utils.get(ctx.message.guild.roles, name= muterole_name) # Поиск вышеуказанной роли для мута
			mute = discord.Embed(title= "Mute", description= mute_cnt, colour= colors[2]) # Создание таблицы
			unmute = discord.Embed(title= "UnMute", description= unmute_cnt, colour= colors[2]) # Создание таблицы
			t = (int(tm) * 60) # Изменение формата с секунд на минуты
			await member.add_roles(role) # Добавление роли замученного указанному игроку
			await ctx.send(embed= mute) # Отправка сообщения об этом
			await asyncio.sleep(t) # Задержка до разбана
			await member.remove_roles(role) # Снятие роли замученного
			await ctx.send(embed= unmute) # Отправка сообщения об этом

@Bot.command()
@commands.has_permissions(administrator= True)
async def unmute(ctx, member : discord.Member = None): # размут игрока, пример - #unmute @HaCsO#9577
	await ctx.message.delete() # Удаления сообщения с командой
	if not member: # Проверка, указан игрок которому будет выдан размут, или нет
		ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
	else: # Выводится при наличии игрока
		membern = member.nick # Взятие ника игрока в переменную
		if member.nick == None: # Проверка наличия самого ника
			membern = member.name # изменение ника на имя аккаунта
		unmute_cnt = f"Пользователь {membern} быз раззамучен админом {ctx.author}!" # Переменная с текстом
		unmute = discord.Embed(title= "UnMute", description= unmute_cnt, colour= colors[2]) # Создание таблицы
		role = discord.utils.get(ctx.message.guild.roles, name= muterole_name) # Поиск вышеуказанной роли для мута
		await member.remove_roles(role) # Снятие роли замученного
		await ctx.send(embed= unmute) # Отправка сообщения об этом


@Bot.command()
@commands.has_permissions(administrator= True)
async def warn(ctx, member : discord.Member = None, *, reason = None): # Выдача предупреждения, Пример - #warn @HaCsO#9577 Шутка про майнкрафт
	await ctx.message.delete() # Удаления сообщения с командой
	if not member: # Проверка, указан игрок которому будет выдан варн, или нет
		ctx.send("Укажите пользователя!") # Отправка сообщения в тот же канал
	else: # Выводится при наличии игрока
		if reason == None: # Проверка наличия причины
			reason = "Неуказанно" # Замена пустой причины на то, чт оуказанно в переменной
		warn_cnt = f"Администратор {ctx.author} выдал предупреждение пользователю {member}\nПричина:\n**{reason}!**" # Переменная с текстом
		warn = discord.Embed(title= "Warned", description= warn_cnt, color= colors[2]) # Создание таблицы
		await member.add_roles(warned_role)
		await ctx.send(embed= warn) # Отправка сообщения об этом

@Bot.command()
async def version(ctx): # Версия, можно редачить
	await ctx.message.delete() # Удаления сообщения с командой
	await ctx.send("`V.1`") # Отправка сообщения в тот же канал


@Bot.command()
async def num(ctx):
	await ctx.message.delete()
	global status
	status = True


	while status:
		await asyncio.sleep(1)
		channel = Bot.get_channel(channellis[0])
		channel1 = Bot.get_channel(channellis[1])
		channel2 = Bot.get_channel(channellis[2])
		channel3 = Bot.get_channel(channellis[3])
		channel4 = Bot.get_channel(channellis[4])
		channel5 = Bot.get_channel(channellis[5])
		channel6 = Bot.get_channel(channellis[6])
		channel7 = Bot.get_channel(channellis[7])
		channel8 = Bot.get_channel(channellis[8])
		channel9 = Bot.get_channel(channellis[9])
		channel10 = Bot.get_channel(channellis[10])
		channel11 = Bot.get_channel(channellis[11])
		channel12 = Bot.get_channel(channellis[12])
		channel13 = Bot.get_channel(channellis[13])
		channel14 = Bot.get_channel(channellis[14])
		channel15 = Bot.get_channel(channellis[15])
		channel16 = Bot.get_channel(channellis[16])
		channel17 = Bot.get_channel(channellis[17])
		channel18 = Bot.get_channel(channellis[18])
		channel19 = Bot.get_channel(channellis[19])
		channel20 = Bot.get_channel(channellis[20])
		channel21 = Bot.get_channel(channellis[21])
		channel22 = Bot.get_channel(channellis[22])
		channel23 = Bot.get_channel(channellis[23])
		channel24 = Bot.get_channel(channellis[24])

		alls = len(channel.members) + len(channel1.members) + len(channel2.members) + len(channel3.members) + len(channel4.members) + len(channel4.members) + len(channel5.members) + len(channel6.members) + len(channel7.members) + len(channel8.members) + len(channel9.members) + len(channel10.members) + len(channel11.members) + len(channel12.members) + len(channel13.members) + len(channel14.members) + len(channel15.members) + len(channel16.members) + len(channel17.members) + len(channel18.members) + len(channel19.members) + len(channel20.members) + len(channel21.members) + len(channel22.members) + len(channel23.members) + len(channel24.members)
		if len(channellis) > 25:
			channel25 = Bot.get_channel(channellis[25])
			alls = alls + len(channel25.members)
		if len(channellis) > 26:
			channel26 = Bot.get_channel(channellis[26])
			alls = alls + len(channel26.members)
		if len(channellis) > 27:
			channel27 = Bot.get_channel(channellis[27])
			alls = alls + len(channel27.members)
		if len(channellis) > 28:
			channel28 = Bot.get_channel(channellis[28])
			alls = alls + len(channel28.members)
		if len(channellis) > 29:
			channel29 = Bot.get_channel(channellis[29])
			alls = alls + len(channel29.members)
		if len(channellis) > 30:
			channel29 = Bot.get_channel(channellis[30])
			alls = alls + len(channel30.members)
		if len(channellis) > 31:
			channel29 = Bot.get_channel(channellis[31])
			alls = alls + len(channel31.members)
		if len(channellis) > 32:
			channel29 = Bot.get_channel(channellis[32])
			alls = alls + len(channel32.members)

		allschannel = Bot.get_channel(allsch)
		await allschannel.edit(name= f"Голосовой онлайн: {alls}")

@Bot.command()
async def stop(ctx):
	await ctx.message.delete()
	global status
	status = False

@Bot.command()
@commands.has_permissions(administrator= True)
async def em(ctx):
    await ctx.message.delete()
    btmsgemhex = discord.Embed(description='**Введите цвет в формате rgb. Пример \'255 255 255\'**', colour= 0x000000)
    btmsgemhex.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

    bt_msg_hex = await ctx.send(embed= btmsgemhex)
    def check(m):
    	return m.author == ctx.author
    em_color = await Bot.wait_for('message', check= check)
    em_color_content = em_color.content    #Титульная
    if em_color_content == '-none':

        await bt_msg_hex.delete()
        await em_color.delete()

        btmsgem = discord.Embed(description='**Введите титульное название.**', colour= 0x000000)
        btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

        bt_msg = await ctx.send(embed= btmsgem)
        def check(m):
            return m.author == ctx.author
        em_title = await Bot.wait_for('message', check= check)
        em_title_content = em_foot.content   #Тиутльник

        if em_title_content == '-none':

            await bt_msg.delete()
            await em_title.delete()

            btmsgem = discord.Embed(description='**Введите футер.**', colour= 0x000000)
            btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

            bt_msg = await ctx.send(embed= btmsgem)
            def check(m):
                return m.author == ctx.author
            em_foot = await Bot.wait_for('message', check= check)
            em_foot_content = em_foot.content   #Футер

            if em_foot_content == '-none':

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour= 0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour= 0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(description=em_desc_content, colour=0x000000)

                        await ctx.send(embed= em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

            if em_foot_content == '-stop':

                await bt_msg.delete()
                await em_foot.delete()

                em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                msg_stoped = await ctx.send(embed= em_stoped)

                await asyncio.sleep (3)

                await msg_stoped.delete()

                pass

            else:

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
       	        def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(description=em_desc_content, colour=0x000000)
                        em.set_footer(text=em_foot_content)

                        await ctx.send(embed= em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

        if em_title_content == '-stop':

            await bt_msg.delete()
            await em_title.delete()

            em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
            em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
            msg_stoped = await ctx.send(embed= em_stoped)

            await asyncio.sleep (3)

            await msg_stoped.delete()

            pass

        else:

            await bt_msg.delete()
            await em_title.delete()

            btmsgem = discord.Embed(description='**Введите футер.**', colour=0x000000)
            btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

            bt_msg = await ctx.send(embed= btmsgem)
            def check(m):
                return m.author == ctx.author

            em_foot = await Bot.wait_for('message', check= check)
            em_foot_content = em_foot.content   #Футер

            if em_foot_content == '-none':

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(title=em_title_content, description=em_desc_content, colour=0x000000)

                        await ctx.send(embed=em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

            if em_foot_content == '-stop':

                await bt_msg.delete()
                await em_foot.delete()

                em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                msg_stoped = await ctx.send(embed= em_stoped)

                await asyncio.sleep (3)

                await msg_stoped.delete()

                pass

            else:

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author

                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed=em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(title=em_title_content, description=em_desc_content, colour=0x000000)
                        em.set_footer(text=em_foot_content)

                        await ctx.send(embed=em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

    elif em_color_content == '-stop':
        await bt_msg_hex.delete()
        await em_color.delete()

        em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
        em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
        msg_stoped = await ctx.send(embed=em_stoped)

        await asyncio.sleep (3)

        await msg_stoped.delete()

        pass

    else:
        await bt_msg_hex.delete()
        await em_color.delete()

        rgb = list(em_color_content)
        R = rgb[0] + rgb[1] + rgb[2]
        G = rgb[4] + rgb[5] + rgb[6]
        B = rgb[8] + rgb[9] + rgb[10]

        btmsgem = discord.Embed(description='**Введите титульное название.**', colour= 0x000000)
        btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

        bt_msg = await ctx.send(embed= btmsgem)
        def check(m):
            return m.author == ctx.author

        em_title = await Bot.wait_for('message', check= check)
        em_title_content = em_title.content   #Тиутльник

        if em_title_content == '-none':

            await bt_msg.delete()
            await em_title.delete()

            btmsgem = discord.Embed(description='**Введите футер.**', colour= 0x000000)
            btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

            bt_msg = await ctx.send(embed= btmsgem)
            def check(m):
                return m.author == ctx.author
            em_foot = await Bot.wait_for('message', check= check)
            em_foot_content = em_foot.content   #Футер

            if em_foot_content == '-none':

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour= 0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour= 0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(description=em_desc_content, colour= discord.Colour.from_rgb(int(R), int(G), int(B)))

                        await ctx.send(embed= em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

            if em_foot_content == '-stop':

                await bt_msg.delete()
                await em_foot.delete()

                em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                msg_stoped = await ctx.send(embed= em_stoped)

                await asyncio.sleep (3)

                await msg_stoped.delete()

                pass

            else:

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
       	        def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(description=em_desc_content, colour= discord.Colour.from_rgb(int(R), int(G), int(B)))
                        em.set_footer(text=em_foot_content)

                        await ctx.send(embed= em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

        if em_title_content == '-stop':

            await bt_msg.delete()
            await em_title.delete()

            em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
            em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
            msg_stoped = await ctx.send(embed= em_stoped)

            await asyncio.sleep (3)

            await msg_stoped.delete()

            pass

        else:

            await bt_msg.delete()
            await em_title.delete()

            btmsgem = discord.Embed(description='**Введите футер.**', colour=0x000000)
            btmsgem.set_footer(text='Введите "-none" что бы пропустить. Введите "-stop" что бы остановить создание ембеда.')

            bt_msg = await ctx.send(embed= btmsgem)
            def check(m):
                return m.author == ctx.author

            em_foot = await Bot.wait_for('message', check= check)
            em_foot_content = em_foot.content   #Футер

            if em_foot_content == '-none':

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author
                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed= em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(title=em_title_content, description=em_desc_content, colour= discord.Colour.from_rgb(int(R), int(G), int(B)))

                        await ctx.send(embed=em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()

            if em_foot_content == '-stop':

                await bt_msg.delete()
                await em_foot.delete()

                em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                msg_stoped = await ctx.send(embed= em_stoped)

                await asyncio.sleep (3)

                await msg_stoped.delete()

                pass

            else:

                await bt_msg.delete()
                await em_foot.delete()

                btmsgem = discord.Embed(description='**Введите описание.**', colour=0x000000)
                btmsgem.set_footer(text='Введите "-stop" что бы остановить создание ембеда.')

                bt_msg = await ctx.send(embed= btmsgem)
                def check(m):
                    return m.author == ctx.author

                em_desc = await Bot.wait_for('message', check= check)
                em_desc_content = em_desc.content   #Описание

                if em_desc_content == '-stop':

                    await bt_msg.delete()
                    await em_desc.delete()

                    em_stoped = discord.Embed(description='**Создание ембеда прекращено.**', colour=0x000000)
                    em_stoped.set_footer(text='Это сообщение автоматически удалится через 3 секунды.')
                    msg_stoped = await ctx.send(embed=em_stoped)

                    await asyncio.sleep (3)

                    await msg_stoped.delete()

                    pass

                else:

                    try:

                        await bt_msg.delete()
                        await em_desc.delete()

                        em = discord.Embed(title=em_title_content, description=em_desc_content, colour= discord.Colour.from_rgb(int(R), int(G), int(B)))
                        em.set_footer(text=em_foot_content)

                        await ctx.send(embed=em)

                    except:

                        errmsg = await ctx.send('**Произошла ошибка!**')

                        await asyncio.sleep(2)

                        await errmsg.delete()



Bot.run(str(token))
