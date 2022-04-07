import time
from sds011 import SDS011
import aqi
from datetime import datetime
import sqlite3

DEBUG = True

sensor = SDS011('COM3', use_query_mode=True)
db = sqlite3.connect('airquality.db')

# calibrate itself real fast
if DEBUG: print('calibrating')
sensor.sleep(sleep=False)
time.sleep(15)

try:
	while True:
		if DEBUG: print('beginning collection')
		data = sensor.query()

		quality_rating = (-1, aqi.US_2_5.apply(data[0]), aqi.US_10.apply(data[1]))
		quality_rating = max(list(filter(lambda x: x != None, quality_rating)))
		quality_rating = round(quality_rating, 2)

		# print debug data
		if DEBUG:
			print(f'2.5: {data[0]} ug/m3, 10: {data[1]} ug/m3')
			print(f'AQI: {quality_rating}')

		# sned to database
		db.execute("""INSERT INTO data ("pm25", "pm10", "aqi", "time") VALUES (?, ?, ?, ?);""", (data[0], data[1], quality_rating, int(datetime.now().timestamp())))
		db.commit()

		# wait an arbitrary amount of secs before getting the next reading
		time.sleep(10)
except:
	db.commit()
	db.close()
	raise