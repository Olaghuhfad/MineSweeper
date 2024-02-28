import random

EASY_SIDE = 6
EASY_MINES = 6
MEDIUM_SIDE = 12
MEDIUM_MINES = 24
HARD_SIDE = 20
HARD_MINES = 66
class MineSweeper:

    def __init__(self):
        self.board = []

        self.mines_list = []

    def restart(self):
        self.board = []
        self.mines_list = []


    def make_board(self, side):
        for r in range(side):
            temp_list = []
            for c in range(side):
                temp_list.append(" ")
            self.board.append(temp_list)

    def place_mines(self, side, num):
        for i in range(num):
            ran_row = random.randint(0, side-1)
            ran_col = random.randint(0, side-1)
            while self.board[ran_row][ran_col] == "*":
                ran_row = random.randint(0, side - 1)
                ran_col = random.randint(0, side - 1)
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
        if (row >= 0) and (row < self.side) and (col >= 0) and (col < self.side):
            return True
        else:
            return False

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.side = EASY_SIDE
            self.num_mines = EASY_MINES
            self.make_board(self.side)
            self.place_mines(self.side, self.num_mines)
            self.moves_left = self.side * self.side
        elif difficulty == "medium":
            self.side = MEDIUM_SIDE
            self.num_mines = MEDIUM_MINES
            self.make_board(self.side)
            self.place_mines(self.side, self.num_mines)
            self.moves_left = self.side * self.side
        elif difficulty == "hard":
            self.side = HARD_SIDE
            self.num_mines = HARD_MINES
            self.make_board(self.side)
            self.place_mines(self.side, self.num_mines)
            self.moves_left = self.side * self.side

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
    def get_side(self):
        return self.side

    def get_num_mines(self):
        return self.num_mines

    def get_mines_locations(self):
        return self.mines_list