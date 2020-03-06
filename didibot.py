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
    if message.content.startswith("!명령어"):
        await message.channel.send("짤, 순위")

    if message.content.startswith("!짤"):
        path = "./randompic"
        file_list = os.listdir(path)
        pic = random.choice(file_list)
        print(pic)
        await message.channel.send(file=discord.File("./randompic/"+pic))
    
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

        rank_age = message.content[4:]
        
        if rank_age == '10대':
            chart = NaverRanking('10s')
        elif rank_age == '20대':
            chart = NaverRanking('20s')
        elif rank_age == '30대':
            chart = NaverRanking('30s')
        elif rank_age == '40대':
            chart = NaverRanking('40s')
        elif rank_age == '50대':
            chart = NaverRanking('50s')
        elif rank_age == '전체':
            chart = NaverRanking('all')
        else:
            await message.channel.send('확인할 실시간 인기 검색어 : 10대  20대 30대 40대 50대 전체')

        for naverranking in chart :
            await message.channel.send(naverranking) 

def NaverRanking(age):
    raking_page = 'https://datalab.naver.com/keyword/realtimeList.naver?age='+ age +'&where=main' # 크롤링할 페이지 주소

    driver = webdriver.Chrome('c:/Users/Taigagoon/Desktop/save/chromedriver') # selenium 사용을 위한 브라우저 드라이버 저장위치
    driver.implicitly_wait(3) # 브라우저 드라이버 실행대기 시간 3초간 대기

    driver.get(raking_page) # 브라우저 드라이버를 raking_page의 주소로 들어가게함 

    html = driver.page_source # 해당 웹페이지 소스를 html 변수에 저장
    na_ranking = BeautifulSoup(html, 'html.parser') # BeautifulSoup를 활용하여 html에 저장되어있던 소스 파싱하여 na_ranking에 저장
    realtime_rank = na_ranking.select('span.item_title') # na_ranking에 파싱되어 있던 내용 중 span.item_title 태그 선택자 찾아서 찾아냄

    i = 0 # 리스트 접근 위한 변수

    saverank = [] # 순위 저장

    for sonwi in realtime_rank:
        saverank.append('{}위 : {}'.format(str(i+1),sonwi.text.strip())) # .append를 사용하여 리스트뒤에 순위 저장
        i = i + 1 #0~20까지 증가

    driver.quit() #브라우저 드라이버 종료

    return saverank # saverank리스트 반환

client.run(TOKEN)
