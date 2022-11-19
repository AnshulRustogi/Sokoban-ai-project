class Node:
    def __init__(self, puzzle, parent, depth):
        self.puzzle = puzzle
        self.parent = parent
        self.depth = depth
        '''
        self.heuristic = heuristic
        self.fn_value = self.depth + self.heuristic'''