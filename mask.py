import urllib.request as ul
import json
import itertools

def getMaskData() :

    URL = "https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/stores/json?page="
    MAX_PAGE = 10

    REGION = "연수구" # 검색 지역

    stores = [] # 필터링된 마스크 판매처 
    

    for page in range(MAX_PAGE) :
        request = ul.Request(f"{URL}{page+1}") # page = 1, page = 2, page = 3 .....
        print(f"URL : {page} : {URL}{page+1}")
        response = ul.urlopen(request)
        jsonData = json.load(response) #페이지별 전체적인 json
        storeJson = jsonData['storeInfos'] #list 형식으로 반환        
        stores.append(filterByRegion(REGION,storeJson))   
    

    return setFinalString(stores)         

   
def filterByRegion(region,storeList) :
    
    #지역에 따라 약국 필터링 ex) 서울특별시, 인천광역시 
    stores = []       

    for store in storeList :
        name = store['name'] # 이름
        address = store['addr'] # 주소
        lat = store['lat'] # 위도
        lng = store['lng'] # 경도
        storeType = store['type'] # 판매처 유형 (약국 : '01', 우체국 : '02', 농협 : '03')
        
        split_address = address.split(" ")
        
        if(region in split_address) :
        # 검색한 주소가 공백별로 나눈 split_address에 존재한다면
        # Dictionary로 데이터를 저장한다    
            stores.append({
                "name" : name,
                "address" : address,
                "lat" : lat,
                "lng" : lng,
                "storeType" : storeType,
                
            }) 

    return stores

def setFinalString(stores) :

    # 봇이 출력할 문자열을 마지막으로 가공

    final_string = "" # 봇이 출력할 최종 문자열

    
    iter_store_list = list(itertools.chain(*stores)) #같은 페이지내의 필터링된 2개 이상의 약국이 있으면 2차원 배열이 만들어지므로 1차원 배열로 만들어준다
    index = 1 #인덱스
    store_type_string = "" #판매처 유형을 담을 문자열

   

    for store in iter_store_list :
        # 판매처 유형별로 분류 (약국 : '01', 우체국 : '02', 농협 : '03')
        if store['storeType'] == '01' :
            store_type_string = '약국'
        elif store['storeType'] == '02' :
            store_type_string = '우체국'
        else :
            store_type_string = '농협'        

        final_string = final_string + f"{index}. {store['name']} 주소 ({store['address']} - 판매처 유형 : {store_type_string}\n"
        index = index + 1

    return final_string






