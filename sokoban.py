from puzzle import Puzzle
import numpy as np
from pandas import DataFrame
from IPython.display import display
import sys
import copy 


#sys.tracebacklimit = 0
class Sokoban(Puzzle):

    def __init__(self,
            state=None,
            test_name="Game",
            test_file="sokoban.xsb"
            ):
        if state is None:
            self.test_name = test_name
            self.test_file = test_file

            if self.does_file_exist():
                self.read_file()
        else:
            self.generate_board_from_state(state, test_name)

    def generate_board_from_state(self, state, test_name: str):
        self.test_name = test_name
        gameWidth = len(state[0])
        return self.generate_board(gameWidth, state, from_state=False)

    def does_file_exist(self):
        try:
            self.file = open(self.test_file, "r")
            #print("File exists: %s" % self.test_file)
            return True
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist")

    def read_file(self):
        gameWidth = -1
        game_raw = []

        for line in self.file:
            game_raw.append(line)
            gameWidth = max(gameWidth, len(line))
        #("File read successfully")
        self.generate_board(gameWidth, game_raw)
    
    #Generate board from file data
    def generate_board(self, gameWidth: int, game_raw: list, from_state=True) -> None:
        '''
        Labels:
        0 = empty space
        1 = wall
        2 = box
        3 = goal
        4 = box on goal
        5 = player
        6 = player on goal
        '''

        '''
        The standard pictorial text file representation is called the xsb format.
        A single character represents the different entities and their state.

        '' (white space) - Floor
        @ - Player
        + - Player on goal
        # - Wall
        $ - Stone/Crate/Box
        . - Goal
        * - Stone/Box/Crate on Goal
        The semicolon ';' is used as a comment character before the puzzle itself starts. 
        If is used to give the name of the instance etc. The instance itself is flanked by a blank line at the beginning and one after the instance ends. 
        '''

        #Variable initialization
        '''
        Variables used
        gameHeight - height of the game board
        gameWidth - width of the game board
        game - the game board
        player - the player's position
        boxes - the boxes' positions
        goals - the goals' positions
        '''
        self.gameHeight = len(game_raw[1:] if from_state else game_raw)
        if from_state:
            self.test_name = ''.join(list(game_raw[0])[2:-1])
        self.gameWidth = gameWidth 
        self.game = [[0 for x in range(self.gameWidth)] for y in range(self.gameHeight)]
        self.boxes = set()
        self.goal = set()
        self.player = (-1, -1)

        #Generate board from file and find player, boxes and goals
        for row, line in enumerate(game_raw[1:] if from_state else game_raw):
            for col, char in enumerate(line):
                if char == ' ' or char == 0:
                    self.game[row][col] = 0
                elif char == '#' or char == 1:
                    self.game[row][col] = 1
                elif char == '$' or char == 2:
                    self.game[row][col] = 2
                    self.boxes.add((row, col))
                elif char == '.' or char == 3:
                    self.game[row][col] = 3
                    self.goal.add((row, col))
                elif char == '*' or char == 4:
                    self.game[row][col] = 4
                    self.boxes.add((row, col))
                    self.goal.add((row, col))
                elif char == '@' or char == 5:
                    self.game[row][col] = 5
                    self.player = (row, col)
                elif char == '+' or char == 6:
                    self.game[row][col] = 6
                    self.player = (row, col)
                elif char == '\n':
                    break
                else:
                    raise ValueError("Invalid character %s" % char)
        #print("Board generated successfully")
        return True

    #Make the move
    def move(self, direction: str, update_self=False):
        '''
        Moves the player in the given direction
        Possible directions are:
        u: up
        d: down
        l: left
        r: right
        '''
        '''
        Labels:
        0 = empty space
        1 = wall
        2 = box
        3 = goal
        4 = box on goal
        5 = player
        6 = player on goal
        '''
        #Check if the direction is valid
        if direction not in ['u', 'd', 'l', 'r']:
            raise ValueError("Invalid direction: %s" % direction)

        #Check if the player is on the board
        if self.player == (-1, -1):
            raise ValueError("Player not on board")

        #Check if box is moved
        box_moved = False

        #Change
        delta = {
            'u': (-1, 0),
            'd': (1, 0),
            'l': (0, -1),
            'r': (0, 1) 
        }
        newGame = copy.deepcopy(self.game)
        
        #Make the move
        newPos = (self.player[0] + delta[direction][0], self.player[1] + delta[direction][1])
        if newGame[newPos[0]][newPos[1]] in [0, 3]:
            newGame[self.player[0]][self.player[1]] = 0
            newGame[newPos[0]][newPos[1]] = 5
            #If the player is on a goal
            if newPos in self.goal:
                newGame[newPos[0]][newPos[1]] = 6
            #If the player was on a goal
            if self.player in self.goal:
                newGame[self.player[0]][self.player[1]] = 3
            
            if update_self:
                self.player = newPos

        #Check if the new position is a wall
        if newGame[newPos[0]][newPos[1]] == 1:
            valid_move = False
            return False

        #Check if the new position is a box or if the box is on a goal
        if newGame[newPos[0]][newPos[1]] in [2, 4]:
            newPositionDash = (newPos[0] + delta[direction][0], newPos[1] + delta[direction][1])
            #Check if the box is below a wall or another box or below a box on a goal
            if newGame[newPositionDash[0]][newPositionDash[1]] in [1, 2, 4]:
                valid_move = False
                return False
            #If the box is not below a wall or another box, move the box and update the game board
            else:
                box_moved = True
                #Set current position to empty space
                newGame[self.player[0]][self.player[1]] = 0
                #Set new position to player
                newGame[newPos[0]][newPos[1]] = 5
                #If the player is on a goal
                if self.player in self.goal:
                    newGame[newPos[0]][newPos[1]] = 6
                if self.player in self.goal:
                    newGame[self.player[0]][self.player[1]] = 3
                
                if update_self:
                    self.player = newPos
                newPositionDash = (newPos[0] + delta[direction][0], newPos[1] + delta[direction][1])
                
                #Set the box's new position to a box
                newGame[newPositionDash[0]][newPositionDash[1]] = 2
                if update_self:
                    self.boxes.add(newPositionDash)
                    self.boxes.remove(newPos)
                #Check if the new position of the box is a goal
                if newPositionDash in self.goal:
                    newGame[newPositionDash[0]][newPositionDash[1]] = 4
        
        return Sokoban(
            state=newGame,
            test_name=self.test_name
        ), direction.upper() if box_moved else direction.lower()

    def is_solved(self):
        '''
        Checks if the game is solved i.e. all boxes are on goals
        '''
        return self.boxes == self.goal

    def print_board(self) -> None:
        '''
        Prints the board
        '''
        tempData = DataFrame(self.game).replace(0, ' ').replace(1, '#').replace(2, '$').replace(3, '.').replace(4, '*').replace(5, '@').replace(6, '+')
        #display(tempData)
        print(tempData)
        return

    def __str__(self) -> str:
        '''
        Returns the board as a string
        '''
        #Convert the board (dtype: list of list) to string
        st = '; %s\n' % self.test_name
        for row in self.game:
            for col in row:
                st += str(col)
            st += '\n'
        return st
    
    def succesors(self) -> list or None:
        '''
        Returns a list of all possible moves
        '''
        child = []
        for direction in ['u', 'd', 'l', 'r']:
            if self.move(direction):
                #yield self.move(direction)
                child.append(self.move(direction))
        return child      

    #Check for all possible deadend in the board
    def deadend(self) -> bool:
        '''
        Checks if the board is a deadend
        Deadend1: A box is in a ditch and is not on a goal
        Deadend2: A box is in a corner and is not on a goal
        
        '''
        #Check if a box is in a ditch that is it's adjacent to walls in three directions 
        for box in self.boxes:
            l, r, u, d = 0, 0, 0, 0
            l = self.game[box[0]][box[1]-1]
            r = self.game[box[0]][box[1]+1]
            u = self.game[box[0]-1][box[1]]
            d = self.game[box[0]+1][box[1]]

            #Deadend 1: Box is in a ditch
            #Check if any 3 of the 4 directions are walls
            if (l == 1 and r == 1 and u == 1) or (l == 1 and r == 1 and d == 1) or (l == 1 and u == 1 and d == 1) or (r == 1 and u == 1 and d == 1):
                #Check if the box is not on a goal
                if box not in self.goal:
                    return True
            
            #Deadend 2: Box is in a corner
            #Check if any 2 of the 4 directions are walls
            if (l == 1 and u == 1) or (l == 1 and d == 1) or (r == 1 and u == 1) or (r == 1 and d == 1):
                #Check if the box is not on a goal
                if box not in self.goal:
                    return True
            '''
            For one side wall, we can check if there are any walls in a two block wide line, or if the goal is
            If not then this too
            '''   
        return False


    @staticmethod
    def get_box_coords(state):
        return [(i, j) for i in range(len(state)) for j in range(len(state)) if state[i][j] in [2, 4]]

    @staticmethod
    def get_player_coords(state: str):
        return [(i, j) for i in range(len(state)) for j in range(len(state)) if state[i][j] in [5, 6]][0]

    @staticmethod
    def get_goal_coords(state):
        return [(i, j) for i in range(len(state)) for j in range(len(state[0])) if state[i][j] in [3, 4]]

if __name__=="__main__":
    game = Sokoban(test_file="game.xsb")
    #Make a while loop that runs until game is over and checks if the game is over using game.check_game_over()
    #Puts the game into the string which can be used to load the game again
    #temp = game.__str__()
    
    #gameTemp = Sokoban(state=temp)
    game.print_board()
    #Play the game
    while not game.is_solved():
        #Get the move from the user
        move = input("Enter the move: ")
        #Check if the move is valid
        
        if game.move(move):
            game, _ = game.move(move)
            #If the move is valid, print the board
            game.print_board()
            print("Boxes: ", game.boxes)
            print("Player: ", game.player)
            print("Is deadend: ", game.deadend())
        else:
            #If the move is not valid, print the board and ask for another move
            print("Invalid move")
            game.print_board()

                    

                
            