import time
from Adafruit_IO import Client
from sds011 import SDS011
import aqi

DEBUG = True


aio = Client('TennisBowling', 'aio_gqkK69eDWJS767YXKJERgogcj30R')
print('yo mama logged in')

sensor = SDS011('/dev/ttyUSB0', use_query_mode=True)

# calibrate itself real fast
if DEBUG: print('calibrating')
sensor.sleep(sleep=False)
if not DEBUG: time.sleep(15)

while True:
	if DEBUG: print('beginning collection')
	data = sensor.query()

	quality_rating = (-1, aqi.US_2_5.apply(data[0]), aqi.US_10.apply(data[1]))
	quality_rating = max(list(filter(lambda x: x != None, quality_rating)))
	quality_rating = round(quality_rating, 2)

	# print debug data
	if DEBUG:
		print('2.5: {0} ug/m3, 10: {1} ug/m3'.format(*data))
		print('AQI: {0}'.format(quality_rating))

	# Sned/Senf it over to AIO
	aio.send('kirklandtwofive', data[0])
	aio.send('kirklandten', data[1])
	aio.send('kirklandaqi', quality_rating)


	# wait an arbitrary amount of secs before getting the next reading
	time.sleep(10)
