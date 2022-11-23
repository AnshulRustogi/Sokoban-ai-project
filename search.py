from sokoban import Sokoban
from node import Node
import sys
from state import State
class Search():
	BFS = 1
	DFS = 2
	DLS = 3
	IDS = 4
	AStar = 5

def appendNewNode(
	nodes, 
	newNode, 
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
			if heuristic(newNode) < heuristic(nodes[i]):
				nodes.insert(i, newNode)
				return
		nodes.append(newNode)
		
		# else:
		# 	nodes.append(newNode)


heuristics = [
	lambda _: 0,
	lambda puzzle: sum([1 for i in range(9) if (puzzle.__str__()[i] != i - 1 or (i == 8 and puzzle.__str__()[i] != 0))]),
	lambda puzzle: sum([((puzzle.__str__()[i] - i) % 3) ** 2 + ((puzzle.__str__()[i] - i) // 3) ** 2 for i in range(9) if puzzle.__str__()[i] != 0]),
	lambda puzzle: sum([abs((puzzle.__str__()[i] - i) % 3) + abs((puzzle.__str__()[i] - i) // 3) for i in range(9) if puzzle.__str__()[i] != 0]),
	lambda puzzle: sum([abs((puzzle.__str__()[i] - i) % 3) + abs((puzzle.__str__()[i] - i) // 3) for i in range(9) if puzzle.__str__()[i] != 0]) + sum([1 for i in range(9) if (puzzle.__str__()[i] != i - 1 or (i == 8 and puzzle.__str__()[i] != 0))]),
	lambda puzzle: sum([((puzzle.__str__()[i] - i) % 3) ** 2 + ((puzzle.__str__()[i] - i) // 3) ** 2 for i in range(9) if puzzle.__str__()[i] != 0]) + sum([1 for i in range(9) if (puzzle.__str__()[i] != i - 1 or (i == 8 and puzzle.__str__()[i] != 0))]),
]

def solve(state: State):
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
		print("Heuristic: \n1. Tiles out of place\n2. Euclindean distance\n3. City block distance\n4. New heuristic\n5. Inadmissible heuristic")
		print("Enter 6 to compare all heuristics")
		heuristicType = int(input())
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
			
			openList = []
			closed = []
			openList.append(Node(state, None, 0))
			
			if heuristicType == 5:
				f = lambda Node: Node.depth + 2 * h(Node.puzzle)
			else:
				f = lambda Node: Node.depth + h(Node.puzzle)
			loop(openList, closed, searchType, dlsDepth, f)
	else:
		openList = []
		closed = []
		openList.append(Node(state, None, 0))

		loop(openList, closed, searchType, dlsDepth, f)


def loop(
	openList,
	closed,
	searchType,
	dlsDepth,
	heuristic = (lambda _: 0),
):
	while openList:
		current = openList.pop(0)
		closed.append(current.puzzle)
		sys.stdout.write(
			"\r" + str(len(closed)) + " nodes expanded, " + str(len(openList)) + " nodes in the open"
			)
		sys.stdout.flush()
		
		if game.is_solved(current.puzzle):
			print("\nSolution found: " + str(current.depth) + " moves")
			while current:
				game.print_board(current.puzzle)
				current = current.parent
			return True
		
		else:
			# i = current.puzzle.__str__().index(0)
			for new in game.succesors(current.puzzle):
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
	game = Sokoban(test_file="test1.xsb")
	state = game.initial_state()
	
	print("1. Play")
	print("2. Solve")
	print("3. Random")
	print("4. Exit")
	choice = int(input())
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
	#	puzzle = puzzle.play(10)
	#	puzzle.print_board()
	elif choice == 3:
		return
	elif choice == 4:
		return
	else:
		print("Invalid input")
		return

	
if __name__ == '__main__':
	main()
