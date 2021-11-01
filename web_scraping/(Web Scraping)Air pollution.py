import urllib.request, json 


def choose_city(city_chosen):
    if city_chosen == '東京':
        with urllib.request.urlopen('http://api.waqi.info/feed/tokyo/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '北海道':
        with urllib.request.urlopen('https://api.waqi.info/feed/sapporo/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '沖繩':
        with urllib.request.urlopen('http://api.waqi.info/feed/okinawa/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '大阪':
        with urllib.request.urlopen('http://api.waqi.info/feed/osaka/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '京都':
        with urllib.request.urlopen('http://api.waqi.info/feed/kyoto/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '首爾':
        with urllib.request.urlopen('http://api.waqi.info/feed/seoul/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '釜山':
        with urllib.request.urlopen('http://api.waqi.info/feed/busan/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '芭達雅':
        with urllib.request.urlopen('http://api.waqi.info/feed/rayong/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '普吉島':
        with urllib.request.urlopen('http://api.waqi.info/feed/surat thani/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '曼谷':
        with urllib.request.urlopen('http://api.waqi.info/feed/bangkok/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '新加坡':
        with urllib.request.urlopen('http://api.waqi.info/feed/singapore/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data
    if city_chosen == '香港':
        with urllib.request.urlopen('http://api.waqi.info/feed/hongkong/?token=386c3b918f1195bc9d3364cc0d3474007025d230') as url:
            data = json.loads(url.read().decode())
        return data



def print_poll(city,data):

    #print(city)
    print("當下最嚴重污染物為："+data['data']['dominentpol'])
    #print("一氧化碳："+str(data['data']['iaqi']['co']['v'])+" ppm")
    #print("二氧化氮："+str(data['data']['iaqi']['no2']['v'])+" ppm")
    #print("臭氧："+str(data['data']['iaqi']['o3']['v'])+" ppm")
    print("pm10："+str(data['data']['iaqi']['pm10']['v'])+" ppm")
    print("pm25："+str(data['data']['iaqi']['pm25']['v'])+" ppm")

    dominant_pollutant = data['data']['dominentpol']
    air_condition = 0
    air_condition_tag = ''
    if dominant_pollutant == 'pm10':
        air_condition = data['data']['iaqi']['pm10']['v']
    else:
        air_condition = data['data']['iaqi']['pm25']['v']
    
    if air_condition <= 50:
        air_condition_tag = '空氣品質優良，基本無空氣污染'
    elif air_condition <= 100:
        air_condition_tag = '空氣品質良好，污染物少，對少數敏感族群可能有輕微影響'
    elif air_condition <= 150:
        air_condition_tag = '空氣輕度污染，敏感族群感到不適'
    elif air_condition <= 200:
        air_condition_tag = '空氣中度污染，可能影響健康人心臟以及呼吸系統'
    elif air_condition <= 300:
        air_condition_tag = '空氣重度污染，運動耐受力降低。健康人出現症狀'
    else:
        air_condition_tag = '空氣嚴重污染，健康人出現明顯症狀'
    
    print(air_condition_tag)
    #get_city = data['name']    



#main function
city_chosen = str(input())
data = choose_city(city_chosen)
print_poll(city_chosen,data)
