import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
from pathlib import Path
from datetime import datetime

class Game(tk.Frame):
    def __init__(self, frame, rows=5, columns=6, players=['1', '2'], colours={'1': 'yellow', '2': 'green'}, cfg=None):
        tk.Frame.__init__(self, frame)
        self.frame = frame
        self.max_rows = rows
        self.max_columns = columns
        self.min_row = 1
        self.min_col = 0
        self.curr_player = 0
        self.players = players
        self.colours = colours

        self.cfg = cfg
        self.savedir = None
        self._init_config()

    def _init_config(self):
        if self.cfg == None:
            self.cfg = os.getcwd()

        config = { 'savedir': self.savedir }
        try:
            with open(self.cfg + '/.config', 'r') as f:
                config = json.load(f)
        except IOError:
            with open(self.cfg + '/.config', 'w') as f:
                json.dump(config, f)

        self.savedir = config['savedir']

    def _update_player(self):
        self.curr_player = (self.curr_player + 1) % len(self.players)
        self.curr_player_label.destroy()
        self.curr_player_label = tk.Label(self.frame, text="Player " + str(self.players[self.curr_player]), padx=40, pady=10)
        self.curr_player_label.grid(row=0, column=0, columnspan=self.max_columns, sticky="nsew")

    def _update_chain_cells(self, row, column):
        # order: lower column, lower row
        cell = (row, column)
        curr_player = self.players[self.curr_player]
        to_append = [[cell]]
        for item in self.chain_cells[curr_player]:
            r, c = item[0]
            if len(item) == 1:
                if self.is_neighbour(item[0], cell):
                    if column - c == 1:
                        to_append.append(item + [cell])
                    if column - c == -1:
                        to_append.append([cell] + item)
                    if column - c == 0:
                        if row - r > 0:
                            to_append.append([cell] + item)
                        else:
                            to_append.append(item + [cell])

            else:
                if self.is_neighbour(item[0], cell):
                    r1, c1 = item[1]
                    if r1 - r == r - row and c1 - c == c - column:
                        to_append.append([cell] + item)
                re, ce = item[-1]
                if self.is_neighbour(item[-1], cell):
                    re1, ce1 = item[-2]
                    if re - re1 == row - re and ce - ce1 == column - ce:
                        to_append.append(item + [cell])

        self.chain_cells[curr_player] += to_append

    def is_neighbour(self, cell1, cell2):
        r1, c1 = cell1
        r2, c2 = cell2
        if abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1:
            return True
        else:
            return False

    def _create_layout(self):
        self.curr_player_label = tk.Label(self.frame, text="Player " + str(self.players[self.curr_player]), padx=40, pady=10)
        self.curr_player_label.grid(row=0, column=0, columnspan=self.max_columns, sticky="nsew")
        self.cells = {}
        for row in range(self.max_rows):
            tk.Grid.rowconfigure(self.frame, index=0, weight=1)
        for column in range(self.max_columns):
            tk.Grid.columnconfigure(self.frame, index=0, weight=1)
        for row in range(self.max_rows):
            self.cells[row] = {}
            for column in range(self.max_columns):
                if self.state[row][column] == 0:
                    self.cells[row][column] = tk.Button(self.frame, text=" ", padx=30, pady=15, state="disabled", command=self.move(row, column))
                else: 
                    self.cells[row][column] = tk.Button(self.frame, text=self.state[row][column], padx=30, pady=15, state="disabled", background=self.colours[self.state[row][column]])
                self.cells[row][column].grid(row=row + self.min_row, column=column + self.min_col, sticky="nsew")

    def new(self):
        self.state = [[0 for col in range(self.max_columns)] for row in range(self.max_columns)]
        self.chain_cells = {}
        for player in self.players:
            self.chain_cells[player] = []

        self._create_layout()
        row = self.max_rows - 1
        for col in range(self.max_columns):
            self.cells[row][col]["state"] = "active"

    def get_save_files(self):
        if self.savedir == None:
            return []

        return [f for f in os.listdir(self.savedir) if f.endswith('.json')]

    def load(self, filename=None, save_obj=None):
        if save_obj == None and filename == None:
            print("filename or save_obj required")
            return
            # raise Exception, "finename or save_obj required"
        if save_obj == None:
            with open(self.savedir + '/' + filename, 'r') as f:
                save_obj = json.load(f)

        # for key in save_obj:
        #     self[key] == save_obj[key]
        self.players = save_obj['players']
        self.state = save_obj['state']
        self.curr_player = save_obj['curr_player']
        self.max_rows = save_obj['max_rows']
        self.max_columns = save_obj['max_columns']
        self.chain_cells = save_obj['chain_cells']
        self.min_row = save_obj['min_row']
        self.min_col = save_obj['min_col']

        self._create_layout()
        for col in range(self.max_columns):
            row = self.max_rows - 1 
            for temp_row in range(self.max_rows - 1, 0, -1):
                if temp_row == 0:
                    row = temp_row
                    break
            self.cells[row][col]["state"] = "active"

    def save(self):
        if self.savedir == None:
            self.savedir = filedialog.askdirectory(title="Select folder to save game files")
            with open(self.cfg + '/.config', 'w') as f:
                json.dump({ 'savedir': self.savedir }, f)

        save_obj = { 
            'players': self.players,
            'state': self.state,
            'curr_player': self.curr_player,
            'max_rows': self.max_rows,
            'max_columns': self.max_columns,
            'chain_cells': self.chain_cells,
            'min_row': self.min_row,
            'min_col': self.min_col
        }

        Path(self.savedir).mkdir(parents=True, exist_ok=True)
        filename = 'connectFour_' + datetime.now().strftime('%Y_%m_%d_%H_%M') + '.json'
        with open(self.savedir + '/' + filename, 'w', encoding='utf-8') as f:
            json.dump(save_obj, f, ensure_ascii=False, indent=4)

        messagebox.showinfo('ConnectFour:Save', 'Game saved successfully')

    def is_terminal(self):
        return

    def is_winner(self):
        return 4 == max(map(lambda x: len(x), self.chain_cells[self.players[self.curr_player]]))

    def is_draw(self):
        for col in range(self.max_columns):
            if self.state[0][col] == 0:
                return False
        return True

    def _game_over(self):
        for row in range(self.max_rows):
            for column in range(self.max_columns):
                self.cells[row][column]["state"] = "disabled"

    def move(self, row, column):
        def make_move():
            self.state[row][column] = self.players[self.curr_player]
            self.cells[row][column].destroy()
            self.cells[row][column] = tk.Button(self.frame, text=self.state[row][column], padx=30, pady=15, state="disabled", background=self.colours[self.state[row][column]])
            self.cells[row][column].grid(row=row + self.min_row, column=column + self.min_col, sticky="nsew")
            self._update_chain_cells(row, column)
            if self.is_winner():
                messagebox.showinfo('Game has ended', 'Player ' + str(self.players[self.curr_player]) + ' is the winner!')
                return self._game_over()
            self._update_player()
            if self.is_draw():
                messagebox.showinfo('Game has ended', 'Draw!')
                return self._game_over()
            if row != 0:
                self.cells[row - 1][column]["state"] = "active"


        return make_move

class App(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        game_frame = tk.LabelFrame(root)
        game_frame.grid(row=0, column=0, sticky="nsew")
        self.game = Game(game_frame)
        self.game.new()

        self.menubar = self._add_menubar()

        # root.geometry("400x400")
        root.config(menu=self.menubar)

    def _add_menubar(self):
        menubar = tk.Menu(root)
        game_menu = tk.Menu(menubar, tearoff=0)
        self.load_menu = tk.Menu(game_menu, tearoff=0)
        game_menu.add_command(label="New", command=self.new_game)
        game_menu.add_cascade(label="Load", menu=self.load_menu)
        game_menu.add_command(label="Save", command=self.save)
        game_menu.add_command(label="Save as...", command=self.save_as)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Game rules", command=self.show_game_rules)
        help_menu.add_command(label="Report an issue", command=self.redirect_github_issues)
        help_menu.add_command(label="About", command=self.redirect_github)
        self.load_list = []
        self._update_load_list()

        menubar.add_cascade(label="Game", menu=game_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        return menubar
    
    def _update_load_list(self):
        if self.load_list != []:
            self.load_menu.delete(0, len(self.load_list) - 1)
            self.load_list = []

        self.load_list = self.game.get_save_files()
        for filename in self.load_list:
            self.load_menu.add_command(label=filename, command=lambda: self.game.load(filename))

    def new_game(self):
        self.game.new()
        return

    def save(self):
        self.game.save()
        self._update_load_list()

    def save_as(self):
        return

    def show_game_rules(self):
        return

    def redirect_github_issues(self):
        return

    def redirect_github(self):
        return

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Connect Four")
    app = App(root)
    root.mainloop()
