from tkinter import Frame, Label, Button, CENTER
import logic
import constants as c


class Game2048(Frame):
    def __init__(self):
        super().__init__()
        self.grid()
        self.master.title("2048 Game")

        # Key + Mouse bindings
        self.master.bind("<Key>", self.key_down)
        self.master.bind("<Button-1>", self.touch_start)
        self.master.bind("<ButtonRelease-1>", self.touch_end)

        self.start_x = 0
        self.start_y = 0

        self.score = 0
        self.grid_cells = []

        self.init_ui()
        self.restart_game()

    def init_ui(self):
        self.score_label = Label(self, text="Score: 0", font=("Verdana", 16))
        self.score_label.grid(row=0, column=0, columnspan=4, pady=5)

        Button(self, text="Restart", command=self.restart_game).grid(
            row=1, column=0, columnspan=4, pady=10
        )

        background = Frame(
            self,
            bg=c.BACKGROUND_COLOR_GAME,
            width=c.SIZE,
            height=c.SIZE
        )
        background.grid(row=2, column=0, columnspan=4)

        for i in range(c.GRID_LEN):
            row = []
            for j in range(c.GRID_LEN):
                cell = Frame(
                    background,
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    width=c.SIZE / c.GRID_LEN,
                    height=c.SIZE / c.GRID_LEN
                )
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)

                label = Label(
                    cell,
                    text="",
                    bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER,
                    font=c.FONT,
                    width=5,
                    height=2
                )
                label.grid()
                row.append(label)

            self.grid_cells.append(row)

    def restart_game(self):
        self.matrix = logic.start_game()
        logic.add_new_tile(self.matrix)
        logic.add_new_tile(self.matrix)
        self.score = 0
        self.update_ui()
        self.master.bind("<Key>", self.key_down)

    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")

        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].config(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY
                    )
                else:
                    self.grid_cells[i][j].config(
                        text=value,
                        bg=c.BACKGROUND_COLOR_DICT[value],
                        fg=c.CELL_COLOR_DICT[value]
                    )

    # ---------------- KEYBOARD CONTROL ----------------
    def key_down(self, event):
        key = event.keysym.lower()

        if key not in c.KEYS:
            return

        self.make_move(c.KEYS[key])

    # ---------------- TOUCHPAD CONTROL ----------------
    def touch_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def touch_end(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if abs(dx) < 30 and abs(dy) < 30:
            return  # Ignore small movements

        if abs(dx) > abs(dy):
            if dx > 0:
                self.make_move("RIGHT")
            else:
                self.make_move("LEFT")
        else:
            if dy > 0:
                self.make_move("DOWN")
            else:
                self.make_move("UP")

    # ---------------- MOVE HANDLER ----------------
    def make_move(self, direction):
        moves = {
            "UP": logic.move_up,
            "DOWN": logic.move_down,
            "LEFT": logic.move_left,
            "RIGHT": logic.move_right
        }

        self.matrix, changed, gained = moves[direction](self.matrix)

        if changed:
            logic.add_new_tile(self.matrix)
            self.score += gained
            self.update_ui()

            state = logic.get_game_state(self.matrix)
            if state in ("WON", "LOST"):
                self.master.unbind("<Key>")
                self.score_label.config(
                    text=f"You {state}! Final Score: {self.score}"
                )


if __name__ == "__main__":
    game = Game2048()
    game.mainloop()