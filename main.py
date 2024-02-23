import tkinter as tk
from tkinter import *
from minesweepergui import MineSweeperGUI

root = Tk()
root.title("Mine Sweeper")
root.minsize(width=500, height=300)

GUI = MineSweeperGUI(root)

root.mainloop()

