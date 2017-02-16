import paho.mqtt.client as mqtt
import sys

import time

from car import Car
from queue import Queue

queue = Queue()
car = Car(2)


class Subscriber:

	def __init__(self, topic, host, port):
		self.topic = topic
		self.host = host
		self.port = port

	def subscribe(self):
		print ("subscribe")
		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message

		self.client.connect(self.host, self.port, 60)

		self.client.loop_forever()


	# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("connected with result code " + str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("innon")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global queue
	global car
	print ("Topic: " + msg.topic + "\nMessage: " + str(msg.payload))
	command_not_Split = str(msg.payload)
	split_command = command_not_Split.split(":")
	if len(split_command)>1:
		direction = split_command[0];
		print (direction)
		if direction == 'w':
			turn_command = queue.dequeue()
			if turn_command is not None:
				car.fwd_until_dist(get_dist(turn_command))
				do_turn(get_direction(turn_command))
				print ("going to sleep for" + split_command[1])
				sleep_time = float(split_command[1]) / 1000
				time.sleep(sleep_time)
			car.do_fwd()  # Move forward
		elif direction == 'a':
			queue.enqueue(split_command)
			car.do_stop()
		elif direction == 'd':
			queue.enqueue(split_command)
			car.do_stop()
		elif direction == 'x':
			car.do_stop()  # Stop
		elif direction == 'z':
			print "Exiting"  # Exit
			sys.exit()
		else:
			print "Wrong Command, Please Enter Again"

def get_dist(command):
	return command[2]

def get_direction(command):
	return command[0]


def do_turn(direction):
	if direction == 'a':
		car.do_left()
	elif direction == 'd':
		car.do_right()


subscriber = Subscriber("innon", "test.mosquitto.org", 1883)
subscriber.subscribe()