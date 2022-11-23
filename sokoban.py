from puzzle import Puzzle
import numpy as np
from pandas import DataFrame
from IPython.display import display
import sys
import copy 
from state import State

#sys.tracebacklimit = 0
class Sokoban(Puzzle):

    def __init__(self,
            state=None,
            test_name=None,
            test_file=None
            ):
        if test_file is not None:
            self.test_name = test_name
            self.test_file = test_file
            if self.does_file_exist():
                self.state = self.read_file()
                return
    

    '''
    def generate_board_from_state(self, state, test_name: str):
        self.test_name = test_name
        gameWidth = len(state[0])
        return self.generate_board(gameWidth, state, from_state=False)
    '''

    def initial_state(self):
        return self.state

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
        return self.generate_board(gameWidth, game_raw)
    
    #Generate board from file data
    def generate_board(self, gameWidth: int, game_raw: list) -> State:
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
        self.gameHeight = len(game_raw)-1
        self.name = ''.join(list(game_raw[0])[1:])
        self.gameWidth = gameWidth 
        self.game = [[0 for x in range(self.gameWidth)] for y in range(self.gameHeight)]
        boxes = set()
        self.goal = set()
        player = (-1, -1)

        #Generate board from file and find player, boxes and goals
        for row, line in enumerate(game_raw[1:]):
            for col, char in enumerate(line):
                if char == ' ':
                    continue
                #    self.game[row][col] = 0
                if char == '#':
                    self.game[row][col] = 1
                    continue
                if char == '$':
                #    self.game[row][col] = 2
                    boxes.add((row, col))
                elif char == '.':
                    #self.game[row][col] = 3
                    self.goal.add((row, col))
                elif char == '*':
                    #self.game[row][col] = 4
                    boxes.add((row, col))
                    self.goal.add((row, col))
                elif char == '@':
                #    self.game[row][col] = 5
                    player = (row, col)
                elif char == '+':
                #    self.game[row][col] = 6
                    player = (row, col)
                    self.goal.add((row, col))
                elif char == '\n':
                    break
                else:
                    raise ValueError("Invalid character %s" % char)
        #print("Board generated successfully")
        return State(player, boxes, None)

    #Make the move
    def move(self, state: State, direction: str):
        '''
        If the move is valid it returns the new state, move else returns None
        '''

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
        player, boxes = state.player_pos, state.box_pos

        #Check if the player is on the board
        if player == (-1, -1):
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
        newState = copy.deepcopy(state)
        
        #Make the move
        newPos = (player[0] + delta[direction][0], player[1] + delta[direction][1])
        if self.game[newPos[0]][newPos[1]] in [0, 3]:
            #Make current position empty
            #self.game[player[0]][player[1]] = 0
            #Make new position player
            #self.game[newPos[0]][newPos[1]] = 5
            newState.player_pos = newPos
            
            #If the player is on a goal
            #if newPos in self.goal:
            #    self.game[newPos[0]][newPos[1]] = 6
            #If the player was on a goal
            #if player in self.goal:
            #    self.game[player[0]][player[1]] = 3
            
            #if update_self:
            #    player = newPos

        #Check if the new position is a wall
        if self.game[newPos[0]][newPos[1]] == 1:
            return None

        #Check if the new position is a box or if the box is on a goal
        if newPos in boxes:
            newPositionDash = (newPos[0] + delta[direction][0], newPos[1] + delta[direction][1])
            #Check if the box is below a wall or another box or below a box on a goal
            if self.game[newPositionDash[0]][newPositionDash[1]]==1 or (newPositionDash in boxes):
                return None
            #If the box is not below a wall or another box, move the box and update the game board
            else:
                box_moved = True
                #Set current position to empty space
                #self.game[self.player[0]][self.player[1]] = 0
                #Set new position to player
                #self.game[newPos[0]][newPos[1]] = 5
                newState.player_pos = newPos
                #If the player is on a goal
                #if self.player in self.goal:
                #    self.game[newPos[0]][newPos[1]] = 6
                #if self.player in self.goal:
                #    self.game[self.player[0]][self.player[1]] = 3
                
                #if update_self:
                #    self.player = newPos
                
                #Set the box's new position to a box
                #self.game[newPositionDash[0]][newPositionDash[1]] = 2
                #if update_self:
                #    self.boxes.add(newPositionDash)
                #    self.boxes.remove(newPos)
                newState.box_pos.add(newPositionDash)
                newState.box_pos.remove(newPos)


                
                #Check if the new position of the box is a goal
                #if newPositionDash in self.goal:
                #    self.game[newPositionDash[0]][newPositionDash[1]] = 4
        newState.move_to_reach = direction.upper() if box_moved else direction.lower()
        return newState

    def is_solved(self, state: State):
        '''
        Checks if the game is solved i.e. all boxes are on goals
        '''
        return state.box_pos == self.goal

    def print_board(self,state) -> None:
        '''
        Prints the board
        '''

        tempData = DataFrame(self.game).replace(0, ' ').replace(1, '#')
        for goal in self.goal:
            tempData.iloc[goal[0], goal[1]] = '.'

        if state.player_pos in self.goal:
            tempData.loc[state.player_pos] = '+'
        else:
            tempData.loc[state.player_pos[0], state.player_pos[1]] = '@'
        for box in state.box_pos:
            if box in self.goal:
                tempData.loc[box[0], box[1]] = '*'
            else:
                tempData.loc[box[0], box[1]] = '$'

        print(tempData)
        return
 
    def succesors(self, state: State) -> list[State]:
        '''
        Returns a list of all possible moves
        '''
        child = []
        for direction in ['u', 'd', 'l', 'r']:
            if self.move(state, direction):
                #yield self.move(direction)
                child.append(self.move(state, direction))
        return child      

    #Check for all possible deadend in the board
    def deadend(self, state: State) -> bool:
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
        '''
        Returns a list of box coordinates
        '''
        return state.box_pos

    @staticmethod
    def get_player_coords(state: str):
        '''
        Returns the player coordinates
        '''
        return state.player_pos

if __name__=="__main__":
    game = Sokoban(test_file="game.xsb")
    start_state = game.state
    print("Game read from file")
    game.print_board(start_state)
    #Play the game
    current_state = start_state
    while not game.is_solved(current_state):
        #Get the move from the user
        move = input("Enter the move: ")
        #Check if the move is valid
        last_state = current_state
        current_state = game.move(current_state, move)
        if current_state:
            game.print_board(current_state)
            print("Boxes: ", current_state.box_pos)
            print("Player: ", current_state.player_pos)
            print("Move to reach: ", current_state.move_to_reach)
        else:
            print("Invalid move")
            current_state = last_state

                    

                
            