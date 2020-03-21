import discord

from datetime import datetime
from epl import getEplData
from corona import getCoronaInfo
from mask import getMaskData

client = discord.Client()

TOKEN = "NjgzNjQ0Nzk1MDQ1OTM3MTUz.XnM7-Q.knnWqT-5uSuCIGAAWEcK5P0GZxU"

@client.event
async def on_ready() :
    print(client.user.id)
    print('ready')
    game = discord.Game("테스트봇")
    await client.change_presence(status=discord.Status.online, activity=game)



@client.event
async def on_message(message) :

    # 봇 응답메세지의 반복을 멈춤 
    if message.author.bot :
        return None 

    # 인사 메세지 
    if message.content.startswith('안녕') :
        await message.channel.send('안녕하세요!')

    if message.content.startswith('코로나') :
        await message.channel.send(getCoronaInfo())

    if message.content.startswith('EPL') :        
        await message.channel.send(getDate() + ' 기준 EPL 순위 - Sky Sports ') # 오늘 날짜 출력                   
        await message.channel.send(getEplData()) #순차적으로 순위, 팀명, 승점 출력

    if message.content.startswith('오늘날짜') :
        await message.channel.send(getDate())

    if message.content.startswith('마스크') : 
        await message.channel.send(getMaskData())              


def getDate() :

    # 오늘의 연 / 월 / 일 을 구해주는 함수
    
    return datetime.today().strftime("%Y년 %m월 %d일")
 

def runBot() :
    client.run(TOKEN)
    
runBot()


    