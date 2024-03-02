import random

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
        self.board = []
        self.mines_list = []


    def make_board(self):
        for row in range(self.height):
            temp_list = []
            for col in range(self.width):
                temp_list.append(" ")
            self.board.append(temp_list)


    def place_mines(self):
        for i in range(self.number_of_mines):
            ran_row = random.randint(0, self.height - 1)
            ran_col = random.randint(0, self.width - 1)
            while self.board[ran_row][ran_col] == "*":
                ran_row = random.randint(0, self.height - 1)
                ran_col = random.randint(0, self.width - 1)
            self.board[ran_row][ran_col] = "*"
            self.mines_list.append((ran_row, ran_col))

    def check_move_available(self, row, col):
        if self.board[row][col] == " ":
            return True
        else:
            return False

    def is_mine(self, row, col):
        if self.board[row][col] == "*":
            return True
        else:
            return False

    def is_valid_move(self, row, col):
        if (row >= 0) and (row < self.height) and (col >= 0) and (col < self.width):
            return True
        else:
            return False

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.height = EASY_HEIGHT
            self.width = EASY_WIDTH
            self.number_of_mines = EASY_MINES
            self.make_board()
            self.place_mines()
            self.moves_left = self.width * self.height
        elif difficulty == "medium":
            self.height = MEDIUM_HEIGHT
            self.width = MEDIUM_WIDTH
            self.number_of_mines = MEDIUM_MINES
            self.make_board()
            self.place_mines()
            self.moves_left = self.width * self.height
        elif difficulty == "hard":
            self.height = HARD_HEIGHT
            self.width = HARD_WIDTH
            self.number_of_mines = HARD_MINES
            self.make_board()
            self.place_mines()
            self.moves_left = self.width * self.height

        else:
            print("error")

    def game_over(self):
        pass

    def count_adjacent_mines(self, row, col):
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

    def mine_sweep(self, row, col):
        if self.is_mine(row, col):
            # if you pressed a mine, game over
            self.game_over()

        else:
            count = self.count_adjacent_mines(row, col)
            self.moves_left -= 1
            self.board[row][col] = count

            if count == 0:
                # NORTH (row - 1, col)
                if self.is_valid_move(row - 1, col):
                    if self.check_move_available(row - 1, col):
                        if not self.is_mine(row - 1, col):
                            self.mine_sweep(row - 1, col)
                # SOUTH (row + 1, col)
                if self.is_valid_move(row + 1, col):
                    if self.check_move_available(row + 1, col):
                        if not self.is_mine(row + 1, col):
                            self.mine_sweep(row + 1, col)
                # EAST (row, col + 1)
                if self.is_valid_move(row, col + 1):
                    if self.check_move_available(row, col + 1):
                        if not self.is_mine(row, col + 1):
                            self.mine_sweep(row, col + 1)
                # WEST (row, col - 1)
                if self.is_valid_move(row, col - 1):
                    if self.check_move_available(row, col - 1):
                        if not self.is_mine(row, col - 1):
                            self.mine_sweep(row, col - 1)
                # NORTH EAST (row - 1, col + 1)
                if self.is_valid_move(row - 1, col + 1):
                    if self.check_move_available(row - 1, col + 1):
                        if not self.is_mine(row - 1, col + 1):
                            self.mine_sweep(row - 1, col + 1)
                # NORTH WEST (row - 1, col - 1)
                if self.is_valid_move(row - 1, col - 1):
                    if self.check_move_available(row - 1, col - 1):
                        if not self.is_mine(row - 1, col - 1):
                            self.mine_sweep(row - 1, col - 1)
                # SOUTH EAST (row + 1, col + 1)
                if self.is_valid_move(row + 1, col + 1):
                    if self.check_move_available(row + 1, col + 1):
                        if not self.is_mine(row + 1, col + 1):
                            self.mine_sweep(row + 1, col + 1)
                # SOUTH WEST (row + 1, col - 1)
                if self.is_valid_move(row + 1, col - 1):
                    if self.check_move_available(row + 1, col - 1):
                        if not self.is_mine(row + 1, col - 1):
                            self.mine_sweep(row + 1, col - 1)

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
    def get_num_mines(self):
        return self.number_of_mines

    def get_mines_locations(self):
        return self.mines_list