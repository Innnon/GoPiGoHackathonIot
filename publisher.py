import paho.mqtt.client as mqtt
import sys

import time

from car import Car

current_milli_time = lambda: time.time()

class Publisher:
	def __init__(self, host, port, topic):
		self.should_run = True
		self.host = host
		self.port = port
		self.topic = topic
		self.car = Car(1)

	def run(self):

		mqttc = mqtt.Client("python_pub")
		mqttc.connect(self.host, self.port)
		first_time = True
		time_of_last_command = current_milli_time()
		while (self.should_run):

			print "Enter the Command:",
			direction = raw_input()  # Fetch the input from the terminal
			distance_from_wall = self.car.get_dist_from_wall()
			command_time = current_milli_time() - time_of_last_command
			time_of_last_command = current_milli_time()
			print (command_time)
			if direction == 'w':
				self.car.do_fwd()  # Move forward
			elif direction == 'a':
				self.car.do_left()  # Turn left
			elif direction == 'd':
				self.car.do_right()  # Turn Right
			elif direction == 'x':
				self.car.do_stop()  # Stop
			elif direction == 'z':
				print "Exiting"  # Exit
				sys.exit()
			else:
				print "Wrong Command, Please Enter Again"

			msg = self.build_message(direction, command_time, distance_from_wall)


			time.sleep(.1)
			mqttc.publish(self.topic, msg)

	def build_message(self, direction, t_time, dist):
		msg = str(direction) + ":" + str(t_time) + ":" + str(dist)
		print (msg)
		return  msg


publisher = Publisher("test.mosquitto.org", 1883, "innon")
publisher.run()