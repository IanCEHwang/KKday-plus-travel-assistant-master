import csv

def temperature(city_input, date1_input, date2_input):
	#使用這輸入城市名稱和日期，日期格式為8位數字
	city_CN = city_input
	date1 = date1_input
	date2 = date2_input

	trans_dict = {'曼谷':'Bangkok', '釜山':'Busan', '香港':'Hong Kong', '京都':'Kyoto', '沖繩':'Okinawa', '大阪':'Osaka',
				'芭達雅':'Phatthaya', '北海道':'Hokkaido', '普吉島':'Sapporo', '首爾':'Seoul', '新加坡':'Singapore', 
				'東京':'Tokyo'}
	
	city = trans_dict[city_CN]
	city_path = city + '.csv'

	#開啟溫度檔案
	file =  './氣溫csv/' + city_path  # need to change between computers

	#每個月分的天數
	month = [31,28,31,30,31,30,31,31,30,31,30,31]

	#把日期換成每年第幾天
	day1 = 0
	day2 = 0
		
	for i in range(10 * int(date1[5]) + int(date1[6])-1) :
		day1 += month[i]

	day1 += 10 * int(date1[8]) + int(date1[9])


	for i in range(10 * int(date2[5]) + int(date2[6])-1) :
		day2 += month[i]

	day2 += 10 * int(date2[8]) + int(date2[9])
	
	
	#找到那天的氣溫資料	
	n = 0
	
	最低氣溫 = 100000
	最高氣溫 = -100000	
	with open(file, newline='', encoding='cp950') as csvFile:
		#直接讀取：讀取 CSV 檔案內容
		rows = csv.reader(csvFile)
		# 迴圈輸出 每一列
		for row in rows:
			n += 1 
			if day1 + 1 <= n <= day2 + 1:
				if int(row[1][:-1]) >= 最高氣溫 :
					最高氣溫 = int(row[1][:-1])
				if int(row[2][:-1]) <= 最低氣溫 :
					最低氣溫 = int(row[2][:-1])
			
	# print("最高氣溫：" + str(最高氣溫) + "℃" )
	# print("最低氣溫：" + str(最低氣溫) + "℃" )
	highest_out = str(最高氣溫) + '℃'
	lowest_out = str(最低氣溫) + '℃'
	return highest_out, lowest_out

# sample input
# temperature('香港', '20190919', '20190923')  