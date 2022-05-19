# COPY OF MyAI.py SUBMITTED AS MINIMAL AI

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
		self.__bomblist = []
		self.__numFlaged = 0
		#have a copy of the board to update the board status on our end
		self.__board = []
		self.create_board()
		
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

		
	def getAction(self, number: int) -> "Action Object":
		# successful game: UNCOVER #C*#R-#M times then LEAVE
		########################################################################
		#							YOUR CODE BEGINS						   #
		########################################################################
		
		self.printBoard()

		#if take too many step, 365 for now, make randome move
		if (self.__moveCount + 1 > 365):
			action = AI.Action(random.randrange(1, len(AI.Action)))
			x = random.randrange(self.__colDimension)
			y = random.randrange(self.__rowDimension)
			self.__moveCount += 1
			return Action(action, x, y)


		
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

		print ("Len of bomList:", len(self.__bomblist))		# DELETE AFTER
		print("Len of self.__toUncover before: ", len(self.__toUncover))	# DELETE AFTER
		print("(x, y):", self.__currX, self.__currY)

		# uncover the tile and set the status 0-8 else flagtheTile
			# When would it return a value that isn't 0-8?
		if (number >= 0 and number <= 8):
			self.uncoverTile(number)
		else:
			self.flagTile()

		# are we done? #CoveredTiles = #Mines ->LEAVES
		if (self.__coveredTiles == self.__totalMines):
			self.flagBombs()
			while (self.__numFlaged < self.__totalMines):
				action = AI.Action(2) #flag
				lastAction = Action(action, self.__bomblist[0][0], self.__bomblist[0][1])
				self.__bomblist.pop(0)
				self.__numFlaged += 1
				print("len of bomblist inside loop:", self.__bomblist)
				return lastAction
			return Action(AI.Action.LEAVE)

		#simple rule of thumb logic UNCOVER X,Y
		if (number == 0):
			self.uncoverAdjTiles()
		else:
			self.checkNumUnMarked(self.__currX, self.__currY, number)
			self.checkAdjTiles(self.__currX, self.__currY)

		print("Len of self.__toUncover after: ", len(self.__toUncover))		# DELETE AFTER
		
		if (len(self.__toUncover) > 0):
			action = AI.Action(1) #uncover
			self.__lastAction = Action(action, self.__toUncover[0][0], self.__toUncover[0][1])
			print("Move to make: ", self.__toUncover[0][0], self.__toUncover[0][1])	# DELETE AFTER
			self.__toUncover.pop(0)
			return self.__lastAction
		else:
			# IF no certain moves left, randomly pick and uncovered tile not adjacent to any edges(techncially higher prob of being safe than adj tiles)
			print("RAN OUT OF MOVES SO NOW RANDOM")
			found = 0
			tried_moves = []
			while (found == 0):
				rand_x = random.randint(0, self.__rowDimension-1)
				rand_y = random.randint(0, self.__colDimension-1)
				print("coord", rand_x, rand_y)
				if (self.__board[rand_x][rand_y] == -1 and (rand_x, rand_y) not in self.__bomblist):	
					# Check if number of non-adj empty tiles is 0
					print("checking random tile")
					counter = 0
					if (rand_x-1 >= 0):
						if (rand_y-1 >= 0 and self.__board[rand_x-1][rand_y-1] != -1):
							print(1)
							self.checkNumUnMarked(rand_x-1, rand_y-1, self.__board[rand_x-1][rand_y-1])
							counter += 1
						if (rand_y+1 < len(self.__board[rand_x]) and self.__board[rand_x-1][rand_y+1] != -1):
							print(2)
							self.checkNumUnMarked(rand_x-1, rand_y+1, self.__board[rand_x-1][rand_y+1])
							counter += 1
						if (self.__board[rand_x-1][rand_y] != -1):
							counter += 1
							self.checkNumUnMarked(rand_x-1, rand_y, self.__board[rand_x-1][rand_y])
							print(3)

					if (rand_x+1 < len(self.__board)):
						if (rand_y-1 >= 0 and self.__board[rand_x+1][rand_y-1] != -1):
							counter += 1
							self.checkNumUnMarked(rand_x+1, rand_y-1, self.__board[rand_x+1][rand_y-1])
							print(4)
						if (rand_y+1 < len(self.__board[rand_x]) and self.__board[rand_x+1][rand_y+1] != -1):
							counter += 1
							self.checkNumUnMarked(rand_x+1, rand_y+1, self.__board[rand_x+1][rand_y+1])
							print(5)
						if (self.__board[rand_x+1][rand_y] != -1):
							counter += 1
							self.checkNumUnMarked(rand_x+1, rand_y, self.__board[rand_x+1][rand_y])
							print(6)

					if (rand_y-1 >= 0 and 0 < self.__board[rand_x][rand_y-1] != -1):
						counter += 1
						self.checkNumUnMarked(rand_x, rand_y-1, self.__board[rand_x][rand_y-1])
						print(7)

					if (rand_y+1 < len(self.__board[rand_x]) and self.__board[rand_x][rand_y+1] != -1):
						counter += 1
						self.checkNumUnMarked(rand_x, rand_y+1, self.__board[rand_x][rand_y+1])
						print(8)
					# Change to not be adjacent to an uncovered edge
					
					tried_moves.append((rand_x, rand_y))
					
					print("counter count", counter)
					#for thing in self.__Uncovered:
						#print(thing)
					if (counter == 0):
						print("loop should quit")
						found = 1
					else:
						if (len(tried_moves) == self.__coveredTiles - len(self.__bomblist)):
							# pick random move from list of tried moves
							print("HIT LOGICAL GUESS")
							rand_x = tried_moves[0][0]
							rand_y = tried_moves[0][1]
							found = 1



			action = AI.Action(1) #uncover
			self.__lastAction = Action(action, rand_x, rand_y)
			self.__currX = rand_x
			self.__currY = rand_y
			print("Move to make (random): ", rand_x, rand_y) 	# DELETE AFTER
			return self.__lastAction

		#IF not found use another logic
		

		#If not found again guess use approximation


		return Action(AI.Action.LEAVE)
		########################################################################
		#							YOUR CODE ENDS							   #
		########################################################################

	# loop through all adjacent tiles and check how many are unmarked
	# if it equals to num meaning all unmarked tiles are bomb marked them (10)? whateve represent bomb
	def checkNumUnMarked(self, x, y, num: int):
		numUnmrked = []

		# Check all adjacent tiles:

		# Check tiles in row below if applicable
		if (x > 0):
			# Check bottom left
			if (y > 0):
				if (self.__board[x - 1][y - 1] == -1 or self.__board[x - 1][y - 1] == 10):
					numUnmrked.append((x-1, y-1))
			# Check bottom right
			if (y < self.__colDimension - 1):
				if (self.__board[x - 1][y + 1] == -1 or self.__board[x - 1][y + 1] == 10):
					numUnmrked.append((x-1, y+1))
			# Check bottom mid
			if (self.__board[x - 1][y] == -1 or self.__board[x - 1][y] == 10) :
				numUnmrked.append((x-1, y))
		
		# Check mid left
		if (y > 0):
			if (self.__board[x][y - 1] == -1 or self.__board[x][y - 1] == 10):
				numUnmrked.append((x, y-1))
		# Check mid right
		if (y < self.__colDimension - 1):
			if (self.__board[x][y + 1] == -1 or self.__board[x][y + 1] == 10):
				numUnmrked.append((x, y+1))

		# Check tiles in row above if applicable
		if (x < self.__rowDimension - 1):
			# Check top left
			if (y > 0):
				if (self.__board[x + 1][y - 1] == -1 or self.__board[x + 1][y - 1] == 10):
					numUnmrked.append((x+1, y-1))
			# Check top right
			if (y < self.__colDimension - 1):
				if (self.__board[x + 1][y + 1] == -1 or self.__board[x + 1][y + 1] == 10):
					numUnmrked.append((x+1, y+1))
			# Checkk top mid
			if (self.__board[x + 1][y] == -1 or self.__board[x + 1][y] == 10):
				numUnmrked.append((x+1, y))
		
		if (len(numUnmrked) == num):
			for i in numUnmrked:
				self.__board[i[0]][i[1]] = 10
				if ((i[0], i[1]) not in self.__bomblist):
					self.__bomblist.append((i[0], i[1]))
				self.checkUpdatedBomb(i[0], i[1])


	def checkUpdatedBomb(self, x, y):
		# When a bomb is flagged, check each adjacent tile if the new info reveals safe tiles
		uncoveredAdjacent = []
		
		# Add uncovered adjacent tiles
		# Check top row
		if (x > 0):
			# Check top left
			if (y > 0):
				if self.__board[x - 1][y - 1] > 0:
					uncoveredAdjacent.append((x - 1, y - 1))
			# Check top right
			if (y < self.__colDimension - 1):
				if self.__board[x - 1][y + 1] > 0:
					uncoveredAdjacent.append((x - 1, y + 1))
			# Check top mid
			if self.__board[x - 1][y] > 0:
				uncoveredAdjacent.append((x - 1, y))
		# Check mid left
		if (y > 0):
			if self.__board[x][y - 1] > 0:
				uncoveredAdjacent.append((x, y - 1))
		# Chcek mid right
		if (y < self.__colDimension - 1):
			if self.__board[x][y - 1] > 0:
				uncoveredAdjacent.append((x, y + 1))
		# Check bottom row
		if (x < self.__rowDimension - 1):
			if (y > 0):
				if self.__board[x - 1][y - 1] > 0:
					uncoveredAdjacent.append((x + 1, y - 1))
			# Check bottom right
			if (y < self.__colDimension - 1):
				if self.__board[x + 1][y + 1] > 0:
					uncoveredAdjacent.append((x + 1, y + 1))
			# Check bottom mid
			if self.__board[x + 1][y] > 0:
				uncoveredAdjacent.append((x + 1, y))

		# For each uncovered adjacent tile, check if num is equal to adjacent bombs and reveal all adjacent uncovered tiles
		for tile in uncoveredAdjacent:
			# Count num of adjacent bombs
			numBombs = 0
			# Check top row
			if (tile[0] > 0):
				# Check top left
				if (tile[1] > 0):
					if self.__board[tile[0] - 1][tile[1] - 1] == 10:
						numBombs += 1
				# Check top right
				if (tile[1] < self.__colDimension - 1):
					if self.__board[tile[0] - 1][tile[1] + 1] == 10:
						numBombs += 1
				# Check top mid
				if self.__board[tile[0] - 1][tile[1]] == 10:
					numBombs += 1
			# Check mid left
			if (tile[1] > 0):
				if self.__board[tile[0]][tile[1] - 1] == 10:
					numBombs += 1
			# Chcek mid right
			if (tile[1] < self.__colDimension - 1):
				if self.__board[tile[0]][tile[1] + 1] == 10:
					numBombs += 1
			# Check bottom row
			if (tile[0] < self.__rowDimension - 1):
				if (tile[1] > 0):
					if self.__board[tile[0] + 1][tile[1] - 1] == 10:
						numBombs += 1
				# Check bottom right
				if (tile[1] < self.__colDimension - 1):
					if self.__board[tile[0] + 1][tile[1] + 1] == 10:
						numBombs += 1
				# Check bottom mid
				if self.__board[tile[0] + 1][tile[1]] == 10:
					numBombs += 1

			# Add covered tiles to be revealed if num bombs equal
			if numBombs == self.__board[tile[0]][tile[1]]:
				if (tile[0] > 0):
					# Check top left
					if (tile[1] > 0):
						if self.__board[tile[0] - 1][tile[1] - 1] == -1 and (tile[0] - 1, tile[1] - 1) not in self.__toUncover:
							self.__toUncover.append((tile[0] - 1, tile[1] - 1))
					# Check top right
					if (tile[1] < self.__colDimension - 1):
						if self.__board[tile[0] - 1][tile[1] + 1] == -1 and (tile[0] - 1, tile[1] + 1) not in self.__toUncover:
							self.__toUncover.append((tile[0] - 1, tile[1] + 1))
					# Check top mid
					if self.__board[tile[0] - 1][tile[1]] == -1 and (tile[0] - 1, tile[1]) not in self.__toUncover:
						self.__toUncover.append((tile[0] - 1, tile[1]))
				# Check mid left
				if (tile[1] > 0):
					if self.__board[tile[0]][tile[1] - 1] == -1 and (tile[0], tile[1] - 1) not in self.__toUncover:
						self.__toUncover.append((tile[0], tile[1] - 1))
				# Chcek mid right
				if (tile[1] < self.__colDimension - 1):
					if self.__board[tile[0]][tile[1] + 1] == -1 and (tile[0], tile[1] + 1) not in self.__toUncover:
						self.__toUncover.append((tile[0], tile[1] + 1))
				# Check bottom row
				if (tile[0] < self.__rowDimension - 1):
					if (tile[1] > 0):
						if self.__board[tile[0] + 1][tile[1] - 1] == -1 and (tile[0] + 1, tile[1] - 1) not in self.__toUncover:
							self.__toUncover.append((tile[0] + 1, tile[1] - 1))
					# Check bottom right
					if (tile[1] < self.__colDimension - 1):
						if self.__board[tile[0] + 1][tile[1] + 1] == -1 and (tile[0] + 1, tile[1] + 1) not in self.__toUncover:
							self.__toUncover.append((tile[0] + 1, tile[1] + 1))
					# Check bottom mid
					if self.__board[tile[0] + 1][tile[1]] == -1 and (tile[0] + 1, tile[1]) not in self.__toUncover:
						self.__toUncover.append((tile[0] + 1, tile[1]))



	def uncoverAdjTiles(self):
		x = self.__currX
		y = self.__currY
		
		# check all 8 adjacent tiles if they are alre ady uncovered; if not add them to toUncover list
		
		# little messy if u can double check that ll be nice
			# changed insert of append to maintain order of tiles being checked
		if (x-1 >= 0):
			if (y-1 >= 0 and ((x-1, y-1) not in self.__Uncovered)) and ((x-1, y-1) not in self.__toUncover):
				self.__toUncover.append((x-1, y-1))
			if (y+1 < len(self.__board[x]) and ((x-1, y+1) not in self.__Uncovered)) and ((x-1, y+1) not in self.__toUncover):
				self.__toUncover.append((x-1, y+1))
			if ((x-1, y) not in self.__Uncovered) and ((x-1, y) not in self.__toUncover):
				self.__toUncover.append((x-1, y))

		if (x+1 < len(self.__board)):
			if (y-1 >= 0 and ((x+1,y-1) not in self.__Uncovered)) and ((x+1,y-1) not in self.__toUncover):
				self.__toUncover.append((x+1,y-1))
			if (y+1 < len(self.__board[x]) and ((x+1,y+1) not in self.__Uncovered) and ((x+1,y+1) not in self.__toUncover)):
				self.__toUncover.append((x+1,y+1))
			if ((x+1,y) not in self.__Uncovered and (x+1,y) not in self.__toUncover):
				self.__toUncover.append((x+1,y))

		if (y-1 >= 0 and ((x,y-1) not in self.__Uncovered)) and ((x,y-1) not in self.__toUncover):
			self.__toUncover.append((x,y-1))

		if (y+1 < len(self.__board[x]) and ((x,y+1) not in self.__Uncovered) and ((x,y+1) not in self.__toUncover)):
			self.__toUncover.append((x,y+1))

			
	def checkAdjTiles(self, x, y):
		# check adjacent tiles and see there's number then call checkNumunMrked()
		if (x-1 >= 0):
			if (y-1 >= 0 and 0 < self.__board[x-1][y-1] <= 8):
				self.checkNumUnMarked(x-1, y-1, self.__board[x-1][y-1])
			if (y+1 < len(self.__board[x]) and 0 < self.__board[x-1][y+1] <= 8):
				self.checkNumUnMarked(x-1, y+1, self.__board[x-1][y+1])
			if (0 < self.__board[x-1][y] <= 8):
				self.checkNumUnMarked(x-1, y, self.__board[x-1][y])

		if (x+1 < len(self.__board)):
			if (y-1 >= 0 and 0 < self.__board[x+1][y-1] <= 8):
				self.checkNumUnMarked(x+1, y-1, self.__board[x+1][y-1])
			if (y+1 < len(self.__board[x]) and 0 < self.__board[x+1][y+1] <= 8):
				self.checkNumUnMarked(x+1, y+1, self.__board[x+1][y+1])
			if (0 < self.__board[x+1][y] <= 8):
				self.checkNumUnMarked(x+1, y, self.__board[x+1][y])

		if (y-1 >= 0 and 0 < self.__board[x][y-1] <= 8):
			self.checkNumUnMarked(x, y-1, self.__board[x][y-1])

		if (y+1 < len(self.__board[x]) and 0 < self.__board[x][y+1] <= 8):
			self.checkNumUnMarked(x, y+1, self.__board[x][y+1])

	def uncoverTile(self, num: int):
		#if ((self.__currX, self.__currY) in self.__toUncover):
		if ((self.__currX, self.__currY) not in self.__Uncovered):
			self.__board[self.__currX][self.__currY] = num
			self.__Uncovered.append((self.__currX, self.__currY))
			self.__coveredTiles -= 1
			#self.__toUncover.pop(0)

	# use 9 as flag for now
	def flagTile(self):
		self.__board[self.__currX][self.__currY] = 10
		# TODO: After marking a bomb, check surrounding tiles if updated info changes anything

	def create_board(self):
		for i in range(self.__rowDimension):
			row = []
			for j in range(self.__colDimension):
				# set to ??? -1 for now cause Idk what else to put
				row.append(-1)
			self.__board.append(row)

		
	def flagBombs(self):
		for i in range(self.__rowDimension):
			for j in range(self.__colDimension):
				if (self.__board[i][j] == -1 or self.__board[i][j] == 9 or self.__board[i][j] == 10):
					if ((i,j) not in self.__bomblist):
						self.__bomblist.append((i,j))
					
	
	def printBoard(self):
		for i in range(self.__rowDimension):
			for j in range(self.__colDimension):
				print(self.__board[j][self.__rowDimension - i - 1], " ", end="")
			print("\n")


# NOTES:
	# Bombs not being properly set, possibly switching positions with safe tiles
		# Need to check how bombs are being marked (possibly fixed)
	# I think redundant bombs being added to bomblist
		# Need to check when bombs are being found (set to 10) and also when being added to bomblist



	# Make fuction to set remaining tiles to all bombs if number of covered = num bombs

