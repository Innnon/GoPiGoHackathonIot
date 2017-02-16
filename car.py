import random


class Car:

	def __init__(self, num):
		self.num = num

	def get_dist_from_wall(self):
		print ("get dist from wall")
		return random.randint(0, 100)

	def do_fwd(self):
		print ("fwd : " + str(self.num))

	def do_left(self):
		print ("left : " + str(self.num))

	def do_right(self):
		print ("right : " + str(self.num))
	def do_stop(self):
		print ("stop : " + str(self.num))

	def fwd_until_dist(self, dist):
		print ("drive forward until we are " + str(dist) + " from wall")