from sokoban import Sokoban
from node import Node
import sys
from state import State
import numpy as np
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
		for i in range(len(nodes)):
			# if heuristic(newNode) < heuristic(nodes[i]):
			if (newNode.depth + newNode.state.heuristicValue) < (nodes[i].depth + nodes[i].state.heuristicValue):
			# if newNode.state.heuristicValue < nodes[i].state.heuristicValue:
				nodes.insert(i, newNode)
				return
		nodes.append(newNode)
		
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
]

def solve(state: State):
	print("Search type: \n1. BFS\n2. DFS\n3. DLS\n4. IDS\n5. A*")
	searchType = int(input())
	# searchType = 5
	
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
		print("Heuristic: \n1. Boxes out of place\n2. Euclidean distance\n3. Manhattan distance\n")
		print("Enter 6 to compare all heuristics")
		heuristicType = int(input())
		# heuristicType = 2
		
		if heuristicType not in range(1, 7):
			print("Invalid input")
			return
		
	else:
		f = lambda _: 0
		heuristicType = -1
	
	if heuristicType != -1:
		
		for i in range(1, 2 if heuristicType != 6 else 6):
			print("Heuristic " + str(i))
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
			openList.append(Node(state, None, 0))
			
			loop(openList, closed, searchType, dlsDepth, f)
					
	else:
		openList = []
		closed = []
		openList.append(Node(state, None, 0))

		loop(openList, closed, searchType, dlsDepth, f)


def loop(
	openList :list[Node],
	closed :list[State],
	searchType,
	dlsDepth,
	heuristic = (lambda _: 0),
):
	while openList:
		current = openList.pop(0)
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
			print("\nSolution found: " + str(current.depth) + " moves")
			while current:
				game.print_board(current.state)
				current = current.parent
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
		if dlsDepth <= 20:
			loop(openList, closed, searchType, dlsDepth)
		else:
			print("No solution found")

def main():
	global game
	game = Sokoban(test_file="game.xsb")
	
	state = game.initial_state()
	
	print("1. Play")
	print("2. Solve")
	print("3. Random")
	print("4. Exit")
	choice = int(input())
	# choice = 2
	if choice == 1:
		while True:
			temp = game.move(state, input("Please enter a move [u, d, l, r]: "))
			if temp is not None:
				state = temp
				game.print_board(state)
				print("Move made: " + state.move_to_reach)
				if game.is_solved(state):
					print("You win!")
					break
		 
	elif choice == 2:
		solve(state)
	#elif choice == 3:
	#	state = state.play(10)
	#	state.print_board()
	elif choice == 3:
		return
	elif choice == 4:
		return
	else:
		print("Invalid input")
		return

	
if __name__ == '__main__':
	main()
	