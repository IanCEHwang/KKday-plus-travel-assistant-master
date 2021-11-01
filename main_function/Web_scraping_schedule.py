#打開kkday ouput.csv
import csv

def schedule(kwList_input, nolist_input, SelectCity_input):

    fn = '../爬蟲們/kkday_csv/tample.csv'
    fh = open(fn, 'r', newline = '', encoding = 'utf-8')
    csv1 = csv.DictReader(fh)
    fields = csv1.fieldnames

    #輸入關鍵字(kw)，用空格分隔後存進kwList
    kwList = kwList_input.split()
    # print(kwList)
    noList = nolist_input.split()
    # print(noList)
    SelectCity = SelectCity_input

    #SelectCity = '沖繩' #測試時打開
    resultNum = 0 #找到幾筆符合結果
    resultList = [] #存放符合的結果
    #走訪ouput.csv的info
    for aline in csv1:
        if SelectCity in aline[fields[1]]: 
            count = 0 #檢查找到的kw數
            info = aline[fields[5]]

        #走訪kwList中的關鍵字，查看是否皆出現在某行程的'info'中
            if len(kwList) == 0 and len(noList) == 0:
                count = len(kwList)

            else:
                for kw in kwList:
                    if kw in info:
                        count += 1
            #走訪noList中不想要的關鍵字        
                for no in noList:
                    if no in info:
                        count -= 1
                
            if count == len(kwList):
                resultNum += 1
                result = [] #存放符合結果的內容
                result.append('行程名稱：' + aline[fields[3]])
                result.append('價格：' + aline[fields[4]])
                result.append('介紹：' + aline[fields[5]])
                result.append('連結：' + 'https://www.kkday.com/zh-tw/product/' + aline[fields[2]])
                resultList.append(result)

    if len(resultList) == 0:
        answer = '查無符合的結果！'
        return answer
    else:
        return resultList
        # for r in resultList:
        #     print(r[0])
        #     print(r[1])
        #     print(r[3])
        #     print()