# open kkday ouput.csv
import csv

def schedule(kwList_input, nolist_input, SelectCity_input):

    fn = '/Users/leepinghsun/Documents/GitHub/G21/爬蟲們/kkday_csv/tample.csv'
    fh = open(fn, 'r', newline = '', encoding = 'utf-8')
    csv = csv.DictReader(fh)
    fields = csv.fieldnames

    #input the keywords(kw), split it with space and put into kwList
    kwList = kwList_input.split()
    noList = nolist_input.split()
    SelectCity = SelectCity_input

    #SelectCity = '沖繩'(Okinawa) #open while testing
    resultNum = 0 #the corresponding results found 
    resultList = [] #then put into the resultlist
    #go through the info in ouput.csv
    for aline in csv:
        if SelectCity == aline[fields[1]]: 
            count = 0 #to check how many keywords are found 
            info = aline[fields[5]]
        #go through the keywords in kwList, check if it is in the traveling package description
            if len(kwList) == 0 and len(noList) == 0:
                count = len(kwList)

            else:
                for kw in kwList:
                    if kw in info:
                        count += 1
            #go through the unwanted keywords in noList         
                for no in noList:
                    if no in info:
                        count -= 1
                
            if count == len(kwList):
                resultNum += 1
                result = [] #a list for the corresponding results package found
                result.append('行程名稱：' + aline[fields[3]])
                result.append('價格：' + aline[fields[4]])
                result.append('介紹：' + aline[fields[5]])
                result.append('連結：' + 'https://www.kkday.com/zh-tw/product/' + aline[fields[2]])
                resultList.append(result)

    if resultNum == 0:
        print('查無符合的結果！') #no result found

    for r in resultList:
        print(r[0])
        print(r[1])
        print(r[3])
        print()
