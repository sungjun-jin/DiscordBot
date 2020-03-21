# DiscordBot

## WeStudy 3~4 주차 Python Discord Bot 만들기

### 1. 코로나19

![](https://images.velog.io/images/sungjun-jin/post/e39fcfa5-4685-49e0-b9a5-1a46217799e3/image.png)

코로나 확진환자, 격리해제, 격리중, 사망 수를 출력. 

#### 2020-03-21(수정)

![](https://images.velog.io/images/sungjun-jin/post/61569c7c-6c03-440e-a963-aac46fc58bbc/image.png)

이전에 크롤링한 데이터는 질병관리본부 페이지에 있는 table의 문자열을 통째로 가져오는 방식을 사용해 불필요한 공백이 많았다. 

테이블의 각 요소(확진환자, 격리해제, 격리중, 사망 수)를 따로따로 가져와서 하나의 dictionary로 정리했다. 이 과정에서 문자열의 공백을 제거해 조금 더 깔끔하게 출력했다. 

질병관리본부의 코로나 홈페이지(http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=&brdGubun=&ncvContSeq=&contSeq=&board_id=&gubun=)를 활용했다.

### 2. 프리미어리그 순위, 승점

![](https://images.velog.io/images/sungjun-jin/post/3e019d13-0d96-44d8-a815-e5201370089c/image.png)

19/20 프리미어리그 순위, 승점 출력

Sky Sports (https://www.skysports.com/premier-league-table)를 활용

### 3. 검색한 지역별 마스크 판매처 출력

![](https://images.velog.io/images/sungjun-jin/post/880f2999-7da9-4502-8473-a05476f18a2b/image.png)

내가 살고 있는 연수구 지역의 마스크 판매처의 이름, 주소, 판매처 유형 (약국, 우체국, 농협)을 출력해준다. 

![](https://images.velog.io/images/sungjun-jin/post/ff8d1b70-a567-4d0d-a5e4-c1eec3353bf2/image.png)

원래는 디스코드 메세지로 지역을 검색하는 기능을 넣고 싶었지만 오류를 해결하지 못해 코드에 검색하고자 하는 지역명을 넣어주는 방식으로 처리했다. 
