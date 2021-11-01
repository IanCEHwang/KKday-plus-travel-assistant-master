import pandas as pd
url = 'https://www.boca.gov.tw/sp-trwa-list-1.html'
table = pd.read_html(url, header=1)    # read the url, and set the first line as header
df = pd.DataFrame(table[0])            # table[0] for the countries in East Asia 


"""clean up the data in dataframe, seperate the country's English and Chinese name in the first column"""
tmp_country_list = list( df['國家'] )    # change'國家'(country) data into a list 
country_list = list()

for country in tmp_country_list:
    chn_eng = country.split()
    
    # if only one English and one Chinese name included
    if len(chn_eng) == 2:
        new_sublist = [ chn_eng[0], chn_eng[1] ]
    
    # if the English name for the country include more than one word
    if len(chn_eng) > 2:
        tmplist = chn_eng[1:]
        eng = ''
        for i in range(len(tmplist)):
            if i == 0:
                eng += tmplist[i]
                continue
            eng += ' ' + tmplist[i]
        new_sublist = [ chn_eng[0], eng ]
    
    country_list.append(new_sublist)

df2 = pd.DataFrame(country_list, columns = ['國家(中文)', '國家(英文)'])


"""combine two dataframes, including the cleaned-up df2 and the df scraping from the website"""
df3 = pd.merge(df2, df[['國家地區','最新警示提醒']], right_index=True, left_index=True)
df4 = df3.set_index( '國家(中文)' )


"""print out the target countries in csv"""
df5 = df4.loc[ ['韓國', '日本', '泰國', '新加坡'], ['國家地區', '最新警示提醒'] ]
df5.to_csv('safety_some.csv')
