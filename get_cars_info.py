from bs4 import BeautifulSoup
import requests
import pymysql
import time
import get_links_from_sql
import re


#url = 'https://newyork.craigslist.org/brk/ctd/5889770298.html'
headers = {
    'Cookie':'cl_def_hp=newyork; cl_b=wj2TQbmx5hGcxHD3O0n9jQpo+xQ; cl_tocmode=sss%3Agrid',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36'
}
links = get_links_from_sql.car_links
for link in links[3:]:
    try:
        web_data = requests.get(link, headers = headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        price = soup.select('span.price')[0].text
        price = re.findall("\d+", price)[0]
        title = soup.select('p.attrgroup > span')
        data = {'title':None, 'paint color':None, 'odometer':None, 'fuel':None, 'drive':None, 'type':None,
                'title status':None, 'price':None}
        for i in title[1:]:
            try:
                data[i.text.split(':')[0]] = i.text.split(':')[1].strip()
            except:
                pass
        data['title'] = title[0].text
        data['price'] = price
        conn = pymysql.connect(host='127.0.0.1', port=3306,user = 'root', passwd = 'mysql',db='craglist_data', charset='utf8')
        cur = conn.cursor()
        cur.execute("INSERT INTO cars_info(Title, Paint_color, Odometer, Fuel, Drive, CarType, Title_status,Price) \
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", (data['title'],data['paint color'],int(data['odometer']),data['fuel'],data['drive'],data['type'],data['title status'], int(data['price'])))

        print(data)
        conn.commit()
        time.sleep(0.5)
    except:
        pass
