from tkinter import Tk, LabelFrame, Label, Button, Menu

root = Tk()
root.title("Connect Four")

menubar = Menu(root)
game_menu = Menu(menubar, tearoff=0)
game_menu.add_command(label="New", command=lambda: print("Hello"))
game_menu.add_cascade(label="Load")
game_menu.add_command(label="Save")
game_menu.add_command(label="Save as...")
game_menu.add_separator()
game_menu.add_command(label="Exit", command=root.quit)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="Game rules")
help_menu.add_command(label="Report an issue")
help_menu.add_command(label="About")

menubar.add_cascade(label="Game", menu=game_menu)
menubar.add_cascade(label="Help", menu=help_menu)

board_frame = LabelFrame(root)

root.config(menu=menubar)
root.mainloop()


