from puzzle import Puzzle
import numpy as np
from pandas import DataFrame
from IPython.display import display
import sys
import copy 
from state import State

delta = {
    'u': (-1, 0),
    'd': (1, 0),
    'l': (0, -1),
    'r': (0, 1) 
}
        
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
                    self.number_of_goal += 1
                elif char == '@':
                #    self.game[row][col] = 5
                    player = (row, col)
                elif char == '+':
                #    self.game[row][col] = 6
                    player = (row, col)
                    self.goal.add((row, col))
                    self.number_of_goal += 1
                elif char == '\n':
                    break
                else:
                    raise ValueError("Invalid character %s" % char)
        #print("Board generated successfully")
        self.goal_dict = {i: goal for i, goal in enumerate(self.goal)}
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
        # use a loop
        # for box in state.box_pos:
        #     if box not in self.goal:
        #         return False

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
            temp = self.move(state, direction)
            if temp is not None:
                child.append(temp)

        #Rearrange child depending on whether a box is moved or not
        child = sorted(child, key=lambda x: x.move_to_reach.isupper(), reverse=True)
		
        # movable_pos = []
        # for box in state.box_pos:
        #     for direction in ['u', 'd', 'l', 'r']:
        #         newPos = (box[0] + delta[direction][0], box[1] + delta[direction][1])
        #         oppositePos = (box[0] - delta[direction][0], box[1] - delta[direction][1])
        #         if self.game[newPos[0]][newPos[1]] not in [1, 2, 4] and self.game[oppositePos[0]][oppositePos[1]] not in [1, 2, 4]:
        #             movable_pos.append(newPos)
        
        # open = [state.player_pos]
        # closed = set()
        # while open:
        #     current = open.pop(0)
        #     closed.add(current)
        #     for direction in ['u', 'd', 'l', 'r']:
        #         newPos = (current[0] + delta[direction][0], current[1] + delta[direction][1])
        #         if self.game[newPos[0]][newPos[1]] not in [1, 2, 4] and newPos not in closed:
        #             open.append(newPos)
				
        return child      
        
    # game.flood_fill(state, matrix, [], '', state.player_pos[0], state.player_pos[1])
    def flood_fill(self, state, matrix, path_list, current_path, x, y):
        # matrix = map
        box_pos = state.box_pos
        # stop clause - not reinvoking for when there's floor and a box position and a wall.
        if self.game[x][y] not in [1, 2, 4] and matrix[x][y] == 0:
            matrix[x][y] = 1
            
            # checks future pos is box
            if (x - 1, y) in box_pos:
                if self.game[x - 2][y] != 1 and (x - 2, y) not in box_pos:
                    path_list.append(current_path + 'u')
            if (x + 1, y) in box_pos:
                if self.game[x + 2][y] != 1 and (x + 2, y) not in box_pos:
                    path_list.append(current_path + 'd')
            if (x, y - 1) in box_pos:
                if self.game[x][y - 2] != 1 and (x, y - 2) not in box_pos:
                    path_list.append(current_path + 'l')
            if (x, y + 1) in box_pos:
                if self.game[x][y + 2] != 1 and (x, y + 2) not in box_pos:
                    path_list.append(current_path + 'r')

            # checks each direction if visited, if wall, if box
            if self.game[x - 1][y] != 1 and (x - 1, y) not in box_pos and matrix[x - 1][y] == 0:
                self.flood_fill(state, matrix, path_list, current_path + 'u', x - 1, y)
            if self.game[x + 1][y] != 1 and (x + 1, y) not in box_pos and matrix[x + 1][y] == 0:
                self.flood_fill(state, matrix, path_list, current_path + 'd', x + 1, y)
            if self.game[x][y - 1] != 1 and (x, y - 1) not in box_pos and matrix[x][y - 1] == 0:
                self.flood_fill(state, matrix, path_list, current_path + 'l', x, y - 1)
            if self.game[x][y + 1] != 1 and (x, y + 1) not in box_pos and matrix[x][y + 1] == 0:
                # self.flood_fill(self.game, matrix, path_list, current_path + 'r', x, y + 1)
                self.flood_fill(state, matrix, path_list, current_path + 'r', x, y + 1)

            return path_list

        return path_list
    
    def get_position_from_path(self, player, path):
        for move in path:
            if move == 'u':
                player = (player[0] - 1, player[1])
            elif move == 'd':
                player = (player[0] + 1, player[1])
            elif move == 'l':
                player = (player[0], player[1] - 1)
            elif move == 'r':
                player = (player[0], player[1] + 1)
        return player

    def expand(self, state):
        # if self.dead_end(state):
        #     return []

        matrix = [[0 for _ in range(self.gameWidth)] for _ in range(self.gameHeight)]
        path_list = self.flood_fill(state, matrix, [], '', state.player_pos[0], state.player_pos[1])
        # path_list = self.flood_fill(state, self.map, list(), '', state.data[0][0], state.data[0][1])


        new_states = []
        for path in path_list:
            # Move player
            # new_player = self.get_position_from_path(state.data[0], path)
            new_player = self.get_position_from_path(state.player_pos, path)

            # Move the box
            # box_index = list(state.data[1:]).index(new_player)
            # new_boxes = list(state.data[1:])
            box_index = list(state.box_pos).index(new_player)
            new_boxes = list(state.box_pos)
            if path[-1] == 'u':
                new_boxes[box_index] = (new_boxes[box_index][0] - 1, new_boxes[box_index][1])
            elif path[-1] == 'd':
                new_boxes[box_index] = (new_boxes[box_index][0] + 1, new_boxes[box_index][1])
            elif path[-1] == 'l':
                new_boxes[box_index] = (new_boxes[box_index][0], new_boxes[box_index][1] - 1)
            elif path[-1] == 'r':
                new_boxes[box_index] = (new_boxes[box_index][0], new_boxes[box_index][1] + 1)

            # new_states.append((path, SokobanState(player=new_player, boxes=new_boxes), len(path)))  
            new_states.append(
                State(
                    player_pos=new_player, 
                    box_pos=new_boxes,
                    move_to_reach=path
                )
            )

        return new_states
        
    def getBlockMoves(self, state: State) -> list[State]:
        '''
        Returns a list of all possible block pushes
        '''    
        reachable = [state.player_pos]
        child = []
        # search the map from player position to reachable positions
        while len(reachable) > 0:
            pos = reachable.pop(0)
            for direction in ['u', 'd', 'l', 'r']:
                newPos = (pos[0] + delta[direction][0], pos[1] + delta[direction][1])
                if newPos in state.box_pos:
                    newPositionDash = (newPos[0] + delta[direction][0], newPos[1] + delta[direction][1])
                    if self.game[newPositionDash[0]][newPositionDash[1]]==0 and newPositionDash not in state.box_pos:
                        child.append(self.move(state, direction))
                        reachable.append(newPositionDash)
    
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

            # #Deadend 1: Box is in a ditch
            # #Check if any 3 of the 4 directions are walls or boxes
            # if(((l == 1 or l == 2) and (r == 1 or r == 2) and (u == 1 or u == 2)
            # or (l == 1 or l == 2) and (r == 1 or r == 2) and (d == 1 or d == 2)
            # or (l == 1 or l == 2) and (u == 1 or u == 2) and (d == 1 or d == 2)
            # or (r == 1 or r == 2) and (u == 1 or u == 2) and (d == 1 or d == 2))):
            #     #Check if the box is not on a goal
            #     if box not in self.goal:
            #         return True
            
            #Box is in a corner
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

                    

                
            
