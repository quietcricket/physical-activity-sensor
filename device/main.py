import network
import time
import urequests
import settings
from ultrasonic import Ultrasonic


# setting pins to accomodate Ultrasonic Sensor (HC-SR04)
trigPin = 14
echoPin = 12

# sensor needs 5V and ground to be connected to pyboard's ground

# creating two Ultrasonic Objects using the above pin config

sensor = Ultrasonic(trigPin, echoPin)

# 100 milli seconds interval, 10 samples per second
interval=100 
# 20 seconds per call to the server
# can't post too big data
max_count=int(1000/interval)*20

data=['-1']*max_count

index=0

wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.connect(settings.WIFI_SSID,settings.WIFI_PASSWORD)

def get_distance():
	global index
	# get sensor1's distance in cm
	data[index]=sensor.distance_in_cm()

	index+=1
	if index==max_count:
		index=0
		try:
			response = urequests.post(settings.SERVER_URL, data = ",".join(data))
		except Exception as e:
			pass

# prints values every second
while True:
	get_distance()
	time.sleep_ms(interval)
