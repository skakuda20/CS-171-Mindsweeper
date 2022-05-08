# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

import random
from AI import AI
from Action import Action


class MyAI( AI ):

	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.__coveredTiles = 0
		self.__totalMines = totalMines
		self.__currX = startX
		self.__currY = startY
		self.__moveCount = 0

		self.__lastAction = Action(AI.Action.UNCOVER, self.__currX, self.__currY)

		#have a copy of the board to update the board status on our end
		self.__board = []
		self.create_board()


		pass
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":
		# successful game: UNCOVER #C*#R-#M times then LEAVE
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################

		#if take too many step, 365 for now, make randome move
		if (self.__moveCount + 1 > 365):
			action = AI.Action(random.randrange(1, len(AI.Action)))
			x = random.randrange(self.__colDimension)
			y = random.randrange(self.__rowDimension)
			self.__moveCount += 1
			return Action(action, x, y)


		# are we done? #CoveredTiles = #Mines ->LEAVES
		if (self.__coveredTiles == self.__totalMines):
			return Action(AI, Action.LEAVE);
		# otherwise need figure out UNCOVER X,Y
		""" E.g. if EffectiveLabel(x) = NumUnMarkedNeighbors(x), then 
		all UnMarkedNeighbors(x) must be mines (mark them as 
		such on the board; this is likely to reduce effective labels of 
		other nearby uncovered tiles, so that the rules-of-thumb 
		can be fired again)
		• E.g. if EffectiveLabel(x) = 0, then all UnMarkedNeighbors(x) 
		must be safe (you can UNCOVER them) """

		self.__currX = self.__lastAction.getX()
		self.__currY = self.__lastAction.getY()

		# uncover the tile and set the status 0-8 else flagtheTile
		if (number >= 0 and number <= 8):
			self.uncoverTile()
		else:
			self.flagTile()

		#simple rule of thumb logic UNCOVER X,Y

		#IF not found use another logic

		#If not found again guess use approximation


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	def uncoverTile(self, num: int):
		self.board[self.__currX][self.__currY] = num

	# use 9 as flag for now
	def flagTile(self):
		self.board[self.__currX][self.__currY] = 9


	def create_board(self):
		for i in range(self.__rowDimension):
			row = []
			for j in range(self.__colDimension):
				# set to ??? -1 for now cause Idk what else to put
				row.append(-1)
			self.__board.append(row)


