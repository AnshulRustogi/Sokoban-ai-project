from abc import ABC, abstractmethod
class Puzzle(ABC):
    
    @abstractmethod
    def __init__(self, state, test_name, test_file):
        pass
	
    @abstractmethod
    def move(self, direction):
        pass

    #@abstractmethod
    #def play(self, k):
    #    pass

    @abstractmethod
    def print_board(self):
        pass

    #@abstractmethod
    #def checkSolvable(self):
    #    pass

    @abstractmethod
    def generate_board(self, gameWidth: int, game_raw: list) -> None:
        pass

