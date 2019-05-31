#! python 3.6
import discord
import os
import time
import asyncio

token = os.getenv('discordRickBotToken')
idFromEnvi = os.getenv('discordServerID')
client = discord.Client()
messages = joined = 0
dic = {"Mor#1024":2, "Ric#2048":1}	# keep a track of each users message count



async def update_status():
	await client.wait_until_ready()
	global messages, joined	

	while not client.is_closed():
		try:
			with open("stats.txt","a") as f:
				f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")
			messages = 0
			joined = 0

			await asyncio.sleep(600)	# seconds
		except Exception as e:
			print(e)



@client.event
async def on_member_join(member):
	await client.wait_until_ready()
	global messages, joined
	joined  += 1
	for channel in member.server.channels:
		if(str(channel) == "general"):
			await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_member_update(before, after):	#changing nick name back
	n = after.nick							# change the permission of the bot to administrator to work
	if n:
		if n.lower().count("morty") > 0:
			last = before.nick
			if last:
				await after.edit(nick=last)
			else:
				await after.edit(nick="RICK IS ANGRY AT U")



@client.event
async def on_message(message):
	global messages
	messages += 1

	id = client.get_guild(idFromEnvi)
	channels = ["general", "memes", "bot_command"]
	valid_users = []
	# add to below if statement -> and str(message.author) in valid_users
	# for restrictiong only some users to use the bot

	bad_words = ["pucky", "punk", "drug"]	# filter bad words

	for word in bad_words:
		if message.content.count(word) > 0:
			print("A bad word was said")
			#await message.channel.purge(limit=1)	# remove the message
			await message.channel.send("Woow Calm down!, Take it easy buddy.")

	if(str(message.channel) in channels):
		if(message.content.find("!rick") != -1):
			if(message.content.find("hello") != -1):
				await message.channel.send("Hi")
			elif(message.content.find("-users_cnt") != -1):
				await message.channel.send(f"""Number of Members {id.member_count}""")
			elif(message.content.find("help") != -1):
				embed = discord.Embed(title="Help For RickBot", description="Some useful commands")
				embed.add_field(name="!rick", value="Default command")
				embed.add_field(name="!rick -users_cnt", value="Display the users stat in server")
				embed.add_field(name="!rick hello", value="replys Hi")
				await message.channel.send(content=None, embed=embed)
			else:
				await message.channel.send("humm...")
	# else:
	# 	print(f"""User:{message.author} tried to do command {message.content}, in  channel {message.channel}""")


client.loop.create_task(update_status())
client.run(token)




