import random

# values for difficulty, can change at any time here
EASY_WIDTH = 9
EASY_HEIGHT = 9
EASY_MINES = 10
MEDIUM_HEIGHT = 16
MEDIUM_WIDTH = 16
MEDIUM_MINES = 40
HARD_HEIGHT = 16
HARD_WIDTH = 30
HARD_MINES = 99


class MineSweeper:
    def __init__(self):
        self.board = []
        self.mines_list = []
        self.height = 0
        self.width = 0
        self.number_of_mines = 0


    def restart(self):
        '''resets everything so the game can be restarted'''
        self.board = []
        self.mines_list = []
        self.height = 0
        self.width = 0
        self.number_of_mines = 0

    def make_board(self):
        '''creates a list of lists to keep track of the board'''
        for row in range(self.height):
            temp_list = []
            for col in range(self.width):
                temp_list.append(" ")
            self.board.append(temp_list)


    def place_mines(self):
        '''randomly places the mines
        and adds the location as a tuple in the mine list'''
        for i in range(self.number_of_mines):
            ran_row = random.randint(0, self.height - 1)
            ran_col = random.randint(0, self.width - 1)
            while self.board[ran_row][ran_col] == "*":
                ran_row = random.randint(0, self.height - 1)
                ran_col = random.randint(0, self.width - 1)
            self.board[ran_row][ran_col] = "*"
            self.mines_list.append((ran_row, ran_col))


    def check_move_available(self, row, col):
        '''checks is the move has already been made,
        returns True if move is avaivable and false if already made'''
        if self.board[row][col] == " ":
            return True
        else:
            return False


    def is_mine(self, row, col):
        '''returns true if the grid location has a mine'''
        if self.board[row][col] == "*":
            return True
        else:
            return False


    def is_valid_move(self, row, col):
        '''a function used to stop lists going out of index
        returns True if it's in range, False if it's out of range'''
        if (row >= 0) and (row < self.height) and (col >= 0) and (col < self.width):
            return True
        else:
            return False


    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.height = EASY_HEIGHT
            self.width = EASY_WIDTH
            self.number_of_mines = EASY_MINES
        elif difficulty == "medium":
            self.height = MEDIUM_HEIGHT
            self.width = MEDIUM_WIDTH
            self.number_of_mines = MEDIUM_MINES
        elif difficulty == "hard":
            self.height = HARD_HEIGHT
            self.width = HARD_WIDTH
            self.number_of_mines = HARD_MINES
        self.make_board()
        self.place_mines()

    def setup(self, width, height, mines):
        '''improved function for setting difficulty'''
        self.width = width
        self.height = height
        self.number_of_mines = mines
        self.make_board()
        self.place_mines()


    def count_adjacent_mines(self, row, col):
        '''checks the 8 surrounding squares of cell given
         and returns the total of any mines found'''
        minecount = 0
        # NORTH (row - 1, col)
        if self.is_valid_move(row - 1, col):
            if self.is_mine(row - 1, col):
                minecount += 1
        # SOUTH (row + 1, col)
        if self.is_valid_move(row + 1, col):
            if self.is_mine(row + 1, col):
                minecount += 1
        # EAST (row, col + 1)
        if self.is_valid_move(row, col + 1):
            if self.is_mine(row, col + 1):
                minecount += 1
        # WEST (row, col - 1)
        if self.is_valid_move(row, col - 1):
            if self.is_mine(row, col - 1):
                minecount += 1
        # NORTH EAST (row - 1, col + 1)
        if self.is_valid_move(row - 1, col + 1):
            if self.is_mine(row - 1, col + 1):
                minecount += 1
        # NORTH WEST (row - 1, col - 1)
        if self.is_valid_move(row - 1, col - 1):
            if self.is_mine(row - 1, col - 1):
                minecount += 1
        # SOUTH EAST (row + 1, col + 1)
        if self.is_valid_move(row + 1, col + 1):
            if self.is_mine(row + 1, col + 1):
                minecount += 1
        # SOUTH WEST (row + 1, col - 1)
        if self.is_valid_move(row + 1, col - 1):
            if self.is_mine(row + 1, col - 1):
                minecount += 1
        return minecount


    def get_height(self):
        '''return height of the game board, number of squares'''
        return self.height


    def get_width(self):
        '''return width of the game board, number of squares'''
        return self.width


    def get_num_mines(self):
        '''return the number of mines in the game'''
        return self.number_of_mines


    def get_mines_locations(self):
        '''returns the locations of the mines, list of tuples'''
        return self.mines_list
