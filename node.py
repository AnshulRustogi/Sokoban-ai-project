from state import State

class Node:
    def __init__(self, state: State, parent, depth, heuristic = -1):
        self.state = state
        self.parent = parent
        self.depth = depth
        # self.heuristic = heuristic
        '''
        self.heuristic = heuristic
        self.fn_value = self.depth + self.heuristic'''

    def __lt__(self, other):
        return self.state.heuristicValue < other.state.heuristicValue

    def __eq__(self, other):
        return self.state == other.state

        