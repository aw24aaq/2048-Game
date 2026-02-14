from tkinter import *
import random

class Game(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.master.title("2048")

        # ---------------- SCORE ----------------
        self.score = 0
        self.score_label = Label(self, text="Score: 0", font=("Arial", 18, "bold"))
        self.score_label.grid(row=0, column=0, pady=5)

        # ---------------- RESTART BUTTON ----------------
        self.restart_button = Button(
            self,
            text="Restart",
            font=("Arial", 14, "bold"),
            command=self.restart_game
        )
        self.restart_button.grid(row=0, column=1, padx=10)

        # ---------------- MAIN GRID ----------------
        self.main_grid = Frame(self, bg="lightgrey", bd=3)
        self.main_grid.grid(row=1, column=0, columnspan=2)

        # Create empty board
        self.board = [[0]*4 for _ in range(4)]

        self.gameboard()

        # Start game with two tiles
        self.restart_game()

        # Controls
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

    # ---------------- RESET GAME ----------------
    def restart_game(self):
        """Clear board and score then start fresh"""

        self.score = 0
        self.board = [[0]*4 for _ in range(4)]

        self.pickNewValue()
        self.pickNewValue()

        self.updateGame()

    # ---------------- CREATE TILES ----------------
    def gameboard(self):
        self.tiles = []

        for i in range(4):
            row = []
            for j in range(4):
                frame = Frame(self.main_grid, bg="white", width=90, height=90)
                frame.grid(row=i, column=j, padx=5, pady=5)

                label = Label(frame, bg="white", font=("Arial", 24, "bold"))
                label.place(relx=0.5, rely=0.5, anchor="center")

                row.append({"frame": frame, "number": label})
            self.tiles.append(row)

    # ---------------- MOVE + MERGE ----------------
    def compress_and_merge(self, row):
        row = [x for x in row if x != 0]

        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0

        row = [x for x in row if x != 0]
        return row + [0] * (4 - len(row))

    # ---------------- HELPERS ----------------
    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    # ---------------- SPAWN TILE ----------------
    def pickNewValue(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if not empty:
            return
        i, j = random.choice(empty)
        self.board[i][j] = 4 if random.randint(1, 5) == 1 else 2

    # ---------------- UPDATE UI ----------------
    def updateGame(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                if value == 0:
                    self.tiles[i][j]["frame"].configure(bg="white")
                    self.tiles[i][j]["number"].configure(text="", bg="white")
                else:
                    self.tiles[i][j]["frame"].configure(bg="orange")
                    self.tiles[i][j]["number"].configure(
                        text=str(value),
                        bg="orange",
                        fg="white"
                    )

        self.score_label.config(text=f"Score: {self.score}")
        self.update_idletasks()

    # ---------------- MOVEMENT ----------------
    def left(self, event):
        self.board = [self.compress_and_merge(row) for row in self.board]
        self.pickNewValue()
        self.updateGame()
        self.final_result()

    def right(self, event):
        self.board = [self.compress_and_merge(row[::-1])[::-1] for row in self.board]
        self.pickNewValue()
        self.updateGame()
        self.final_result()

    def up(self, event):
        self.transpose()
        self.board = [self.compress_and_merge(row) for row in self.board]
        self.transpose()
        self.pickNewValue()
        self.updateGame()
        self.final_result()

    def down(self, event):
        self.transpose()
        self.board = [self.compress_and_merge(row[::-1])[::-1] for row in self.board]
        self.transpose()
        self.pickNewValue()
        self.updateGame()
        self.final_result()

    # ---------------- MOVE CHECKS ----------------
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j + 1]:
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    # ---------------- GAME STATE ----------------
    def final_result(self):
        if any(2048 in row for row in self.board):
            self.show_message("YOU WIN!", "green")

        elif not any(0 in row for row in self.board) and \
             not self.horizontal_move_exists() and \
             not self.vertical_move_exists():
            self.show_message("GAME OVER", "red")

    def show_message(self, text, color):
        frame = Frame(self.main_grid, bg=color, bd=5)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(
            frame,
            text=text,
            bg=color,
            fg="white",
            font=("Arial", 32, "bold")
        ).pack()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = Tk()
    Game(root)
    root.mainloop()
