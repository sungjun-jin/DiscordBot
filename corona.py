import requests 
from bs4 import BeautifulSoup

# 코로나 정보 출력 함수
def getCoronaInfo() :

    # 1. 코로나 확진 환자
    # 2. 코로나 검사 진행
    # 3. 격리해제
    # 4. 사망자 

    # 크롤링 할 URL
    url = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=&brdGubun=&ncvContSeq=&contSeq=&board_id=&gubun="

    response = requests.get(url)

    # 파이썬 내장 html.parser 사용
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find("p",{"class" : "s_descript"}).string # 제목 ex) 코로나바이러스감염증-19 국내 발생현황 (3.19. 00시 기준)


    data_list = []
    
    table_soup = soup.find("table",{"class" : "num"})
    t_head = table_soup.find_all("th") # find_all은 list로 반환된다.

    confirmed = t_head[0].string # 확진환자
    discharged = t_head[1].string # 격리해제
    quarantine =  t_head[2].string # 격리중
    death = t_head[3].string # 사망

    # t_body soup : [<td>8,565</td>, <td>1,947</td>, <td>6,527</td>, <td>91</td>] (td는 확진환자, 격리해제, 격리중, 사망 순)
    t_body = table_soup.find_all("td")


    data_list.append({

        confirmed : t_body[0].string,
        discharged : t_body[1].string,
        quarantine : t_body[2].string,
        death : t_body[3].string,
    })

    final_string = setFinalString(title, data_list)
    return final_string

        
def setFinalString(title,data_list) :

    # 봇이 출력할 문자열을 마지막으로 가공

    final_string =  title + '\n'

    for data in data_list :
        final_string = final_string + str(data)

    # 문자열 가공 '{}' 제거
    final_string = final_string.strip("{") 
    final_string = final_string.strip("}")

    return final_string

