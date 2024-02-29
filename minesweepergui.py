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

        self.images_list = []
        self.load_images()
        self.make_end_display()

        self.display_board = []

        self.difficulty = "none"
        self.number_of_mines = 0
        self.side = 0

        self.moves_left = 0

        self.mines_list = []


        # last thing to do
        self.intro_menu()

    def intro_menu(self):
        self.intro_label = Label(text="Welcome to Mine Sweeper", font=FONT)
        self.intro_label.grid(column=1, row=0, padx=30, pady=50)

        self.easy_button = Button(text="Easy", font=FONT, command=lambda: self.choose_difficulty("easy"))
        self.easy_button.grid(column=0, row=1, padx=50)

        self.medium_button = Button(text="Medium", font=FONT, command=lambda: self.choose_difficulty("medium"))
        self.medium_button.grid(column=1, row=1, )

        self.hard_button = Button(text="Hard", font=FONT, command=lambda: self.choose_difficulty("hard"))
        self.hard_button.grid(column=2, row=1, padx=50)

        self.easy_label = Label(text=f"{EASY_SIDE} x {EASY_SIDE}\n{EASY_MINES} mines", font=FONT)
        self.easy_label.grid(column=0, row=2, pady=50)

        self.medium_label = Label(text=f"{MEDIUM_SIDE} x {MEDIUM_SIDE}\n{MEDIUM_MINES} mines", font=FONT)
        self.medium_label.grid(column=1, row=2, pady=50)

        self.hard_label = Label(text=f"{HARD_SIDE} x {HARD_SIDE}\n{HARD_MINES} mines", font=FONT)
        self.hard_label.grid(column=2, row=2, pady=50)

    def refresh_intro_menu(self):
        self.window.minsize(width=500, height=300)
        self.intro_label.grid(column=1, row=0, padx=30, pady=50)
        self.easy_button.grid(column=0, row=1, padx=50)
        self.medium_button.grid(column=1, row=1, )
        self.hard_button.grid(column=2, row=1, padx=50)
        self.easy_label.grid(column=0, row=2, pady=50)
        self.medium_label.grid(column=1, row=2, pady=50)
        self.hard_label.grid(column=2, row=2, pady=50)

    def remove_intro_menu(self):
        self.intro_label.grid_forget()
        self.easy_button.grid_forget()
        self.medium_button.grid_forget()
        self.hard_button.grid_forget()
        self.easy_label.grid_forget()
        self.medium_label.grid_forget()
        self.hard_label.grid_forget()

    def setup(self):
        self.remove_intro_menu()
        height = self.side * 25
        width = self.side * 25
        self.window.minsize(height=height, width=width)
        self.build_button_board(self.side, self.number_of_mines)

    def choose_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.game.set_difficulty(self.difficulty)
        self.side = self.game.get_side()
        self.number_of_mines = self.game.get_num_mines()
        self.mines_list = self.game.get_mines_locations()
        self.moves_left = (self.side * self.side) - self.number_of_mines
        self.setup()


    def click_square(self, row, col):
        if self.game.is_mine(row, col):
            self.real_board[row][col].config(image=self.mine_img)
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
        for r in range(self.side):
            for c in range(self.side):
                self.real_board[r][c].config(command=0)

        self.reveal_mines()

        self.over_label = Label(text="GAME OVER", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        grid_loc = int((self.side / 2) - 1)
        self.over_label.grid(columnspan=5, rowspan=2,  row=grid_loc, column=grid_loc-1)

        r_grid_loc = int(self.side/2) +1
        self.restart_button.grid(columnspan=5, rowspan=2, row=r_grid_loc, column=grid_loc-1)
    def game_won(self):
        for r in range(self.side):
            for c in range(self.side):
                self.real_board[r][c].config(command=0)

        self.over_label = Label(text="YOU WIN", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        grid_loc = int((self.side / 2) - 1)
        self.over_label.grid(columnspan=4, row=grid_loc, column=grid_loc - 1)

        r_grid_loc = int(self.side / 2) + 1
        self.restart_button.grid(columnspan=5, rowspan=2, row=r_grid_loc, column=grid_loc - 1)

    def restart(self):
        self.remove_end_display()
        self.empty_button_board()
        self.game.restart()
        self.refresh_intro_menu()


    def make_end_display(self):
        pass

    def remove_end_display(self):
        self.over_label.grid_forget()
        self.restart_button.grid_forget()

    def build_button_board(self, side, mines):
        self.real_board = []
        for r in range(side):
            temp_list = []
            for c in range(side):
                temp_button = Button(image=self.square_img, highlightthickness=0, borderwidth=0)
                temp_list.append(temp_button)
            self.real_board.append(temp_list)

        for r in range(self.side):
            for c in range(self.side):
                # setting up args passed
                self.real_board[r][c].config(command=partial(self.click_square, r, c))
                self.real_board[r][c].grid(column=c, row=r)
                # bind right click for flagging
                self.real_board[r][c].bind("<Button-2>", self.flag_a_mine)
                self.real_board[r][c].bind("<Button-3>", self.flag_a_mine)

    def empty_button_board(self):
        for row in range(self.side):
            for col in range(self.side):
                self.real_board[row][col].destroy()
        self.real_board = []

    def make_top_display(self):
        self.top_display = Canvas(width=(self.side * 25), height=50, highlightthickness=0, )

        self.mines_display = self.top_display.create_text(30, 25, text=f"M {self.number_of_mines}")

        self.smile_display = self.top_display.create_image(70, 20, image=self.smile_img)

        self.top_display.grid(columnspan=self.side, column=0, row=self.side)
    def flag_a_mine(self, event):
        # event.widget access what was right clicked
        if event.widget.cget("image") == str(self.square_img):
            event.widget.configure(image=self.flag_img)
        elif event.widget.cget("image") == str(self.flag_img):
            event.widget.configure(image=self.square_img)

    def reveal_mines(self):
        for tuple in self.mines_list:
            self.real_board[tuple[0]][tuple[1]].config(image=self.mine_img)

    def load_images(self):
        self.load_filenames()

        self.flag_img = PhotoImage(file="./images/FlagPNG.png")
        self.square_img = PhotoImage(file="./images/RaisedSquarePNG.png")
        self.mine_img = PhotoImage(file="./images/MinePNG.png")

        self.smile_img = PhotoImage(file="./images/SmileDisplayPNG.png")

        filepath = "./images/"

        for filename in self.mine_filename_list:
            fullfilename = filepath + filename
            temp_img = PhotoImage(file=fullfilename)
            self.images_list.append(temp_img)


    def load_filenames(self):
        with open(file="./notes/minefilenames.txt", mode="r") as file:
            self.mine_filename_list = file.read().splitlines()