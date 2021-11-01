from re import match
from io import BytesIO
from lxml import etree
from six import u
from six.moves.urllib import request

# Get the latest currency exchange rate from Taiwanese bank
class Currency():
    __CURRENT_QUOTE_URL = 'http://rate.bot.com.tw/xrt?Lang=zh-TW'
    __HISTORY_QUOTE_URL_PATTERN = 'http://rate.bot.com.tw/xrt/quote/{range}/{currency}'
    __NAME_DICT = {}


    def __parse_tree(self, url):
        contents = request.urlopen(url).read()
        
        return etree.parse(BytesIO(contents), etree.HTMLParser())
        

    def now_all(self):
        """ Get the exchange rates for all currencies
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
        """ Get the exchange rate for target currency 
            :param str currency: 貨幣代號 currency id
            :rtype: list
        """
        return self.now_all()[currency]


    def currencies(self):
        """ get the id for all the currencies
            :rtype: list
        """
        return list(self.currency_name_dict().keys())


    def currency_name_dict(self):
        """ get the chinese name for all the currencies
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
        """ Get the currency exchange rate one-day-before
            :param str currency: 貨幣代號 currency id
            :rtype: list
        """
        return self.__parse_history_page(
            self.__HISTORY_QUOTE_URL_PATTERN.format(currency=currency, range='day'),
            first_column_is_link=False)


    def past_six_month(self, currency):
        """ Get the currency name and exchange rate 6 months ago from now
            :param str currency: 貨幣代號 currency id
            :rtype: list
        """
        return self.__parse_history_page(self.__HISTORY_QUOTE_URL_PATTERN.format(currency=currency, range='l6m'))


    def specify_month(self, currency, year, month):
        """ get the currency exchange rate and name for the terget month
            :param str currency: 貨幣代號 currency id
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
    for key in country_dict:
        if country == key:
            country_eng = country_dict[key]
            break

    nowadays = C.now(country_eng)  # print the currency data 
    print(country + '現在的匯率為：' , nowadays[2])
    past_6month = C.past_six_month(country_eng)  # print the currency data for 6 months before
    print(country + '六個月前的匯率為：', past_6month[-1][2])

    lowest = 10000
    lowest_day = []
    for i in past_6month:  # find the lowest exchange in the past 6 months. The data is in the form of elementTree, encoded as utf-8 and then decode as string
        if float(i[2].encode().decode()) < lowest:
            lowest = float(i[2].encode().decode())
            lowest_day = []
            lowest_day.append(i)
        elif float(i[2].encode().decode()) == lowest:
            lowest_day.append(i)

    print(country + '六個月以來的最低匯率為：', end=' ')
    for i in lowest_day:
        print(i[0], end=' ')
    print(lowest)
