import discord, asyncio, time
from discord.ext import commands
from discord.ext.commands import Bot
import os

token = "NTc5OTc2OTQwOTk2Mzk1MDI4.XOLpAw.CF4IiUWesUqHIAgvYVAqG7ggkE8" # Нада указать токен

channellis = [579456506794213397, 579445102284374026,579408546781724675, 579444096075169792, 579444141386104833, 579444203919245322, 579430751682953231, 579430894352203786, 579412799017582602, 579413084901212170, 579412873953148969, 579413003049631767, 579412943209234613, 579436825337397268, 579747836233646091, 579748173917192226, 579742381490962462, 579762985900310550, 579432556248694812, 579432593745772545, 579432636053717022, 579414211789193226, 579414372682825730, 579449892057907215, 579413594161152019] # Каналы которых надо подсчитать
allsch = 580088129231388703 # Канал в котором будет счет людей

prefix = 'n/' # Знак который будет перед коммандой, можно изменить
Bot = commands.Bot(command_prefix= prefix) # Выставление префикса коммандам
Bot.remove_command("help") # Удаление стоковой команды help

@Bot.event
async def on_ready():
    print("бульк")

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
		allschannel = Bot.get_channel(allsch)
		await allschannel.edit(name= f"Голосовой онлайн: {alls}")

@Bot.command()
async def stop(ctx):
	await ctx.message.delete()
	global status
	status = False

Bot.run(str(token))