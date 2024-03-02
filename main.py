import tkinter as tk
from minesweepergui import MineSweeperGUI

root = tk.Tk()
root.title("Mine Sweeper")
root.minsize(width=500, height=300)

GUI = MineSweeperGUI(root)

root.mainloop()

