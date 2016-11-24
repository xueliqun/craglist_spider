import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306,user = 'root', passwd = 'mysql',db='craglist_data', charset='utf8')
cur1 = conn.cursor()
cur1.execute("SELECT car_link FROM car_urls")
rows = cur1.fetchall()
car_links = []
for i in rows:
    car_links.append(i[0])