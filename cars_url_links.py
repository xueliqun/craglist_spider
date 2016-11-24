from bs4 import BeautifulSoup
import requests
import time
import pymysql

urls_list = ["https://newyork.craigslist.org/search/ctd?s={}00".format(str(i)) for i in range(25)]
url_host = "https://newyork.craigslist.org"
def get_save_allinks():
    for url in urls_list:
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text, 'lxml')
        links = soup.select('a.result-title.hdrlnk')
        for link in links:
            onecar_url = url_host + link.get('href')
            conn = pymysql.connect(host='127.0.0.1', port=3306,user = 'root', passwd = 'mysql',db='craglist_data', charset='utf8')
            cur = conn.cursor()
            cur.execute("INSERT INTO car_urls(car_link) VALUES(%s)",(onecar_url))
            conn.commit()
            print(onecar_url)
        time.sleep(1)
        

get_save_allinks()
