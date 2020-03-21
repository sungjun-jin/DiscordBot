import requests 
from bs4 import BeautifulSoup


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
    final_string_list = setFinalString(chat_string)
    return final_string_list



def setFinalString(final_string) :

    # 봇이 출력할 문자열을 마지막으로 가공

    final_string_list = ""

    for string in final_string :
        final_string_list = final_string_list + string + "\n"

    return final_string_list

