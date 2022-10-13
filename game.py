from IPython.display import display
import numpy as np
# import matplotlib.pyplot as plt
from pandas import *
import os
# import time


# class State:

# 	def stateFromFile(self, fileName):
# 		self.fileName = fileName
# 		if self.fileName == None:
# 			raise Exception('File not found\nFile provide a valid file name')
# 		try:
# 			self.file = open(self.fileName, 'r')
# 		except FileNotFoundError as E:
# 			raise Exception('File not found\nFile provide a valid file name', E)
			
# 		self.walls = []
# 		self.player = [0,0]
# 		self.boxes = []
# 		self.boxCount = 0
# 		self.goals = []
# 		fileGame = []
# 		maxWidth = -1
# 		for line in self.file:
# 			if line.find('#') == -1:
# 				continue
# 			fileGame.append(line)
# 			maxWidth = max( maxWidth, len(line))
# 		self.fill_data(fileGame, maxWidth)
		
# 	def fill_data(self, fileGame, maxWidth):
# 		self.walls = np.zeros((len(fileGame), maxWidth))
# 		# self.name = ''.join(list(fileGame[0])[2:-1])
		
# 		for lineIndex, line in enumerate(fileGame):
# 			for charIndex, char in enumerate(line):
# 				if char == '#':
# 					self.walls[lineIndex][charIndex] = 1
# 				elif char == '$':
# 					self.boxes.append([lineIndex, charIndex])
# 					#self.walls[lineIndex][charIndex] = 2
# 					self.boxCount += 1
# 				elif char == '.':
# 					self.goals.append([lineIndex, charIndex])
# 				elif char == '@':
# 					self.player = [lineIndex, charIndex]
# 				elif char == '+':
# 					self.goals.append([lineIndex, charIndex])
# 					self.player = [lineIndex, charIndex]
# 				elif char == '*':
# 					self.boxes.append([lineIndex, charIndex])
# 					self.boxCount += 1
# 					self.goals.append([lineIndex, charIndex])
# 				elif char == ' ' or char == '-':
# 					pass
# 				elif char == '\n':
# 					break
# 				else:
# 					raise Exception('Invalid character in file: ', char)

		
# 		self.walls = self.walls.astype(int)
# 		#self.boxes = np.array(self.boxes)
# 		#self.goals = np.array(self.goals)
# 		#self.player = np.array(self.player)
# 		return
		
# 	def copy(self):
# 		newState = State()
# 		newState.walls = self.walls.copy()
# 		newState.player = self.player.copy()
# 		newState.boxes = self.boxes.copy()
# 		newState.boxCount = self.boxCount
# 		newState.goals = self.goals.copy()
# 		return newState

class Sokoban:
	def __init__(
		self, 
		# name='1', 
		fileName='game.xsb',
		):
		# self.state = State().stateFromFile(fileName)
		# self.name = self.state.name
		
		# self.name = name
		self.fileName = fileName
		if self._checkExistAndOpen():
			raise Exception('File not found\nFile provide a valid file name')
		
		self.create_instance()
	
	def _checkExistAndOpen(self):
		if self.fileName == None:
			print('No file name given')
			return 1
		try:
			self.file = open(self.fileName, 'r')
		except FileNotFoundError as E:
			print('File not found: ', E)
			return 1
		return 0

	def create_instance(self):
		self.walls = []
		self.player = [0,0]
		self.boxes = []
		self.boxCount = 0
		self.goals = []
		fileGame = []
		maxWidth = -1
		for line in self.file:
			if line.find('#') == -1:
				continue
			fileGame.append(line)
			maxWidth = max( maxWidth, len(line))
		self.fill_data(fileGame, maxWidth)
	
	def fill_data(self, fileGame, maxWidth):
		self.walls = np.zeros((len(fileGame), maxWidth))
		# self.name = ''.join(list(fileGame[0])[2:-1])
		
		for lineIndex, line in enumerate(fileGame):
			for charIndex, char in enumerate(line):
				if char == '#':
					self.walls[lineIndex][charIndex] = 1
				elif char == '$':
					self.boxes.append([lineIndex, charIndex])
					#self.walls[lineIndex][charIndex] = 2
					self.boxCount += 1
				elif char == '.':
					self.goals.append([lineIndex, charIndex])
				elif char == '@':
					self.player = [lineIndex, charIndex]
				elif char == '+':
					self.goals.append([lineIndex, charIndex])
					self.player = [lineIndex, charIndex]
				elif char == '*':
					self.boxes.append([lineIndex, charIndex])
					self.boxCount += 1
					self.goals.append([lineIndex, charIndex])
				elif char == ' ' or char == '-':
					pass
				elif char == '\n':
					break
				else:
					raise Exception('Invalid character in file: ', char)

		
		self.walls = self.walls.astype(int)
		#self.boxes = np.array(self.boxes)
		#self.goals = np.array(self.goals)
		#self.player = np.array(self.player)
		return

	def check_game_over(self):
		countInPlace = 0
		for box in self.boxes:
			if box in self.goals:
				countInPlace += 1
		return countInPlace == self.boxCount
	
	def print_visual(self):
		tempData = self.walls.tolist()
		for goalX, goalY in self.goals:
			tempData[goalX][goalY] = "."
		if tempData[self.player[0]][self.player[1]]==".":
			tempData[goalX][goalY] = "*"
		else:
			tempData[self.player[0]][self.player[1]] = "@"
		for boxX, boxY in self.boxes:
			if tempData[boxX][boxY] == ".":
				tempData[boxX][boxY] = "*"
			else:
				tempData[boxX][boxY] = "$"

		tempData = DataFrame(tempData).replace(0, '', regex=True).replace(1, '#', regex=True)
		display(tempData)
		return

	def print_rawData(self):
		print("Walls:")
		print(self.walls)
		print("Boxes:")
		print(self.boxes)
		print("Goals:")
		print(self.goals)
		print("Player:")

	def make_move(self, direction):
		self.validMove=True
		self.boxMoved = False
		if direction == 'u':
			if self.walls[self.player[0]-1][self.player[1]] == 0:
				tempPosition = [self.player[0]-1, self.player[1]]
				for boxIndex, box in enumerate(self.boxes):
					if box == tempPosition:
						if self.walls[box[0]-1][box[1]] == 0:
							for box2 in self.boxes:
								if box2 == [box[0]-1, box[1]]:
									self.validMove = False
									return 1
							self.boxes[boxIndex][0] -= 1
							self.boxMoved = True
							self.player[0] -= 1
							return 0
						self.validMove = False
						return 2
				self.player[0] -= 1  
				return 0
			self.validMove = False
			return -1
		elif direction == 'd':
			if self.walls[self.player[0]+1][self.player[1]] == 0:
				tempPosition = [self.player[0]+1, self.player[1]]
				for boxIndex, box in enumerate(self.boxes):
					if box == tempPosition:
						if self.walls[box[0]+1][box[1]] == 0:
							for box2 in self.boxes:
								if box2 == [box[0]+1, box[1]]:
									self.validMove = False
									return 1

							self.boxes[boxIndex][0] += 1
							self.boxMoved = True
							self.player[0] += 1
							return 0
						self.validMove = False
						return 2
				self.player[0] += 1
				return 0
			self.validMove = False
			return -1
		elif direction == 'l':
			if self.walls[self.player[0]][self.player[1]-1] == 0:
				tempPosition = [self.player[0], self.player[1]-1]
				for boxIndex, box in enumerate(self.boxes):
					if box == tempPosition:
						if self.walls[box[0]][box[1]-1] == 0:
							for box2 in self.boxes:
								if box2 == [box[0], box[1]-1]:
									self.validMove = False
									return 1
							self.boxes[boxIndex][1] -= 1
							self.boxMoved = True
							self.player[1] -= 1
							return 0
						self.validMove = False
						return 2
				self.player[1] -= 1
				return 0
			self.validMove = False
			return -1
		elif direction == 'r':
			if self.walls[self.player[0]][self.player[1]+1] == 0:
				tempPosition = [self.player[0], self.player[1]+1]
				for boxIndex, box in enumerate(self.boxes):
					if box == tempPosition:
						if self.walls[box[0]][box[1]+1] == 0:
							for box2 in self.boxes:
								if box2 == [box[0], box[1]+1]:
									self.validMove = False
									return 1
							self.boxes[boxIndex][1] += 1
							self.boxMoved = True
							self.player[1] += 1
							return 0
						self.validMove = False
						return 2
				self.player[1] += 1
				return 0
			self.validMove = False
			return -1
		else:
			# raise Exception('Invalid direction: ', direction)
			print('Invalid direction: ', direction)
		return 0
				
def main():
	#Create instance of class Sokoban
	game = Sokoban()
	#Make a while loop that runs until game is over and checks if the game is over using game.check_game_over(count=False)
	while not game.check_game_over():
		
		# os.system('cls||clear')
		
		#Print the visual representation of the game
		game.print_visual()
		#Get the direction from the user
		print("Enter a direction: ")
		direction = input()
		
		# start time
		# start = time.time()
		#Make the move using game.make_move(direction)
		game.make_move(direction)
		
		# end = time.time()
		# print(f"Runtime of the program is {end - start}")
		
		# print("Move: " + str(game.validMove))
		# print("Box Moved: " + str(game.boxMoved))
		# print("Boxes in place: " + str(game.check_game_over(count=True)))
		
		#Check if the move was valid using game.validMove
		if game.validMove == False:
			print("Invalid move")
		#Check if a box was moved using game.boxMoved
		if game.boxMoved == True:
			print("Box moved")
		#Check if the game is over using game.check_game_over(count=False)
		if game.check_game_over():
			print("Game over")
			print("Game over")
			break
	
if __name__ == "__main__":
	main()
