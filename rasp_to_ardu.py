# !/usr/bin/env python
import serial
import sys
import math
from collections import deque
from copy import deepcopy
#from __future__ import division
#from __future__ import print_function

import RPi.GPIO as GPIO
import smbus
import time

#.encode(encoding='UTF-8')

class I2CInterfaceHandler:

  def __init__(self):
    self.I2C_BUS = 1
    self.I2C_SLAVE = 0x03
    self.I2C_MASTER = 0x01
    self.i2c=smbus.SMBus(self.I2C_BUS)

  def send(self, data):
    messageToSend = []
    
    for element in data:
      messageToSend.append(element)
    self.i2c.write_i2c_block_data(self.I2C_SLAVE, self.I2C_MASTER, messageToSend)
    print 'Data sended: '+str(messageToSend[0])+' '+str(messageToSend[1])+' '+str(messageToSend[2])+' '+str(messageToSend[3])
    print '.............................'
    time.sleep(0.2)
# Arduino Serial Data Packaging Handler
class SerialDataPacker:
	names = {}  # Dict for names to data indexes
	initVals = []  # List of middle uSec values
	curVals = []  # List of current list of values
	data = []

	def __init__(self, initVals, defaultNumBytes=2):

		self.defaultNumBytes = defaultNumBytes
		self.initVals = initVals
		self.num = len(self.initVals)
		# Set the current values to be the middle values
		self.curVals = deepcopy(self.initVals)
		# Prepare data package

	def setDriveVals(self,value,direction):
		self.data=[]
		if direction==True: # go forward
			self.data.append(value)
			self.data.append(1)
			self.data.append(value)
			self.data.append(1)
		else: # go backward
			self.data.append(value)
			self.data.append(0)
			self.data.append(value)
			self.data.append(0)

	def setRotateVals(self, value, direction):
		self.data=[]
		if direction==True: # cw rotation
			self.data.append(value)
			self.data.append(1)
			self.data.append(value)
			self.data.append(0)
		else: # ccw rotation
			self.data.append(value)
			self.data.append(0)
			self.data.append(value)
			self.data.append(1)


class OurPreciousDriver:
	def __init__(self, stabValues=None, dataPacker=None):

		if stabValues == None:
			self.stabValues = [0, 0, 0, 0]
		else:
			self.stabValues = stabValues

		self.arduFace = I2CInterfaceHandler()

		if dataPacker == None:
			self.dataPacker = SerialDataPacker(self.stabValues)
		else:
			self.dataPacker = dataPacker()

	def stop(self):
		self.dataPacker.setDriveVals(self.dataPacker.initVals)
		self.arduFace.send(self.dataPacker.data)

	def drive(self, val=None,direction=True):
		if val != None:
			self.dataPacker.setDriveVals(val,direction)
		self.arduFace.send(self.dataPacker.data)

	def rotate(self,value=None, direction=True):
		if value != None:
			self.dataPacker.setRotateVals(value, direction)
		self.arduFace.send(self.dataPacker.data)

rcvBuffer = deque()
