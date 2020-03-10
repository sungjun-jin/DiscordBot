import discord
import openpyxl
import os
import random
from discord.ext import commands
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests


TOKEN = ""

client = discord.Client()
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

    if message.content.startswith('!순위') :
        await message.channel.send('확인할 실시간 인기 검색어 : 10대  20대 30대 40대 50대 전체')
    
    if message.content.startswith('!10대') :
        await message.channel.send(NaverRanking1())
    
    if message.content.startswith('!20대') :
        await message.channel.send(NaverRanking2())

    if message.content.startswith('!30대') :
        await message.channel.send(NaverRanking3())
    
    if message.content.startswith('!40대') :
        await message.channel.send(NaverRanking4())
    
    if message.content.startswith('!50대') :
        await message.channel.send(NaverRanking5())

    if message.content.startswith('!전체') :
        await message.channel.send(NaverRanking6())

def NaverRanking1():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=10s&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(3)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')
    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave




def NaverRanking2():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=20s&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(60)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')
    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave


def NaverRanking3():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=30s&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(60)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')
    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave


def NaverRanking4():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=40s&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(60)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')
    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave

def NaverRanking5():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=50s&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(60)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')
    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave

def NaverRanking6():
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age=all&where=main'
            
    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver')
    driver.implicitly_wait(60)

    driver.get(raking_page)

    html = driver.page_source
    na_ranking = BeautifulSoup(html, 'html.parser')

    realtimerank = na_ranking.select('span.item_title')

    memsave = list()
    i = 0
    for sonwi in realtimerank:
        print('{}위 : {}'.format(str(i+1),sonwi.text.strip()))
        memsave[i:] = ['{}위 : {}'.format(str(i+1),sonwi.text.strip())]
        i = i + 1

    driver.quit()

    return memsave


client.run(TOKEN)
