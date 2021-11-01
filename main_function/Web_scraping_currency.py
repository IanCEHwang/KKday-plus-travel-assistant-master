from re import match
from io import BytesIO
from lxml import etree
from six import u
from six.moves.urllib import request
import ssl

class Currency():
    __CURRENT_QUOTE_URL = 'http://rate.bot.com.tw/xrt?Lang=zh-TW'
    __HISTORY_QUOTE_URL_PATTERN = 'http://rate.bot.com.tw/xrt/quote/{range}/{currency}'
    __NAME_DICT = {}


    def __parse_tree(self, url):
        context = ssl._create_unverified_context()
        contents = request.urlopen(url, context=context).read()
        
        return etree.parse(BytesIO(contents), etree.HTMLParser())
        

    def now_all(self):
        """ 取得目前所有幣別的牌告匯率
            :rtype: dict
        """
        ret = {}
        tree = self.__parse_tree(self.__CURRENT_QUOTE_URL)
        table = tree.xpath(u'//table[@title="牌告匯率"]')[0]
        quote_time = tree.xpath(u('//span[@class="time"]/text()'))[0]

        for row in table.xpath('tbody/tr'):
            tds = row.xpath('td')
            full_name = tds[0].xpath('div/div[@class="visible-phone print_hide"]/text()')[0].strip()
            key = match(r'.*\((\w+)\)', full_name).group(1)
            self.__NAME_DICT[key] = full_name

            cash_buy = tds[1].text
            cash_sell = tds[2].text
            rate_buy = tds[3].text
            rate_sell = tds[4].text

            ret[key] = (quote_time, cash_buy, cash_sell, rate_buy, rate_sell)

        return ret


    def now(self, currency):
        """ 取得目前指定幣別的牌告匯率
            :param str currency: 貨幣代號
            :rtype: list
        """
        return self.now_all()[currency]


    def currencies(self):
        """ 取得所有幣別代碼
            :rtype: list
        """
        return list(self.currency_name_dict().keys())


    def currency_name_dict(self):
        """ 取得所有幣別的中文名稱
            :rtype: dict
        """
        if not self.__NAME_DICT:
            self.now_all()
        return dict(self.__NAME_DICT)


    def __parse_history_page(self, url, first_column_is_link=True):
        ret = []

        tree = self.__parse_tree(url)
        table = tree.xpath(u'//table[@title="歷史本行營業時間牌告匯率"]')[0]
        for row in table.xpath('tbody/tr'):
            if first_column_is_link:
                t = row.xpath('td[1]/a/text()')[0]
                name, cash_buy, cash_sell, spot_buy, spot_sell = row.xpath('td/text()')
            else:
                t, name, cash_buy, cash_sell, spot_buy, spot_sell = row.xpath('td/text()')
            ret.append((t, cash_buy, cash_sell, spot_buy, spot_sell))

        return ret


    def past_day(self, currency):
        """ 取得最近一日的報價
            :param str currency: 貨幣代號
            :rtype: list
        """
        return self.__parse_history_page(
            self.__HISTORY_QUOTE_URL_PATTERN.format(currency=currency, range='day'),
            first_column_is_link=False)


    def past_six_month(self, currency):
        """ 取得最近六個月的報價(包含貨幣名稱)
            :param str currency: 貨幣代號
            :rtype: list
        """
        return self.__parse_history_page(self.__HISTORY_QUOTE_URL_PATTERN.format(currency=currency, range='l6m'))


    def specify_month(self, currency, year, month):
        """ 取得指定月份的報價(包含貨幣名稱)
            :param str currency: 貨幣代號
            :param int year: 年
            :param int month: 月
            :rtype: list
        """
        month_str = '{}-{:02}'.format(year, month)
        return self.__parse_history_page(self.__HISTORY_QUOTE_URL_PATTERN.format(currency=currency, range=month_str))


C = Currency()

def currency_function(country_input):
    country_dict = {'韓國': 'KRW', '日本': 'JPY', '泰國': 'THB', '新加坡': 'SGD', '香港': 'HKD'}
    country = country_input  
    country_eng = ''
    for key in country_dict:
        if country == key:
            country_eng = country_dict[key]
            break

    nowadays = C.now(country_eng)  # 印出現在匯率資料
    nowout = nowadays[2]
    # print(country + '現在的匯率為：' , nowadays[2])
    past_6month = C.past_six_month(country_eng)  # 取得六個月內所有匯率收盤資料
    past6out = past_6month[-1][2]
    # print(country + '六個月前的匯率為：', past_6month[-1][2])

    lowest = 10000
    lowest_day = []
    for i in past_6month:  # 找出最低匯率，由於取得的會是elementTree的資料，所以先encode成utf-8資料再decode成string資料
        if float(i[2].encode().decode()) < lowest:
            lowest = float(i[2].encode().decode())
            lowest_day = []
            lowest_day.append(i)
        elif float(i[2].encode().decode()) == lowest:
            lowest_day.append(i)

    # print(country + '六個月以來的最低匯率為：', end=' ')
    # for i in lowest_day:
    #     print(i[0], end=' ')
    # print(lowest)

    return nowout, past6out, lowest_day, lowest
