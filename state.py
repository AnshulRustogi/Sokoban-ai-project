class State:
    def __init__(self, player_pos: tuple, box_pos: set, move_to_reach: chr):
        self.player_pos = player_pos
        self.box_pos = box_pos
        self.move_to_reach = move_to_reach
        self.heuristicValue = -1

    def __eq__(self, other: 'State') -> bool:
        return self.player_pos == other.player_pos and self.box_pos == other.box_pos

    def __hash__(self):
        return hash((self.player_pos, frozenset(self.box_pos)))
