#! usr/bin/env python
# -*- coding: utf-8 -*-
# system imports

import random
import numpy as np
import sys
from time import time, sleep
import math
import serial
#import threading
#from __future__ import division
#from __future__ import print_function
from rasp_to_ardu import *
from eye import *


class MainController():
	def __init__(self):
		# start the arduino communication
		self.arduino = OurPreciousDriver(stabValues=[0,0,0,0]) #98:D3:31:60:30:AE
		# start camera
		self.imager = Eye()
		
	
	def Flow(self): # main game controller

		while True: # check whether a figure exists on the field
			figure=self.imager.get_figure_cg()
			if not figure[0]==-5:
                                break

		# there is a shape on the field, let's drive through it..
		self.rotate_to_shape()
		self.drive_to_shape()

	# Game Loop Methods
	def rotate_to_shape(self):
		cg_shape = self.imager.get_figure_cg()

		error=abs(cg_shape[0] - 160)
		while error > 5:
			if cg_shape[0]>160:
				self.rotate(50, True)
			else:
				self.rotate(50, False)
			cg_shape = self.imager.get_figure_cg()
			error = abs(cg_shape[0] - 160)
		self.drive(speed=0)

        def drive_to_shape(self):
		self.drive(speed=70)
		i=0
		while i<3000000:
                        i=i+1
		self.drive(speed=0)

	def drive(self,speed, direc=False): #Driving of motor, linearly
		self.arduino.drive(val=speed,direction=direc)

	def rotate(self,speed, direc): #rotation procedure
		# direc=True rotates cw
		self.arduino.rotate(value=speed, direction=direc)
