import base64
from requests import Session
import datetime
import time
import json
import os

url = 'http://www.aqistudy.cn/html/city_detail.html?v=1.8'
# data_url = 'http://www.aqistudy.cn/api/getdata_citydetail.php'
data_url = 'http://www.aqistudy.cn/api/getdata_cityweather.php'
s = Session()
s.get(url)

filename = '2016beijing.csv'

if not os.path.exists(filename):
	f = open(filename,'w+')
	f.close()

startday = datetime.datetime(2016,10,8)
endday = datetime.datetime(2016,10,9)
oneday = datetime.timedelta(days = 1)
day = startday

while day < endday:
	print day
	time.sleep(10)
	endTime = day + oneday
	startTime = base64.b64encode(str(day))
	endTime = base64.b64encode(str(endTime))
	day = day + oneday
	postdata = {
		'city':'5L+d5a6a',# baoding
		# 'city':'5YyX5Lqs', # beijing
		'type':'U0U5VlVnPT0=',
		'startTime':startTime,
		'endTime':endTime
		}
	
	data = s.post(data_url,data = postdata).text
	# print data
	city_detail = base64.b64decode(base64.b64decode(data))
	try:
		data = json.loads(city_detail)
		json.dump(data,indent=4)
		for item in data['rows']:
			times = item['time']
			pm2_5 = item['pm2_5']
			pm10 = item['pm10']
			aqi = item['aqi']
			with open(filename,'a+') as fhand:
				temp = '%s,%s,%s,%s,\n' %(times,pm2_5,pm10,aqi)
				fhand.write(temp)
	except:
		data = json.loads(city_detail[0:-6])
		json.dump(data,indent=4)
		for item in data['rows']:
			times = item['time']
			pm2_5 = item['pm2_5']
			pm10 = item['pm10']
			aqi = item['aqi']
			with open(filename,'a+') as fhand:
				temp = '%s,%s,%s,%s,\n' %(times,pm2_5,pm10,aqi)
				fhand.write(temp)
	
