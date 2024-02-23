import tkinter as tk
from tkinter import *
from minesweeper import MineSweeper
from functools import partial

FONT = ("Courier", 14, "normal")
EASY_SIDE = 6
EASY_MINES = 5
MEDIUM_SIDE = 12
MEDIUM_MINES = 10
HARD_SIDE = 20
HARD_MINES = 15

class MineSweeperGUI:

    def __init__(self, window):
        self.window = window

        self.game = MineSweeper()

        self.load_images()


        self.display_board = []

        self.number_of_mines = 0
        self.side = 0

        self.moves_left = 0


        # last thing to do
        self.intro_menu()

    def intro_menu(self):
        self.intro_label = Label(text="Welcome to Mine Sweeper", font=FONT)
        self.intro_label.grid(column=1, row=0, padx=30, pady=50)

        self.easy_button = Button(text="Easy", font=FONT, command=lambda: self.choose_difficulty("easy"))
        self.easy_button.grid(column=0, row=1, padx=50)

        self.medium_button = Button(text="Medium", font=FONT, command=self.medium_setup)
        self.medium_button.grid(column=1, row=1, )

        self.hard_button = Button(text="Hard", font=FONT, command=self.hard_setup)
        self.hard_button.grid(column=2, row=1, padx=50)

        self.easy_label = Label(text=f"{EASY_SIDE} x {EASY_SIDE}\n{EASY_MINES} mines", font=FONT)
        self.easy_label.grid(column=0, row=2, pady=50)

        self.medium_label = Label(text=f"{MEDIUM_SIDE} x {MEDIUM_SIDE}\n{MEDIUM_MINES} mines", font=FONT)
        self.medium_label.grid(column=1, row=2, pady=50)

        self.hard_label = Label(text=f"{HARD_SIDE} x {HARD_SIDE}\n{HARD_MINES} mines", font=FONT)
        self.hard_label.grid(column=2, row=2, pady=50)

    def remove_intro_menu(self):
        self.intro_label.grid_forget()
        self.easy_button.grid_forget()
        self.medium_button.grid_forget()
        self.hard_button.grid_forget()
        self.easy_label.grid_forget()
        self.medium_label.grid_forget()
        self.hard_label.grid_forget()

    def easy_setup(self):
        self.remove_intro_menu()
        self.window.minsize(height=150, width=150)
        self.build_button_board(self.side, self.number_of_mines)

        for r in range(self.side):
            for c in range(self.side):
                self.real_board[r][c].config(command=partial(self.click_square, r, c))
                self.real_board[r][c].grid(column=c, row=r)





    def medium_setup(self):
        pass

    def hard_setup(self):
        pass

    def choose_difficulty(self, difficulty):
        if difficulty == "easy":
            self.game.set_difficulty("easy")
            self.side = self.game.get_side()
            self.number_of_mines = self.game.get_num_mines()
            self.moves_left = (self.side * self.side) - self.number_of_mines
            self.easy_setup()
        elif difficulty == "medium":
            self.medium_setup()
        elif difficulty == "hard":
            self.hard_setup()

    def click_square(self, row, col):
        print("click")
        if self.game.is_mine(row, col):
            self.real_board[row][col].config(image=self.mine_img)
            print("mine hit game over")
            self.game_over()
        else:
            if self.game.check_move_available(row, col):
                self.moves_left -= 1
                minecount = self.game.count_adjacent_mines(row, col)
                self.real_board[row][col].config(image=self.images_list[minecount])
                self.real_board[row][col].config(command=0)
                self.game.board[row][col] = minecount

                if self.moves_left == 0:
                    self.game_won()

                if minecount == 0:
                    # NORTH (row - 1, col)
                    if self.game.is_valid_move(row - 1, col):
                        if self.game.check_move_available(row - 1, col):
                            if not self.game.is_mine(row - 1, col):
                                self.click_square(row - 1, col)
                    # SOUTH (row + 1, col)
                    if self.game.is_valid_move(row + 1, col):
                        if self.game.check_move_available(row + 1, col):
                            if not self.game.is_mine(row + 1, col):
                                self.click_square(row + 1, col)
                    # EAST (row, col + 1)
                    if self.game.is_valid_move(row, col + 1):
                        if self.game.check_move_available(row, col + 1):
                            if not self.game.is_mine(row, col + 1):
                                self.click_square(row, col + 1)
                    # WEST (row, col - 1)
                    if self.game.is_valid_move(row, col - 1):
                        if self.game.check_move_available(row, col - 1):
                            if not self.game.is_mine(row, col - 1):
                                self.click_square(row, col - 1)
                    # NORTH EAST (row - 1, col + 1)
                    if self.game.is_valid_move(row - 1, col + 1):
                        if self.game.check_move_available(row - 1, col + 1):
                            if not self.game.is_mine(row - 1, col + 1):
                                self.click_square(row - 1, col + 1)
                    # NORTH WEST (row - 1, col - 1)
                    if self.game.is_valid_move(row - 1, col - 1):
                        if self.game.check_move_available(row - 1, col - 1):
                            if not self.game.is_mine(row - 1, col - 1):
                                self.click_square(row - 1, col - 1)
                    # SOUTH EAST (row + 1, col + 1)
                    if self.game.is_valid_move(row + 1, col + 1):
                        if self.game.check_move_available(row + 1, col + 1):
                            if not self.game.is_mine(row + 1, col + 1):
                                self.click_square(row + 1, col + 1)
                    # SOUTH WEST (row + 1, col - 1)
                    if self.game.is_valid_move(row + 1, col - 1):
                        if self.game.check_move_available(row + 1, col - 1):
                            if not self.game.is_mine(row + 1, col - 1):
                                self.click_square(row + 1, col - 1)

    def game_over(self):
        print("put some sort of game over on screen")
        print("for now game cannot reset")
        print("utimately a reset where you go back to main menu")
        for r in range(self.side):
            for c in range(self.side):
                self.real_board[r][c].config(command=0)

        self.over_label = Label(text="GAME OVER", font=FONT)
        grid_loc = int((self.side / 2) - 1)
        self.over_label.grid(columnspan=4, row=grid_loc, column=grid_loc-1)

    def game_won(self):
        print("game is over because player won")
        print("have something pop up about winning")
        print("ultimate able to reset")
        for r in range(self.side):
            for c in range(self.side):
                self.real_board[r][c].config(command=0)

        self.over_label = Label(text="YOU WIN", font=FONT)
        grid_loc = int((self.side / 2) - 1)
        self.over_label.grid(columnspan=4, row=grid_loc, column=grid_loc - 1)

    def build_button_board(self, side, mines):
        self.real_board = []
        for r in range(side):
            temp_list = []
            for c in range(side):
                temp_button = Button(image=self.square_img, highlightthickness=0)
                temp_list.append(temp_button)
            self.real_board.append(temp_list)

    def load_images(self):
        self.square_img = PhotoImage(file="./images/RaisedSquarePNG.png")
        self.mine_img = PhotoImage(file="./images/MinePNG.png")
        self.zero_img = PhotoImage(file="./images/GreySquarePNG.png")
        self.one_img = PhotoImage(file="./images/OneMinePNG.png")
        self.two_img = PhotoImage(file="./images/TwoMinesPNG.png")
        self.three_img = PhotoImage(file="./images/ThreeMinesPNG.png")
        self.four_img = PhotoImage(file="./images/FourMinesPNG.png")
        self.five_img = PhotoImage(file="./images/FiveMinesPNG.png")

        self.images_list = []
        self.images_list.append(self.zero_img)
        self.images_list.append(self.one_img)
        self.images_list.append(self.two_img)
        self.images_list.append(self.three_img)
        self.images_list.append(self.four_img)
        self.images_list.append(self.five_img)