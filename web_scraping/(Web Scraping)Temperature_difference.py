import csv

def temperature(city_input, date1_input, date2_input):
	#input the date and city name, noted that the date's format is XXXXXXXX in number
	city_CN = city_input
	date1 = date1_input
	date2 = date2_input

	trans_dict = {'曼谷':'Bangkok', '釜山':'Busan', '香港':'Hong Kong', '京都':'Kyoto', '沖繩':'Okinawa', '大阪':'Osaka',
				'芭達雅':'Phatthaya', '北海道':'Hokkaido', '普吉島':'Sapporo', '首爾':'Seoul', '新加坡':'Singapore', 
				'東京':'Tokyo'}
	
	city = trans_dict[city_CN]
	city_path = city + '.csv'

	#open the temperature file
	file =  '/Users/leepinghsun/Documents/GitHub/G21/main_function/氣溫csv/' + city_path  # need to change between computers

	#the number of days in each month
	month = [31,28,31,30,31,30,31,31,30,31,30,31]

	#change the date into day X in each year
	day1 = 0
	day2 = 0
		
	for i in range(10 * int(date1[4]) + int(date1[5])-1) :
		day1 += month[i]

	day1 += 10 * int(date1[6]) + int(date1[7])


	for i in range(10 * int(date2[4]) + int(date2[5])-1) :
		day2 += month[i]

	day2 += 10 * int(date2[6]) + int(date2[7])
		
	#find the temperature data for that specific day	
	n = 0
	with open(file, newline='', encoding='cp950') as csvFile:
		#read directly: read the csv file 
		rows = csv.reader(csvFile)
		# for loop the rows
		for row in rows:
			n += 1 
			if day1 + 1 <= n <= day2 + 1:
				print("最高氣溫：" + str(row[1]))
				print("最低氣溫：" + str(row[2]))

# temperature('香港', '20190919', '20190923')  sample input
