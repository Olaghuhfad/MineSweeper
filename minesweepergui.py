import tkinter as tk
from tkinter import *
from minesweeper import MineSweeper
from functools import partial

FONT = ("Courier", 14, "normal")
DISPLAY_FONT = ("Courier", 16, "normal")
NUMBERS_FONT = ("Alarm Clock", 25, "normal")


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

        self.number_images_list = []
        self.load_images()

        self.real_board = []

        self.difficulty = "none"
        self.number_of_mines = 0

        self.height = 0
        self.width = 0

        self.number_of_flags = 0

        self.moves_left = 0

        self.timer_number = 0

        self.mines_list = []
        self.flags_list = []

        self.timer_on = False
        self.first_click = True

        # last thing to do
        self.make_custom_menu()

        self.intro_menu()
        self.grid_intro_menu()

    def intro_menu(self):
        '''creates the intro menu/main menu'''
        self.intro_label = Label(text="Welcome to Mine Sweeper", font=FONT)
        self.easy_button = Button(text="Easy", font=FONT, command=partial(self.setup, EASY_WIDTH, EASY_HEIGHT, EASY_MINES))
        self.medium_button = Button(text="Medium", font=FONT, command=partial(self.setup, MEDIUM_WIDTH, MEDIUM_HEIGHT, MEDIUM_MINES))
        self.hard_button = Button(text="Hard", font=FONT, command=partial(self.setup, HARD_WIDTH, HARD_HEIGHT, HARD_MINES))
        self.easy_label = Label(text=f"{EASY_WIDTH} x {EASY_HEIGHT}\n{EASY_MINES} mines", font=FONT)
        self.medium_label = Label(text=f"{MEDIUM_WIDTH} x {MEDIUM_HEIGHT}\n{MEDIUM_MINES} mines", font=FONT)
        self.hard_label = Label(text=f"{HARD_WIDTH} x {HARD_HEIGHT}\n{HARD_MINES} mines", font=FONT)
        self.custom_button = Button(text="Custom", font=FONT, command=self.grid_custom_menu)




    def grid_intro_menu(self):
        '''puts the main menu widgets back in the window using grid'''
        self.intro_label.grid(column=1, row=0, padx=30, pady=50)
        self.easy_button.grid(column=0, row=1, padx=50)
        self.medium_button.grid(column=1, row=1, )
        self.hard_button.grid(column=2, row=1, padx=50)
        self.easy_label.grid(column=0, row=2, pady=20)
        self.medium_label.grid(column=1, row=2, pady=20)
        self.hard_label.grid(column=2, row=2, pady=20)

        self.custom_button.grid(column=1, row=3, pady=20)



    def remove_intro_menu(self):
        '''removes the intro menu using grid forget. so that when the
        menu is needed again the widgets can just be put on the grid again'''
        self.intro_label.grid_forget()
        self.easy_button.grid_forget()
        self.medium_button.grid_forget()
        self.hard_button.grid_forget()
        self.easy_label.grid_forget()
        self.medium_label.grid_forget()
        self.hard_label.grid_forget()
        self.custom_button.grid_forget()

    def make_custom_menu(self):
        self.width_label = Label(text="Width", font=FONT)
        self.width_box = Entry(width=2, font=FONT)
        self.width_box.insert(0, "30")
        self.height_label = Label(text="Height", font=FONT)
        self.height_box = Entry(width=2, font=FONT)
        self.height_box.insert(0, "16")
        self.mines_label = Label(text="Mines", font=FONT)
        self.mines_box = Entry(width=3, font=FONT)
        self.mines_box.insert(0, "100")
        self.play_button = Button(text="Minesweeper", font=FONT, command=self.make_custom_game)

    def grid_custom_menu(self):
        self.remove_intro_menu()
        self.width_label.grid(column=0, row=0, pady=10, padx=20)
        self.width_box.grid(column=0, row=1, pady=20)
        self.height_label.grid(column=1, row=0, pady=10, padx=20)
        self.height_box.grid(column=1, row=1, pady=20)
        self.mines_label.grid(column=2, row=0, pady=10, padx=20)
        self.mines_box.grid(column=2, row=1, pady=20)
        self.play_button.grid(column=1, row=2, pady=20)

    def remove_custom_menu(self):
        self.width_label.grid_forget()
        self.width_box.grid_forget()
        self.height_label.grid_forget()
        self.height_box.grid_forget()
        self.mines_label.grid_forget()
        self.mines_box.grid_forget()
        self.play_button.grid_forget()

    def make_custom_game(self):
        width = int(self.width_box.get())
        height = int(self.height_box.get())
        mines = int(self.mines_box.get())
        self.setup(width, height, mines)

    def setup(self, width, height, mines):
        '''sets up the game variables and then builds the display board, and top display'''
        self.remove_intro_menu()
        self.remove_custom_menu()
        self.game.setup(width, height, mines)
        self.width = width
        self.height = height
        self.number_of_mines = mines
        self.mines_list = self.game.get_mines_locations()
        self.moves_left = (self.width * self.height) - self.number_of_mines
        self.build_display_board()
        self.make_top_display()
        self.refresh_top_display()



    def click_square(self, row, col):
        '''the main function of minesweeper. if player clicked a mine then it calls game over
        if there are mines near the cell clicked then it changes the square to the number image required
        if there are no mines nearby then it uses recursion to reveal all nearby no mine cells'''
        if self.game.is_mine(row, col):
            self.real_board[row][col].config(image=self.mine_img)
            self.game_over(row, col)
        else:
            if self.game.check_move_available(row, col):
                self.moves_left -= 1
                minecount = self.game.count_adjacent_mines(row, col)
                self.real_board[row][col].config(image=self.number_images_list[minecount])
                # unbind clicking to stop player from clicking the same square
                self.real_board[row][col].bind("<Button-1>", '')
                self.real_board[row][col].bind("<Button-2>", '')
                self.real_board[row][col].bind("<Button-3>", '')
                self.game.board[row][col] = minecount

                if self.moves_left == 0:
                    self.game_won()

                # if there are no mines nearby then the game fills in the empty areas for the player
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
        '''called when the player loses by pressing a mine. unbinds mouse clicks.
        calls reveal mines. creates a game over label and restart button. stops timer.
        changes the image of the top display smiley'''
        # unbind the labels so player can't click on things after game over
        for r in range(self.height):
            for c in range(self.width):
                self.real_board[r][c].bind("<Button-1>", '')
                self.real_board[r][c].bind("<Button-2>", '')
                self.real_board[r][c].bind("<Button-3>", '')

        self.reveal_mines()
        self.real_board[row][col].config(image=self.red_mine_img)

        self.over_label = Label(text="GAME OVER", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        row_loc = int((self.height / 2) - 1)
        col_loc = int((self.width / 2) -2)

        self.over_label.grid(columnspan=5, rowspan=2, row=row_loc, column=col_loc)
        r_row_loc = int((self.height / 2) + 1)

        self.restart_button.grid(columnspan=5, rowspan=2, row=r_row_loc, column=col_loc)

        self.top_display.itemconfig(self.smile_display, image=self.dead_smile_img)
        self.timer_on = False


    def game_won(self):

        '''called when the player wins. unbind the labels so the player can't click on things
        show the player they won and have a restart button. and stops the timer.
        changes the image of the top display smiley'''
        # unbind labels so the player can't click on things after the game ends
        for r in range(self.height):
            for c in range(self.width):
                self.real_board[r][c].bind("<Button-1>", '')
                self.real_board[r][c].bind("<Button-2>", '')
                self.real_board[r][c].bind("<Button-3>", '')

        # new labels are created here because then they display over the game
        self.over_label = Label(text="YOU WIN", font=FONT)
        self.restart_button = Button(text="RESTART", font=FONT, command=self.restart)

        row_loc = int((self.height / 2) - 1)
        col_loc = int((self.width / 2) - 2)

        self.over_label.grid(columnspan=5, rowspan=2, row=row_loc, column=col_loc)
        r_row_loc = int((self.height / 2) + 1)

        self.restart_button.grid(columnspan=5, rowspan=2, row=r_row_loc, column=col_loc)

        self.top_display.itemconfig(self.smile_display, image=self.sunglasses_smile_img)
        # stop the timer
        self.timer_on = False


    def restart(self):
        '''used to restart the game'''
        self.remove_end_display()
        self.reset_values()
        self.remove_top_display()
        self.empty_button_board()
        self.game.restart()
        self.grid_intro_menu()



    def reset_values(self):
        '''used on restart to reset various variables'''
        self.number_of_mines = 0
        self.number_of_flags = 0
        self.flags_list = []
        self.mines_list = []
        self.timer_number = 0
        self.timer_on = False
        self.first_click = True


    def remove_end_display(self):
        '''destroys the end display on restart'''
        self.over_label.destroy()
        self.restart_button.destroy()


    def build_display_board(self):
        '''creates the display board'''
        self.real_board = []
        for row in range(1, self.height + 1):
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
        '''when player clicks a label, finds which square they pressed
        and runs the main minesweeper function'''
        if self.first_click:
            self.first_click = False
            self.timer_on = True
            self.update_timer()
        for r in range(self.height):
            for c in range(self.width):
                if self.real_board[r][c] == event.widget:
                    row = r
                    col = c
        self.click_square(row, col)


    def empty_button_board(self):
        '''destroys all the widgets so the game can be restarted'''
        for row in range(self.height):
            for col in range(self.width):
                self.real_board[row][col].destroy()
        self.real_board = []


    def make_top_display(self):
        '''creates the top display'''
        display_width = self.width * 25
        self.top_display = Canvas(width=display_width, height=55, highlightthickness=0, )

        self.rectangle = self.top_display.create_rectangle(10, 10, 70, 40, fill="black")
        self.mines_display = self.top_display.create_text(40, 25, text=f"{self.number_of_mines}", font=NUMBERS_FONT, fill="red")

        temp_smile_x = int(display_width / 2)
        self.smile_display = self.top_display.create_image(temp_smile_x, 25, image=self.smile_img)

        temp_rect2_x = (display_width - 70)
        self.rectangle2 = self.top_display.create_rectangle(temp_rect2_x, 10, (temp_rect2_x + 60), 40, fill="black")

        self.timer_display = self.top_display.create_text((display_width - 40), 25, text="001", font=NUMBERS_FONT, fill="red")

        self.top_display.grid(columnspan=self.width, column=0, row=0)


    def refresh_top_display(self):
        '''configures the top display based on what size the game is'''
        mines = self.number_of_mines - self.number_of_flags
        self.top_display.itemconfig(self.timer_display, text=f"{self.timer_number:03d}")
        self.top_display.itemconfig(self.mines_display, text=f"{mines:03d}")



    def remove_top_display(self):
        '''removes the top display with grid forget'''
        self.top_display.grid_forget()

    def update_timer(self):
        '''recursive function running the timer
        game over or winning stops the timer'''
        if self.timer_on:
            self.timer_number += 1
            self.top_display.itemconfig(self.timer_display, text=f"{self.timer_number:03d}")
            self.window.after(1000, self.update_timer)
            # in original if the timer hits 999 the timer stops
            if self.timer_number == 999:
                self.timer_on = False

    def flag_a_mine(self, event):
        '''allows player to flag squares they think are a mine'''
        # find row and col of what was clicked
        for r in range(self.height):
            for c in range(self.width):
                if self.real_board[r][c] == event.widget:
                    row = r
                    col = c
        if event.widget.cget("image") == str(self.square_img):
            event.widget.configure(image=self.flag_img)
            self.number_of_flags += 1
            self.flags_list.append((row, col))
            self.refresh_top_display()
            # unbind left click so player can't click flags by accident
            self.real_board[row][col].bind("<Button-1>", '')
        elif event.widget.cget("image") == str(self.flag_img):
            event.widget.configure(image=self.square_img)
            self.number_of_flags -= 1
            self.flags_list.remove((row, col))
            self.refresh_top_display()
            # rebind left click so square can be clicked again
            self.real_board[row][col].bind("<Button-1>", self.left_click)


    def reveal_mines(self):
        '''when game over needs to reveal mines missed,
        keep correctly flagged mines as flags,
        and display a cross over incorrect flags'''
        # find matches in the list of mines and list of flags to find correctly flagged mines
        correct_mines = set(self.mines_list) & set(self.flags_list)
        # remove mines from list of flags to find incorrect flags
        incorrect_flags = set(self.flags_list) - set(self.mines_list)
        # remove flag list from mine list to find mines that were not flagged
        missed_mines = set(self.mines_list) - set(self.flags_list)

        for tup in correct_mines:
            self.real_board[tup[0]][tup[1]].config(image=self.flag_img)

        for tup in incorrect_flags:
            self.real_board[tup[0]][tup[1]].config(image=self.incorrect_flag_img)

        for tup in missed_mines:
            self.real_board[tup[0]][tup[1]].config(image=self.mine_img)


    def load_images(self):
        '''all images are made here'''
        self.load_filenames()

        self.flag_img = PhotoImage(file="./images/FlagPNG.png")
        self.square_img = PhotoImage(file="./images/RaisedSquarePNG.png")

        self.mine_img = PhotoImage(file="./images/MinePNG.png")
        self.red_mine_img = PhotoImage(file="./images/MineRedPNG.png")

        self.incorrect_flag_img = PhotoImage(file="./images/IncorrectFlagPNG.png")

        self.smile_img = PhotoImage(file="./images/SmileDisplay40PNG.png")
        self.dead_smile_img = PhotoImage(file="./images/DeadSmileDisplay40PNG.png")
        self.sunglasses_smile_img = PhotoImage(file="./images/SmileDisplaySunglassesPNG.png")

        filepath = "./images/"

        # loops through the filename list to create the number images in a list
        for filename in self.mine_filename_list:
            fullfilename = filepath + filename
            temp_img = PhotoImage(file=fullfilename)
            self.number_images_list.append(temp_img)


    def load_filenames(self):
        '''gets names of number images and puts it into a list'''
        with open(file="./notes/minefilenames.txt", mode="r") as file:
            self.mine_filename_list = file.read().splitlines()