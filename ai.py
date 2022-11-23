import enum
from game import Sokoban

class Node:
	def __init__(self, game: Sokoban, parent, depth):
		self.game = game
		self.parent = parent
		self.depth = depth
		
def appendNewNode(
	nodes, 
	newNode, 
	# searchType,
	# dlsDepth = 0
	):
	# if searchType == Search.BFS:
	nodes.append(newNode)
	# elif searchType == Search.DFS:
	# 	nodes.insert(0, newNode)
	# elif searchType == Search.DLS:
	# 	if newNode.depth <= dlsDepth:
	# 		nodes.insert(0, newNode)
	# 	# else:
	# 	# 	nodes.append(newNode)
	# elif searchType == Search.IDS:
	# 	if newNode.depth <= dlsDepth:
	# 		nodes.insert(0, newNode)
	# 	else:
	# 		nodes.append(newNode)

class AI:
	def __init__(self, game):
		self.game = game
		
	def solve(self):
		openNodes = []
		closed = []
		
		openNodes.append(Node(
			self.game
			# {
			# 	'player': self.game.player,
			# 	'boxes': self.game.boxes,
			# }
			, None, 0))
	
		while openNodes:
			current = openNodes.pop(0)
			closed.append(current.game)
			# closed.append({
			# 	'player': current.game.player,
			# 	'boxes': current.game.boxes,
			# })
			
			# sys.stdout.write(
			# 	"\r" + ''.join(map(str, current.game.state)) + 
			# 	" " + str(len(open)) +
			# 	" " + str(len(closed))
			# 	)
			# sys.stdout.flush()
			# current.print_visual()
			
			if current.game.check_game_over():
				print("\nSolution found:")
				print(current.depth, " moves")
				while current:
					current.game.print_visual()
					current = current.parent
				return
			
			else:
				# i = current.game.state.index(0)
				# j in u, d, l, r
				for j in ['u', 'd', 'l', 'r']:
					# new = current.game.move(j)
					new = current.game.copy()
					new.make_move(j)
					if not new.validMove:
						continue
					# if( new is not None 
					# 	and {
					# 		'player': new.player,
					# 		'boxes': new.boxes,
					# 	} not in closed):
					if new is not None and new not in closed:
						newNode = Node(new, current, current.depth + 1)
						appendNewNode(openNodes, newNode)
						# appendNewNode(openNodes, newNode, searchType, dlsDepth)


def main():
	file = open("game.xsb", "r")
	game = Sokoban(file)
	
	ai = AI(game)
	ai.solve()
		

if __name__ == "__main__":
	main()
