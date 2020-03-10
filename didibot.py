import discord
import openpyxl
import os
import random # 랜덤 이미지 출력을 위한 랜덤 라이브러리 호출
import youtube_dl
import shutil
import asyncio
from discord.ext import commands
from discord.utils import get
from os import system
from selenium import webdriver # selenium을 사용하기위한 라이브러리
from bs4 import BeautifulSoup # BeautifulSoup 라이브러리
from urllib.request import urlopen # 
import requests



TOKEN = ""

client = discord.Client()
bot = commands.Bot(command_prefix = '!')


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


# 네이버 인기검색어 기능
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


# youtube 재생기능

@bot.command(pass_context=True, aliases=['j', '들락'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f":woman_juggling: {bot.user.name}이 놀러왔습니다.")


@bot.command(pass_context=True, aliases=['l', '날락'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f":homes: {bot.user.name}이 집에 돌아갔습니다.")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


@bot.command(pass_context=True, aliases=['p', '재생'])
async def play(ctx, url: str):
    
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
    

    if url[0:5] == 'https' or url[0:6] == 'youtube':
            print(url)
    else:   
        keywordinput = 'https://www.youtube.com/results?search_query=' + url
        req = requests.get(keywordinput)

        soup = BeautifulSoup(req.text, 'lxml')
        title = soup.select("h3.yt-lockup-title > a")
        playtime = soup.select("h3.yt-lockup-title > span")


    fix_title = []
    fix_playtime = []
    fix_youtubeurl = []

    for i in range(5):
        str_tmp = str(title[i].text)
        fix_title.append(str_tmp)

    for i in range(5):
        str_tmp = str(playtime[i].text)
        str_tmp = str_tmp.replace(' - ', '')
        fix_playtime.append(str_tmp)
        
    for i in range(5):
        str_tmp = str(title[i].get('href', '/'))
        str_tmp = str(f"https://www.youtube.com{str_tmp}")
        fix_youtubeurl.append(str_tmp)
        
    embed = discord.Embed(
        colour= discord.Colour.blue(),
        title = "유튜브 검색",
        description = f"{url}로 검색한 결과입니다."
    )
    
    serchlist = []
    for i in range(5):
        serchlist.append(f"{fix_title[i]} : {fix_playtime[i]}")
        #embed.add_field(name="", value=f"{serchlist[i]}", inline=False)
        print(serchlist[i])

    await ctx.send('곡을 선택해 주세요')
    
    choicenum = None

    def check(m):
        return m.content == '1' or m.content == '2' or m.content == '3' or m.content == '4' or m.content == '5' and m.channel == channel
            
    try:
        msg = await client.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        print(msg)
        await ctx.send('취소되었습니다.')
    else:
        choicenum = msg
        await ctx.send(f'{choicenum}이 선택되었습니다.')


    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                voice.disconnect()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                        

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1.0

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    await ctx.send("노래 준비중")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)") # 유튜브 url이 아닐경우 spotify url 여부 파악하여 다운
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0
    
    namelen = len(name)
    await ctx.send(f"Playing: **{name[:namelen-16]}**")
    print("playing\n")


@bot.command(pass_context=True, aliases=['pa', '일시정지'])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause")


@bot.command(pass_context=True, aliases=['r', '다시재생'])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")


@bot.command(pass_context=True, aliases=['s', '정지'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped"), 
        await voice.disconnect()
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")


queues = {}

@bot.command(pass_context=True, aliases=['a', '추가'])
async def addqueue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1

    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1 
        else:
            add_queue = False
            queues[q_num] = q_num
    
    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\%(title)s.%(ext)s")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("FALLBACK: youtube-dl does not support this URL, using Spotify (This is normal if Spotify URL)")
        q_path = os.path.abspath(os.path.realpath("Queue"))
        system(f"spotdl -ff song{q_num} -f " + '"' + q_path + '"' + " -s " + url)
    
    mp3list = os.listdir("./Queue")
    name = mp3list[-1]
    qq = len(mp3list)
    print(mp3list)
    print(f"Renamed File: {name}\n")
    os.rename(f"./Queue/{name}", f"./Queue/'{q_num} {name}")

    namelen=len(name)

    await ctx.send(f"**{name[:namelen-4]}** 대기열에 추가 됨")      
    await ctx.send("현재 **" + str(qq) + "** 곡 큐 대기중")

    print("Song added to queue\n")


@bot.command(pass_context=True, aliases=['n', '다음곡'])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        nextsong1 = os.listdir("./Queue")
        nextsong2 = nextsong1[0]
        namelen = len(nextsong2)
        await ctx.send(f"다음곡 : **{nextsong2[3:namelen-4]}**")
        voice.stop()
    else:
        print("No music playing")
        await ctx.send("No music playing failed")


@bot.command(pass_context=True, aliases=['v', '볼륨'])
async def volume(ctx, vol : int):
    voice = get(bot.voice_clients, guild=ctx.guild)

    embed = discord.Embed(
        colour=discord.Colour.blue()
    )

    voice.source.volume = 1.0

    vole = float(vol/100)

    if vol >= 0 and vol <= 100:
        voice.source.volume = vole
        embed.add_field(name="현재 볼륨", value="{}".format(int(vole*100)))
        await ctx.send(embed=embed)
    else:
        embed.add_field(name="주의", value="0~100사이에서만 조절해 주세요")
        await ctx.send(embed=embed)

@bot.command(pass_context=True, aliases=['q', '큐'])
async def listqueue(ctx):

    mp3list = os.listdir("./Queue")
    print(len(mp3list))

    embed = discord.Embed(
        colour= discord.Colour.blue(),
        title = "대기열 목록",
        description = f"총 {len(mp3list)}곡 대기중"
    )

    for mp3l in range(len(mp3list)):
        qlist = mp3list[mp3l]
        qlen = len(qlist)
        embed.add_field(name="11",value=f"{mp3l+1}. {qlist[4:qlen-4]}", inline=False)
        await ctx.send(embed=embed)


client.run(TOKEN)

