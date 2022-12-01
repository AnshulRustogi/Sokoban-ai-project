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
            state_width=0,
            test_name=None,
            test_file=None
            ):
        if test_file is not None:
            self.test_name = test_name
            self.test_file = test_file
            if self.does_file_exist():
                self.state = self.read_file()
                return
        if state is not None:
            self.state = self.generate_board(state_width, state)
            return

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
            line = line.rstrip()
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
        self.goal_dict = {}
        player = (-1, -1)
        self.number_of_goal = 0
        
        #Generate board from file and find player, boxes and goals
        for row, line in enumerate(game_raw[1:]):
            for col, char in enumerate(line):
                if char == ' ':
                    continue
                if char == '#':
                    self.game[row][col] = 1
                    continue
                if char == '$':
                    boxes.add((row, col))
                elif char == '.':
                    self.goal.add((row, col))
                elif char == '*':
                    boxes.add((row, col))
                    self.goal.add((row, col))
                    self.number_of_goal += 1
                elif char == '@':
                    player = (row, col)
                elif char == '+':
                    player = (row, col)
                    self.goal.add((row, col))
                    self.number_of_goal += 1
                elif char == '\n':
                    break
                else:
                    raise ValueError("Invalid character %s" % char)
        self.goal_dict = {i: goal for i, goal in enumerate(self.goal)}
        return State(player, boxes, None)

    #Make the move
    def move(self, state: State, direction: str):
        '''
        If the move is valid it returns the new state, move else returns None
        
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
            newState.player_pos = newPos
        
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
                newState.player_pos = newPos
                newState.box_pos.add(newPositionDash)
                newState.box_pos.remove(newPos)
        
        newState.move_to_reach = direction.upper() if box_moved else direction.lower()
        return newState

    def is_solved(self, state: State):
        '''
        Checks if the game is solved i.e. all boxes are on goals
        '''
        return state.box_pos == self.goal
        
    def print_board(self,state) -> None:
        '''
        Prints the board using pandas dataframe
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
            temp = self.move(state, direction)
            if temp is not None:
                child.append(temp)

        #Rearrange child depending on whether a box is moved or not
        child = sorted(child, key=lambda x: x.move_to_reach.isupper(), reverse=True)
        return child

    #Check for all possible deadend in the board
    def deadend(self, state: State) -> bool:
        '''
        Checks if the board is a deadend
        - A box is in a corner and is not on a goal
        
        '''
        #Check if a box is in a ditch that is it's adjacent to walls in three directions 
        for box in self.boxes:
            l, r, u, d = 0, 0, 0, 0
            x, y = box
            l = self.game[box[0]][box[1]-1]
            r = self.game[box[0]][box[1]+1]
            u = self.game[box[0]-1][box[1]]
            d = self.game[box[0]+1][box[1]]

            #Box is in a corner
            #Check if any 2 of the 4 directions are walls
            if (l == 1 and u == 1) or (l == 1 and d == 1) or (r == 1 and u == 1) or (r == 1 and d == 1):
                #Check if the box is not on a goal
                if box not in self.goal:
                    return True

        return False

if __name__=="__main__":   
    test_file = "sampleCSD311.xsb"
    read_file = open(test_file, "r")
    lines = read_file.readlines()
    read_file.close()
    game_states = []
    newGame = []
    for line in lines:
        if ';' in line:
            game_states.append(newGame)
            newGame = [line]
        else:
            newGame.append(line)
    game_states.append(newGame)
    game_states = game_states[1:]
    print(game_states)
    print("Number of games: ", len(game_states))
    game_number = int(input("Please enter the game number you want to play: ")) - 1
    gameLen = max(len(line) for line in game_states[game_number])
    game = Sokoban(state=game_states[game_number], state_width=gameLen)
    start_state = game.state
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

                    

                
            
