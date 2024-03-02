import tkinter as tk
from tkinter import *
from minesweeper import MineSweeper
from functools import partial

FONT = ("Courier", 14, "normal")
DISPLAY_FONT = ("Courier", 16, "normal")
EASY_SIDE = 9
MEDIUM_SIDE = 16
HARD_SIDE = 20

EASY_WIDTH = 9
EASY_HEIGHT = 9
EASY_MINES = 10
MEDIUM_HEIGHT = 16
MEDIUM_WIDTH = 16
MEDIUM_MINES = 40
HARD_HEIGHT = 16
HARD_WIDTH = 30
HARD_MINES = 99

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

        self.height = 0
        self.width = 0

        self.number_of_flags = 0

        self.moves_left = 0

        self.mines_list = []


        # last thing to do
        self.intro_menu()

    def intro_menu(self):
        self.intro_label = Label(text="Welcome to Mine Sweeper", font=FONT)
        self.intro_label.grid(column=1, row=0, padx=30, pady=50)

        self.easy_button = Button(text="Easy", font=FONT, command=partial(self.choose_difficulty, "easy"))
        self.easy_button.grid(column=0, row=1, padx=50)

        self.medium_button = Button(text="Medium", font=FONT, command=partial(self.choose_difficulty, "medium"))
        self.medium_button.grid(column=1, row=1, )

        self.hard_button = Button(text="Hard", font=FONT, command=partial(self.choose_difficulty, "hard"))
        self.hard_button.grid(column=2, row=1, padx=50)

        self.easy_label = Label(text=f"{EASY_WIDTH} x {EASY_HEIGHT}\n{EASY_MINES} mines", font=FONT)
        self.easy_label.grid(column=0, row=2, pady=50)

        self.medium_label = Label(text=f"{MEDIUM_WIDTH} x {MEDIUM_HEIGHT}\n{MEDIUM_MINES} mines", font=FONT)
        self.medium_label.grid(column=1, row=2, pady=50)

        self.hard_label = Label(text=f"{HARD_WIDTH} x {HARD_HEIGHT}\n{HARD_MINES} mines", font=FONT)
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
        height = self.height * 25
        width = self.width * 25
        self.window.minsize(height=height, width=width)
        self.build_display_board()
        self.make_top_display()
        self.refresh_top_display()

    def choose_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.game.set_difficulty(self.difficulty)
        self.height = self.game.get_height()
        self.width = self.game.get_width()
        self.number_of_mines = self.game.get_num_mines()
        self.mines_list = self.game.get_mines_locations()
        self.moves_left = (self.width * self.height) - self.number_of_mines
        self.setup()


    def click_square(self, row, col):
        if self.game.is_mine(row, col):
            self.real_board[row][col].config(image=self.mine_img)
            self.game_over(row, col)
        else:
            if self.game.check_move_available(row, col):
                self.moves_left -= 1
                minecount = self.game.count_adjacent_mines(row, col)
                self.real_board[row][col].config(image=self.images_list[minecount])
                self.real_board[row][col].bind("<Button-1>", '')
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

    def game_over(self, row, col):
        for r in range(self.height):
            for c in range(self.width):
                self.real_board[r][c].bind("<Button-1>", '')

        self.reveal_mines()
        self.real_board[row][col].config(image=self.red_mine_img)

        self.over_label = Label(text="GAME OVER", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        row_loc = int((self.height / 2) - 1)
        col_loc = int((self.width / 2) -2)
        self.over_label.grid(columnspan=5, rowspan=2, row=row_loc, column=col_loc)
        r_row_loc = int((self.height / 2) + 1)

        self.restart_button.grid(columnspan=5, rowspan=2, row=r_row_loc, column=col_loc)
    def game_won(self):
        for r in range(self.height):
            for c in range(self.width):
                self.real_board[r][c].bind("<Button-1>", '')

        self.over_label = Label(text="YOU WIN", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        row_loc = int((self.height / 2) - 1)
        col_loc = int((self.width / 2) - 2)
        self.over_label.grid(columnspan=5, rowspan=2, row=row_loc, column=col_loc)
        r_row_loc = int((self.height / 2) + 1)
        self.restart_button.grid(columnspan=5, rowspan=2, row=r_row_loc, column=col_loc)


    def restart(self):
        self.remove_end_display()
        self.reset_values()
        self.remove_top_display()
        self.empty_button_board()
        self.game.restart()
        self.refresh_intro_menu()

    def reset_values(self):
        self.number_of_mines = 0
        self.number_of_flags = 0

    def make_end_display(self):
        pass

    def remove_end_display(self):
        self.over_label.grid_forget()
        self.restart_button.grid_forget()

    def build_display_board(self):
        self.real_board = []
        for row in range(self.height):
            temp_list = []
            for col in range(self.width):
                temp_label = Label(height=25, width=25, image=self.square_img, borderwidth=0)
                # binding left click
                temp_label.bind("<Button-1>", self.left_click)
                # bind right click flagging
                temp_label.bind("<Button-2>", self.flag_a_mine)
                temp_label.bind("<Button-3>", self.flag_a_mine)
                temp_label.grid(column=col, row=row)
                temp_list.append(temp_label)
            self.real_board.append(temp_list)



    def left_click(self, event):
        for r in range(self.height):
            for c in range(self.width):
                if self.real_board[r][c] == event.widget:
                    row = r
                    col = c
        self.click_square(row, col)

    def empty_button_board(self):
        for row in range(self.height):
            for col in range(self.width):
                self.real_board[row][col].destroy()
        self.real_board = []

    def make_top_display(self):
        self.top_display = Canvas(width=(self.width * 25), height=55, highlightthickness=0, )

        self.mines_display = self.top_display.create_text(40, 25, text=f"M {self.number_of_mines}", font=DISPLAY_FONT)

        self.smile_display = self.top_display.create_image(70, 20, image=self.smile_img)

        self.top_display.grid(columnspan=self.width, column=0, row=self.height)

    def refresh_top_display(self):
        if self.difficulty == "easy":
            mines = self.number_of_mines - self.number_of_flags
            self.top_display.itemconfig(self.mines_display, text=f"M {mines}")
            # self.top_display.coords(self.mines_display, 40, 25)
            self.top_display.coords(self.smile_display, 112, 25)
        elif self.difficulty == "medium":
            mines = self.number_of_mines - self.number_of_flags
            self.top_display.itemconfig(self.mines_display, text=f"M {mines}")
            # self.top_display.coords(self.mines_display, 40, 25)
            self.top_display.coords(self.smile_display, 200, 25)
        else:
            mines = self.number_of_mines - self.number_of_flags
            self.top_display.itemconfig(self.mines_display, text=f"M {mines}")
            self.top_display.coords(self.smile_display, 375, 25)

    def remove_top_display(self):
        self.top_display.grid_forget()

    def flag_a_mine(self, event):
        # event.widget access what was right clicked
        if event.widget.cget("image") == str(self.square_img):
            event.widget.configure(image=self.flag_img)
            self.number_of_flags += 1
            self.refresh_top_display()
        elif event.widget.cget("image") == str(self.flag_img):
            event.widget.configure(image=self.square_img)
            self.number_of_flags -= 1
            self.refresh_top_display()

    def reveal_mines(self):
        for tup in self.mines_list:
            self.real_board[tup[0]][tup[1]].config(image=self.mine_img)

    def load_images(self):
        self.load_filenames()

        self.flag_img = PhotoImage(file="./images/FlagPNG.png")
        self.square_img = PhotoImage(file="./images/RaisedSquarePNG.png")
        self.mine_img = PhotoImage(file="./images/MinePNG.png")
        self.red_mine_img = PhotoImage(file="./images/MineRedPNG.png")

        self.smile_img = PhotoImage(file="./images/SmileDisplay40PNG.png")

        filepath = "./images/"

        for filename in self.mine_filename_list:
            fullfilename = filepath + filename
            temp_img = PhotoImage(file=fullfilename)
            self.images_list.append(temp_img)


    def load_filenames(self):
        with open(file="./notes/minefilenames.txt", mode="r") as file:
            self.mine_filename_list = file.read().splitlines()