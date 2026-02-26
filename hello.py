import tkinter as tk
from tkinter import messagebox


class PencilGame:
    """Two-player pencil game: remove 1, 2, or 4 pencils; taking the last loses."""

    STARTING_PENCILS = 15
    VALID_MOVES = (1, 2, 4)

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("15 Pencils")
        self.root.resizable(False, False)

        self.pencils = self.STARTING_PENCILS
        self.current_player = 1
        self.game_over = False

        self.status_var = tk.StringVar()
        self.pencil_vars: list[tk.StringVar] = []

        self._build_ui()
        self._refresh_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, padx=16, pady=16)
        container.pack()

        tk.Label(
            container,
            text="Take 1, 2, or 4 pencils.\nWhoever takes the last pencil loses!",
            font=("Arial", 11),
            justify="center",
        ).pack(pady=(0, 12))

        self.status_label = tk.Label(
            container,
            textvariable=self.status_var,
            font=("Arial", 12, "bold"),
        )
        self.status_label.pack(pady=(0, 10))

        board = tk.Frame(container)
        board.pack(pady=(0, 12))

        for i in range(self.STARTING_PENCILS):
            var = tk.StringVar(value="✏")
            self.pencil_vars.append(var)
            tk.Label(board, textvariable=var, font=("Arial", 22)).grid(
                row=i // 5, column=i % 5, padx=4, pady=4
            )

        controls = tk.Frame(container)
        controls.pack()

        self.move_buttons = []
        for amount in self.VALID_MOVES:
            button = tk.Button(
                controls,
                text=f"Remove {amount}",
                width=12,
                command=lambda value=amount: self.play_turn(value),
            )
            button.pack(side="left", padx=4)
            self.move_buttons.append(button)

        tk.Button(container, text="Restart", width=12, command=self.reset_game).pack(
            pady=(12, 0)
        )

    def _refresh_ui(self) -> None:
        for i, var in enumerate(self.pencil_vars):
            var.set("✏" if i < self.pencils else "")

        if self.game_over:
            for button in self.move_buttons:
                button.config(state="disabled")
            return

        self.status_var.set(f"Player {self.current_player}'s turn — pencils left: {self.pencils}")

        for button, amount in zip(self.move_buttons, self.VALID_MOVES):
            state = "normal" if amount <= self.pencils else "disabled"
            button.config(state=state)

    def play_turn(self, amount: int) -> None:
        if self.game_over or amount not in self.VALID_MOVES or amount > self.pencils:
            return

        self.pencils -= amount

        # Misère rule: player who takes the last pencil loses.
        if self.pencils == 0:
            loser = self.current_player
            winner = 2 if loser == 1 else 1
            self.game_over = True
            self.status_var.set(
                f"Player {loser} took the last pencil and loses. Player {winner} wins!"
            )
            self._refresh_ui()
            messagebox.showinfo("Game over", self.status_var.get())
            return

        self.current_player = 2 if self.current_player == 1 else 1
        self._refresh_ui()

    def reset_game(self) -> None:
        self.pencils = self.STARTING_PENCILS
        self.current_player = 1
        self.game_over = False
        self._refresh_ui()


def main() -> None:
    root = tk.Tk()
    PencilGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
