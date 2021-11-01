import csv
import urllib.request
import re

city = input()	

with open('C:\\Users\\user\\Desktop\\' + str(city) + '.csv','w', newline = '') as csvfile :
	
	writer = csv.writer(csvfile)
	writer.writerow(['日期', '最高氣溫', '最低氣溫'])
	
	for i in range(1,13) :
		
		if i < 10 :
			month = "20180" + str(i)
		else :
			month = "2018" + str(i)
		
		request=urllib.request.Request("http://tianqi.2345.com/t/inter_history/js/asia/{m}/{c}_{m}.js".format(m=month,c=city))
		request.add_header("Referer","http://tianqi.2345.com/inter_history/asia/{c}.htm".format(c=city))

		response=urllib.request.urlopen(request)
		html=response.read().decode("gbk")
		content=str.split(html,"=")[1].split("]")[0].split("tqInfo:[")[1]
		re_object=re.findall("{.*?}",content)
	
	
		for item in re_object:
			s_item = item.split(',')
			if len(s_item) >= 3 :
				date = s_item[0][6:16]
				high_tem = s_item[1][8:-1]
				low_tem = s_item[2][8:-1]
			writer.writerow([date, high_tem, low_tem])


	



