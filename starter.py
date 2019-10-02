import math
import sys


from mainController import *

class Starter():
	def __init__(self):
		self.mainer=MainController()
	
	def start_game(self):
		self.mainer.Flow()
	

if __name__ == '__main__':
	m=Starter()
	game_choice=raw_input("Press something to start:")
	m.start_game()
	

	
