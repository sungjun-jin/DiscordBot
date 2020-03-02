import discord
import openpyxl
import os
import random
from discord.ext import commands

TOKEN = 


client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print(client.user.id)
    print("ready")
    game = discord.Game("테스트 봇")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')


@client.event
async def on_message(message):    
    if message.content.startswith("!짤"):
        path = "./짤"
        file_list = os.listdir(path)
        pic = random.choice(file_list)
        await message.channel.send(file=discord.File("./짤/"+pic))
    
    if message.content.startswith("!채널메시지"):
        channel = message.content[7:25]
        msg = message.content[26:]
        await client.get_channel(int(channel)).send(msg)

    if message.content.startswith("!DM"):
        author = message.guild.get_member(int(message.content[4:22]))
        msg = message.content[23:]
        await author.send(msg)
    
    if message.content.startswith("!뮤트"):
        author = message.guild.get_member(int(message.content[4:22]))
        role = discord.utils.get(message.guild.roles, name="뮤트")
        await author.add_roles(role)
    
    if message.content.startswith("!언뮤트"):
        author = message.guild.get_member(int(message.content[5:23]))
        role = discord.utils.get(message.guild.roles, name="뮤트")
        await author.remove_roles(role)
    
    if message.content.startswith("!경고"):
        author = message.guild.get_member(int(message.content[4:22]))
        file = openpyxl.load_workbook("경고.xlsx")
        sheet = file.active
        i = 1
        while True:
            if sheet["A" + str(i)].value == str(author.id):
                sheet["B" + str(i)].value = int(sheet["B" + str(i)].value) + 1
                file.save("경고.xlsx")
                if sheet["B" + str(i)].value == 2:
                    await message.guild.ban(author)
                    await message.channel.send("경고 2회 누적입니다. 서버에서 추방됩니다.")
                else:
                    await message.channel.send("{0} : 경고를 1회 받았습니다.".format(author))
                break
            if sheet["A" + str(i)].value == None:
                sheet["A" + str(i)].value = str(author.id)
                sheet["B" + str(i)].value = 1
                file.save("경고.xlsx")
                await message.channel.send("{0} : 경고를 1회 받았습니다.".format(author))
                break
            i += 1



client.run(TOKEN)
