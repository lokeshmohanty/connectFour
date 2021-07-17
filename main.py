import tkinter as tk
from tkinter import messagebox

class Game(tk.Frame):
    def __init__(self, frame, rows=5, columns=6, players=[1, 2]):
        tk.Frame.__init__(self, frame)
        self.frame = frame
        self.max_rows = rows
        self.max_columns = columns
        self.min_row = 1
        self.min_col = 0
        self.curr_player = 0
        self.players = players

        self.state = [[0 for col in range(self.max_columns)] for row in range(self.max_columns)]
        self.chain_cells = {}
        for player in self.players:
            self.chain_cells[player] = []

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
                self.cells[row][column] = tk.Button(self.frame, text=" ", padx=30, pady=15, state="disabled", command=self.move(row, column))
                self.cells[row][column].grid(row=row + self.min_row, column=column + self.min_col, sticky="nsew")

    def new(self):
        self._create_layout()
        row = self.max_rows - 1
        for col in range(self.max_columns):
            self.cells[row][col]["state"] = "active"

    def load(self, state, curr_player):
        return

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
            self.cells[row][column] = tk.Button(self.frame, text=self.state[row][column], padx=30, pady=15, state="disabled", background="gray")
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
        # self.frame = tk.Frame(frame)
        self.menubar = self._add_menubar()

        game_frame = tk.LabelFrame(root)
        game_frame.grid(row=0, column=0, sticky="nsew")
        self.game = Game(game_frame)
        self.game.new()

        # root.geometry("400x400")
        root.config(menu=self.menubar)

    def _add_menubar(self):
        menubar = tk.Menu(root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New", command=self.new_game)
        game_menu.add_cascade(label="Load", state=tk.DISABLED, command=self.load)
        game_menu.add_command(label="Save", command=self.save)
        game_menu.add_command(label="Save as...", command=self.save_as)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Game rules", command=self.show_game_rules)
        help_menu.add_command(label="Report an issue", command=self.redirect_github_issues)
        help_menu.add_command(label="About", command=self.redirect_github)

        menubar.add_cascade(label="Game", menu=game_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        return menubar

    def new_game(self):
        self.game.new()
        return

    def load(self):
        return

    def save(self):
        return

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
