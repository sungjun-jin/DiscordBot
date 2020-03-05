import discord
import requests 
from bs4 import BeautifulSoup
from datetime import datetime

client = discord.Client()

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
        await message.channel.send(coronaInfo())

    if message.content.startswith('EPL') :
        
        await message.channel.send(getDate() + ' 기준 EPL 순위 - Sky Sports ')        
        epl_data = getEplData()
        for data in epl_data :
            await message.channel.send(data) #순차적으로 순위, 팀명, 승점 출력

    if message.content.startswith('오늘날짜') :
        await message.channel.send(getDate())        
           



# 코로나 정보 출력 함수
def coronaInfo() :

    # 1. 코로나 확진 환자
    # 2. 코로나 검사 진행
    # 3. 격리해제
    # 4. 사망자 

    # 크롤링 할 URL
    url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=&brdGubun=&ncvContSeq=&contSeq=&board_id=&gubun="

    response = requests.get(url)

    # 파이썬 내장 html.parser 사용
    domain = BeautifulSoup(response.content, 'html.parser')

    # 데이터 업데이트 시간
    corona_update_time = domain.select_one('p.s_descript').text.strip()

    # 확진환자, 검사진행 환자, 격리해제 환자, 사망자 수 
    corona_text = domain.select_one('.num').text.strip()

    print(corona_text);

    return corona_update_time +'\n'+ corona_text

def getEplData() :

    # Sky Sports 크롤링 후 EPL 팀의 순위를 가져오는 함수


    # 1. 순위
    # 2. 팀
    # 3. 승점        

    datas = [] #데이터
    teams = [] # 팀명 
    ranks = [] # 순위
    points = [] # 승점


    index = 0 # 데이터 추출을 위한 list 접근용 인덱스


    # 크롤링 할 URL
    url = "https://www.skysports.com/premier-league-table"

    response = requests.get(url)
    # 파이썬 내장 html.parser 사용
    domain = BeautifulSoup(response.content, 'html.parser')    
    rankTable = domain.find_all("a",{"class" : "standing-table__cell--name-link"})

    rankPoint = domain.find_all("td",{"class" : "standing-table__cell"})

    for team in rankTable :

       teams.append(team.string)
    

    # 팀명을 제외한 순위, 점수, 가지고 오기 
    for text in rankPoint :
        datas.append(text.string)
              
    

    # 데이터에서 순위 가지고 오기   
    for rank in datas :      

        if index % 11 == 0 :
            ranks.append(str(rank))            
            index = index + 1
        else :
            index = index + 1  

    index = 0    

    # 데이터에서 승점 가지고 오기

    for point in datas : 

        if index  == 9 :
            points.append(str(point))
            index = index + 1           
        elif index == 10 :
            index = 0    
        else :
            index = index + 1
    
    chat_string = getEPLDataString(teams,ranks,points)
    return chat_string


def getEPLDataString(teams,ranks,points) :

    
    # 가져온 데이터들을 모두 하나의 문자열로 합치는 함수

    index = 0 # 배열에 접근하고자 하는 index

 
    
    final_string = [] # 봇이 출력할 최종 문자열 리스트4

    for rank in ranks :

        final_string.append(rank + ". ")       

    for team in teams :

        final_string[index] = final_string[index] + team + " -  승점 : "
        index = index + 1
    
    index = 0 # index 재초기화

    for point in points :

        final_string[index] = final_string[index] + point
        index = index + 1

    return final_string


def getDate() :

    # 오늘의 연 / 월 / 일 을 구해주는 함수
    
    return datetime.today().strftime("%Y년 %m월 %d일")
 


client.run("NjgzNjQ0Nzk1MDQ1OTM3MTUz.Xlzitg.U6IX-8_2I-IglAzwsYDM791NZVw")

