import math
from sokoban import Sokoban
from node import Node
import sys
from state import State
import numpy as np
import scipy.optimize
import heapq
import threading
import multiprocessing
from multiprocessing import Pool

class Search():
	BFS = 1
	DFS = 2
	DLS = 3
	IDS = 4
	AStar = 5

def appendNewNode(
	nodes :list[Node],
	newNode :Node,
	searchType,
	dlsDepth=0,
	heuristic = (lambda _: 0),
	):
	if searchType == Search.BFS:
		nodes.append(newNode)
	elif searchType == Search.DFS:
		nodes.insert(0, newNode)
	elif searchType == Search.DLS:
		if newNode.depth <= dlsDepth:
			nodes.insert(0, newNode)
		# else:
		# 	nodes.append(newNode)
	elif searchType == Search.IDS:
		if newNode.depth <= dlsDepth:
			nodes.insert(0, newNode)
	elif searchType == Search.AStar:
		#for i in range(len(nodes)):
		#	'''
		#	Uniform Search and A*
		#		'''
		#	if newNode.state.heuristicValue > pow(2, 10):
		#		return
		#	## if (newNode.depth + newNode.state.heuristicValue) < (nodes[i].depth + nodes[i].state.heuristicValue):
		#	#if newNode.state.heuristicValue < nodes[i].state.heuristicValue:
		#	#	nodes.insert(i, newNode)
		#	#	return
		#nodes.append(newNode)
		heapq.heappush(nodes, (newNode.state.heuristicValue, newNode))
		
		# else:
		# 	nodes.append(newNode)

def boxesOutOfPlace(state: State):
	a = np.array(state.box_pos)
	b = np.array(game.goal)
	return np.count_nonzero(a != b)

def euclideanDistance(state: State):
	sum = 0
	for box in state.box_pos:
		min = game.gameHeight * game.gameWidth
		for goal in game.goal:
			dist = ((box[0] - goal[0]) ** 2 + (box[1] - goal[1]) ** 2) ** 0.5
			if dist < min:
				min = dist
		sum += min
	return sum
	
def manhattanDistance(state: State):
	sum = 0
	for box in state.box_pos:
		min = game.gameHeight * game.gameWidth
		for goal in game.goal:
			dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
			if dist < min:
				min = dist
		sum += min
	return sum

#Assign a box to a goal using hungarian algorithm
def pullDistance(state: State):
	#Calculate distances as a weighted undirected bipartite graph D = (VD,ED).
	#Compute distance between each box and each goal
	distance_box_goal = np.zeros((len(state.box_pos), len(game.goal)))
	#Calculate distance between each box and each goal efficiently
	for i, box_position in enumerate(state.box_pos):
		for j in range(len(game.goal)):
			distance_box_goal[i][j] = dist_goal2position[j][box_position[0]][box_position[1]]
	#Assign a box to a goal using hungarian algorithm
	#print(distance_box_goal)
	distance_box_goal[distance_box_goal == np.inf] = 100000000000000000000
	#print(distance_box_goal)
	row_ind, col_ind = scipy.optimize.linear_sum_assignment(distance_box_goal)
	#print(row_ind, col_ind)
	#sys.exit()
	h = sum( [distance_box_goal[i,j] for i,j in zip(row_ind, col_ind)])
	
	#Calculate distance between player and each box
	distance_player_box = np.zeros((len(state.box_pos)))
	for i, box_position in enumerate(state.box_pos):
		distance_player_box[i] = abs(box_position[0] - state.player_pos[0]) + abs(box_position[1] - state.player_pos[1]) - 1

	h += min(distance_player_box)

	return h

#Implement above algorithm
def distanceToGoal():
	#Initialize distanceToGoal
	distanceToGoal = np.zeros((len(game.goal), game.gameHeight, game.gameWidth))
	distanceToGoal.fill(np.inf)
	delta = {
			'u': (-1, 0),
			'd': (1, 0),
			'l': (0, -1),
			'r': (0, 1) 
		}
	#Calculate distance from each goal to all positions
	for (i, goal) in game.goal_dict.items():
		distanceToGoal[i][goal[0]][goal[1]] = 0
		queue = [goal]
		while queue:
			position = queue.pop(0)
			for direction in delta.values():
				boxPosition = (position[0] + direction[0], position[1] + direction[1])
				playerPosition = (position[0] + 2 * direction[0], position[1] + 2 * direction[1])
				if distanceToGoal[i][boxPosition[0]][boxPosition[1]] == np.inf:
					if not game.game[boxPosition[0]][boxPosition[1]]==1 and not game.game[playerPosition[0]][playerPosition[1]]==1:
						distanceToGoal[i][boxPosition[0]][boxPosition[1]] = distanceToGoal[i][position[0]][position[1]] + 1
						queue.append(boxPosition)

	return distanceToGoal


heuristics = [
	lambda _: 0,
	# Boxes out of place
	# lambda state: sum([1 for i in range(game.boxes) if state.boxes[i] in game.goal]),
	lambda state: boxesOutOfPlace(state),
	
	# Euclidean distance
	# lambda state: sum([abs((state.boxes[i] - game.goals[i]) % 3) + abs((state.boxes[i] - game.goals[i]) // 3) for i in range(game.boxes)]),
	lambda state: euclideanDistance(state),
	
	# Manhattan distance
	# lambda state: sum([abs((state.boxes[i] - game.goals[i]) % 3) + abs((state.boxes[i] - game.goals[i]) // 3) for i in range(game.boxes)]),
	lambda state: manhattanDistance(state),

	#Pull distance
	lambda state: pullDistance(state),
]

def solve(state: State, searchType: int, heuristicType: int, dlsDepth: int = 0, printStates: int = 0):
	
	if heuristicType != -1:
		
		for i in range(1, 2 if heuristicType != 6 else 6):
			#print("Heuristic " + str(i))
			if heuristicType == 6:
				# if i == 1:
				# 	continue
				h = heuristics[i]
			else:
				h = heuristics[heuristicType]
			
			# if heuristicType == 5:
			# 	f = lambda Node: Node.depth + 2 * h(Node.state)
			# else:
			# 	f = lambda Node: Node.depth + h(Node.state)
			f = h
				
			openList = []

			closed = []
			state.heuristicValue = h(state)
			#openList.append(Node(state, None, 0))
			heapq.heappush(openList, (state.heuristicValue, Node(state, None, 0)))
			loop(openList, closed, searchType, dlsDepth, f, printStates)
					
	else:
		openList = []
		closed = []
		openList.append(Node(state, None, 0))

		loop(openList, closed, searchType, dlsDepth, f, printStates)

def loop(
	openList :list[Node],
	closed :list[State],
	searchType,
	dlsDepth,
	heuristic = (lambda _: 0),
	printStates = 0,
):
	while openList:
		#current = openList.pop(0)
		current = heapq.heappop(openList)[1]
		closed.append(current.state)
		sys.stdout.write(
			"\r" + str(len(closed)) + " nodes expanded, " 
			+ str(len(openList)) + " nodes in the open, "
			+ str(current.depth) + " moves, "
			+ str(current.state.heuristicValue) + " heuristic value"
			)
		sys.stdout.flush()
		
		# print("Heuristic value: " + str(current.state.heuristicValue))
		# print(current.state.box_pos, game.goal, game.is_solved(current.state))
		# tttt = input()
		# if tttt == "a":
		# 	print(current.state.box_pos, game.goal)
		# elif tttt == "b":
		# 	for node in openList:
		# 		print(node.state.box_pos, node.state.heuristicValue)
					
		if game.is_solved(current.state):
			print("\nSolution found for " + game.name[:-1] + ": " + str(current.depth) + " moves")
			moves_to_solution = []
			while current:
				if printStates:
					game.print_board(current.state)
				moves_to_solution.append(current.state.move_to_reach)
				current = current.parent
			print("Moves to solution: " + str("".join(moves_to_solution[::-1][1:])))
			print("")
			return True
		else:
			for new in game.succesors(current.state):
				if new is not None:
					new.heuristicValue = heuristic(new)
				if new is not None and new not in closed:
					newNode = Node(new, current, current.depth + 1)
					appendNewNode(openList, newNode, searchType, dlsDepth, heuristic)
					
	if searchType == Search.IDS:
		dlsDepth += 1
		if dlsDepth <= 2:
			loop(openList, closed, searchType, dlsDepth)
		else:
			print("No solution found")

def main():
	global game, dist_goal2position

	test_file = "test4.xsb"
	read_file = open(test_file, "r")
	lines = read_file.readlines()
	read_file.close()

	given_games = []
	new_game = []
	for line in lines:
		if line == "\n":
			continue
		if ';' in line:
			given_games.append(new_game)
			new_game = [line]
		else:
			new_game.append(line)
	given_games.append(new_game)
	given_games = given_games[1:]

	print("Search type: \n1. BFS\n2. DFS\n3. DLS\n4. IDS\n5. A*")
	searchType = int(input())
	
	if searchType not in range(1, 6):
		print("Invalid input")
		return
	
	if searchType == Search.DLS:
		dlsDepth = int(input())
		if dlsDepth < 0:
			print("Invalid input")
			return
	else:
		dlsDepth = 1
	
	if searchType == Search.AStar:
		print("Heuristic: \n1. Boxes out of place\n2. Euclidean distance\n3. Manhattan distance\n4. Pull distance")
		heuristicType = int(input("Enter 6 to compare all heuristics: "))
		# heuristicType = 2
		
		if heuristicType not in range(1, 7):
			print("Invalid input")
			return
		
	else:
		f = lambda _: 0
		heuristicType = -1
	printStates = int(input("Print solution states? 1 for yes, 0 for no: "))
	print("Running search type: " + str(searchType) + " with " + str(heuristicType) + " heuristic\n")

	for current_game in given_games:
		gameLen = max(len(line) for line in current_game)
		game = Sokoban(state=current_game, state_width=gameLen)
		print("Test Case: " + game.name[:-1])
		dist_goal2position = distanceToGoal()
		
		state = game.initial_state()
		solve(state, searchType, heuristicType, dlsDepth, printStates)
		
		#print("1. Play")
		#print("2. Solve")
		#print("3. Random")
		#print("4. Exit")
		#choice = int(input())
		# choice = 2
		#if choice == 1:
		#	while True:
		#		temp = game.move(state, input("Please enter a move [u, d, l, r]: "))
		#		if temp is not None:
		#			state = temp
		#			game.print_board(state)
		#			print("Move made: " + state.move_to_reach)
		#			if game.is_solved(state):
		#				print("You win!")
		#				break
			
		#elif choice == 2:
		#	solve(state)
		#elif choice == 3:
		#	state = state.play(10)
		#	state.print_board()
		#elif choice == 3:
		#	return
		#elif choice == 4:
		#	return
		#else:
		#	print("Invalid input")
		#	return

	
if __name__ == '__main__':
	main()
	