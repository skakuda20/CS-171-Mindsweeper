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
		self.__coveredTiles = rowDimension * colDimension
		self.__totalMines = totalMines
		self.__currX = startX
		self.__currY = startY
		self.__moveCount = 0

		self.__lastAction = Action(AI.Action.UNCOVER, self.__currX, self.__currY)

		# to uncover list
		self.__toUncover = [(self.__currX, self.__currY)]
		# tiles that are aleady uncovered
		self.__Uncovered = []

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
		if (number == 0):
			self.uncoverAdjTiles()
		else:
			self.checkNumUnMarked(number)

		# if toUncover list not empty, get the first available one and uncover it
		if (len(self.__toUncover) > 0):
			action = AI.Action(1) #uncover
			self.__lastAction = Action(action, self.__toUncover[0][0], self.__toUncover[0][1])
			return self.__lastAction
			
		#IF not found use another logic

		#If not found again guess use approximation


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# loop through all adjacent tiles and check how many are unmarked
	# if it equals to num meaning all unmarked tiles are bomb marked them (10)? whateve represent bomb
	def checkNumUnMarked(self, num: int):
		numUnmrked = 0

		# Check all adjacent tiles:

		# Check tiles in row below if applicable
		if (self.__currX < self.__rowDimension - 1):
			# Check bottom left
			if (self.__currY > 0):
				if (self.__board[self.__currX - 1][self.__currY - 1] == -1):
					numUnmrked += 1
			# Check bottom right
			if (self.__currY < self.__colDimension - 1):
				if (self.__board[self.__currX - 1][self.__currY + 1] == -1):
					numUnmrked += 1
			# Check bottom mid
			if (self.__board[self.__currX - 1][self.__currY] == -1):
				numUnmrked += 1
		
		# Check mid left
		if (self.__currY > 0):
			if (self._board[self.__currX][self.__currY - 1] == -1):
				numUnmrked += 1
		# Check mid right
		if (self.__currY < self.__colDimension - 1):
			if (self._board[self.__currX][self.__currY + 1] == -1):
				numUnmrked += 1

		# Check tiles in row above if applicable
		if (self.__currX > 0):
			# Check top left
			if (self.__currY > 0):
				if (self.__board[self.__currX + 1][self.__currY - 1] == -1):
					numUnmrked += 1
			# Check top right
			if (self.__currY < self.__colDimension - 1):
				if (self.__board[self.__currX + 1][self.__currY + 1] == -1):
					numUnmrked += 1
			# Checkk top mid
			if (self.__board[self.__currX + 1][self.__currY] == -1):
				numUnmrked += 1
		
		return numUnmrked == num


	def uncoverAdjTiles(self):
		x = self.__currX
		y = self.__currY
		
		# check all 8 adjacent tiles if they are already uncovered; if not add them to toUncover list
		
		# little messy if u can double check that ll be nice

		if (x-1 >= 0):
			if (y-1 >= 0 and ((x-1,y-1) not in self.__Uncovered)):
				self.__toUncover.append((x-1,y-1))
			if (y+1 <= len(self.__board[x]) and ((x-1,y+1) not in self.__Uncovered)):
				self.__toUncover.append((x-1,y+1))
			if ((x-1,y) not in self.__Uncovered):
				self.__toUncover.append((x-1,y))

		if (x+1 <= self.__board):
			if (y-1 >= 0 and ((x+1,y-1) not in self.__Uncovered)):
				self.__toUncover.append((x+1,y-1))
			if (y+1 <= len(self.__board[x]) and ((x+1,y+1) not in self.__Uncovered)):
				self.__toUncover.append((x+1,y+1))
			if ((x+1,y) not in self.__Uncovered):
				self.__toUncover.append((x+1,y))

		if (y-1 >= 0 and ((x,y-1) not in self.__Uncovered)):
			self.__toUncover.append((x,y-1))

		if (y+1 <= self.__board[x] and ((x,y+1) not in self.__Uncovered)):
			self.__toUncover.append((x,y+1))


	def uncoverTile(self, num: int):
		if ((self.__currX, self.__currY) in self.__toUncover):
			self.__board[self.__currX][self.__currY] = num
			self.__Uncovered.append((self.__currX, self.__currY))
			self.__coveredTiles -= 1
			self.__toUncover.pop(0)

	# use 9 as flag for now
	def flagTile(self):
		self.__board[self.__currX][self.__currY] = 9


	def create_board(self):
		for i in range(self.__rowDimension):
			row = []
			for j in range(self.__colDimension):
				# set to ??? -1 for now cause Idk what else to put
				row.append(-1)
			self.__board.append(row)


