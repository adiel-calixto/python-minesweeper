import tkinter as tk
import random

vis = []


class MineSweeper(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.size = 9
        self.num_mines = 10
        self.over = False
        self.blocks = []
        self.flags = []

        self.title("MineSweeper")
        self.geometry("320x400+100+100")
        self.resizable(False, False)

        self.columnconfigure(tuple(range(self.size)), weight=1)
        self.rowconfigure(tuple(range(self.size + 1)), weight=1)

        self.game_button = tk.Button(self, text="Reset", command=self.reset)
        self.game_button.grid(column=1, row=0, sticky=tk.NSEW, columnspan=2)

        self.remaining_flags = tk.Label(self, text=self.num_mines)
        self.remaining_flags.grid(column=0, row=0, sticky=tk.NSEW)

        self.set_values()
        self.draw_blocks()

    def set_values(self):
        self.values = [[0 for _ in range(self.size)] for _ in range(self.size)]

        self.place_mines()
        self.set_numbers()

    def reset(self):
        global vis
        vis = []

        self.over = False
        self.flags = []
        self.set_values()
        self.update_text()

        for col in self.blocks:
            for btn in col:
                btn["text"] = ""

    def draw_blocks(self):
        for i in range(self.size):
            self.blocks.append([])
            for j in range(self.size):
                self.blocks[i].append(tk.Button(self))

                self.blocks[i][j].bind(
                    "<Button-3>",
                    lambda event, row=i, col=j: self.right_clicked_btn(
                        event, row, col),
                )

                self.blocks[i][j].bind(
                    "<Button-1>",
                    lambda event, row=i, col=j: self.left_clicked_btn(
                        event, row, col),
                )

                self.blocks[i][j].grid(column=j, row=i + 1, sticky=tk.NSEW)

    def open_block_neighbours(self, row, col, distance=0):
        global vis

        if ([row, col] in vis) or distance > 1:
            return

        if self.values[row][col] == -1 or ([row, col] in self.flags):
            return

        vis.append([row, col])

        self.blocks[row][col]["text"] = self.values[row][col]
        self.blocks[row][col]["state"] = "disabled"

        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                # Prevent out of index error
                if r < 0 or c < 0 or r >= self.size or c >= self.size:
                    continue

                if r == row and c == col:
                    continue

                d = distance + 1 if self.values[r][c] != 0 else 0

                self.open_block_neighbours(r, c, d)

    def update_text(self):
        empty_blocks = 0

        for col in self.blocks:
            for btn in col:
                if btn["text"] == "":
                    empty_blocks += 1

        if empty_blocks == 0 and len(self.flags) == self.num_mines and not self.over:
            self.over = True
            self.game_button["text"] = "Won"
        elif self.over:
            self.game_button["text"] = "Lost"
        else:
            self.game_button["text"] = "Reset"

        self.remaining_flags.configure(text=self.num_mines - len(self.flags))

    def left_clicked_btn(self, event, row, col):
        if event.widget["text"] != "" or self.over:
            return

        if self.values[row][col] == -1:
            self.over = True
            self.update_text()
            event.widget.configure(text="B", state="disabled")
            return

        event.widget["text"] = self.values[row][col]
        event.widget["state"] = "disabled"

        self.open_block_neighbours(row, col)
        self.update_text()

    def right_clicked_btn(self, event, row, col):
        if self.over:
            return

        if event.widget["text"] != "" and event.widget["text"] != "F":
            return

        if [row, col] in self.flags:
            self.flags.remove([row, col])

            event.widget.configure(text="")
            event.widget["state"] = "active"
        else:
            if len(self.flags) < self.num_mines:
                self.flags.append([row, col])

                event.widget.configure(text="F")
                event.widget["state"] = "disabled"

        self.update_text()

    def place_mines(self):
        count = 0

        while count < self.num_mines:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            if self.values[row][col] != -1:
                self.values[row][col] = -1
                count += 1

    def set_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                mines_around = 0

                if self.values[i][j] == -1:
                    continue

                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        # Prevent out of index error
                        if r < 0 or c < 0 or r >= self.size or c >= self.size:
                            continue

                        if r == i and c == j:
                            continue

                        if self.values[r][c] == -1:
                            mines_around += 1

                self.values[i][j] = mines_around


if __name__ == "__main__":
    game = MineSweeper()
    game.mainloop()
