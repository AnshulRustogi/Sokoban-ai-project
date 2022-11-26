class State:
    def __init__(self, player_pos: tuple, box_pos: set, move_to_reach: str = None) -> None:
        self.player_pos = player_pos
        self.box_pos = list(box_pos)
        self.box_pos.sort()
        self.box_pos = tuple(self.box_pos)
        self.move_to_reach = move_to_reach
        self.heuristicValue = -1

    def __eq__(self, other: 'State') -> bool:
        return self.player_pos == other.player_pos and self.box_pos == other.box_pos

    def __hash__(self):
        return hash((self.player_pos, frozenset(self.box_pos)))

    def __str__(self):
        return 'player: ' + str(self.player_pos) + ' boxes: ' + str(self.box_pos)
