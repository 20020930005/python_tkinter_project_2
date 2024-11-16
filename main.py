import tkinter as tk
import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}


# Game Logic functions
def get_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns


def check_victory(columns, lines, bet, values):
    victory = 0
    victory_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            if column[line] != symbol:
                break
        else:
            victory += values[symbol] * bet
            victory_lines.append(line + 1)
    return victory, victory_lines


# UI implementation with tkinter
class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        self.root.configure(bg="#1a1a1d")

        #  Balance at initial phase
        self.balance = 0
        self.create_deposit_screen()

    def create_deposit_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Slot Machine", font=("Helvetica", 18, "bold"), bg="#1a1a1d",
                 fg="#f6f6f6").pack(pady=10)
        tk.Label(self.root, text="Enter your initial deposit: $", font=("Helvetica", 12), bg="#1a1a1d",
                 fg="#f6f6f6").pack()

        self.deposit_entry = tk.Entry(self.root, font=("Helvetica", 12), width=10)
        self.deposit_entry.pack(pady=5)

        tk.Button(self.root, text="Deposit", command=self.deposit, font=("Helvetica", 12), bg="#4CAF50", fg="white",
                  width=10).pack(pady=10)

    def deposit(self):
        try:
            amount = int(self.deposit_entry.get())
            if amount <= 0:
                raise ValueError("Deposit must be greater than zero.")
            self.balance = amount
            self.create_game_screen()
        except ValueError as e:
            tk.Label(self.root, text=f"Error: {e}", fg="red", bg="#1a1a1d").pack()

    def create_game_screen(self):
        self.clear_screen()

        tk.Label(self.root, text=f"Current Balance: ${self.balance}", font=("Helvetica", 14, "bold"), bg="#1a1a1d",
                 fg="#f6f6f6").pack(pady=10)

        tk.Label(self.root, text="Number of lines to bet on (1-3):", font=("Helvetica", 12), bg="#1a1a1d",
                 fg="#f6f6f6").pack()
        self.lines_entry = tk.Entry(self.root, font=("Helvetica", 12), width=5)
        self.lines_entry.pack(pady=5)

        tk.Label(self.root, text="Bet per line ($1-$100):", font=("Helvetica", 12), bg="#1a1a1d", fg="#f6f6f6").pack()
        self.bet_entry = tk.Entry(self.root, font=("Helvetica", 12), width=5)
        self.bet_entry.pack(pady=5)

        tk.Button(self.root, text="Spin", command=self.play_game, font=("Helvetica", 12), bg="#4CAF50", fg="white",
                  width=10).pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg="#1a1a1d", fg="#f6f6f6")
        self.result_label.pack(pady=10)

        self.slot_display = tk.Label(self.root, text="", font=("Courier", 18), bg="#1a1a1d", fg="#FFD700")
        self.slot_display.pack(pady=5)

        # Continue and Exit Buttons
        tk.Button(self.root, text="Continue", command=self.create_game_screen, font=("Helvetica", 12), bg="#2196F3",
                  fg="white", width=12, height=4).pack(side="left", padx=10, pady=20)
        tk.Button(self.root, text="Exit", command=self.root.quit, font=("Helvetica", 12), bg="#f44336", fg="white",
                  width=12,height=3).pack(side="right", padx=10, pady=20)

    def play_game(self):
        try:
            lines = int(self.lines_entry.get())
            bet = int(self.bet_entry.get())
            total_bet = lines * bet

            if not (1 <= lines <= MAX_LINES):
                raise ValueError("Lines must be between 1 and 3.")
            if not (MIN_BET <= bet <= MAX_BET):
                raise ValueError(f"Bet must be between ${MIN_BET} and ${MAX_BET}.")
            if total_bet > self.balance:
                raise ValueError("Insufficient balance for this bet.")

            self.balance -= total_bet
            columns = get_spin(ROWS, COLS, symbol_count)
            victory, victory_lines = check_victory(columns, lines, bet, symbol_value)
            self.balance += victory

            # Update UI with spin results
            result_text = " | ".join(" ".join(col) for col in columns)
            self.slot_display.config(text=result_text)

            if victory > 0:
                result_msg = f"You won ${victory} on lines: {', '.join(map(str, victory_lines))}!"
            else:
                result_msg = "No winning lines."

            self.result_label.config(text=f"{result_msg} Current balance: ${self.balance}")

            if self.balance <= 0:
                self.result_label.config(text="Game Over! You are out of balance.")
                self.create_deposit_screen()

        except ValueError as e:
            self.result_label.config(text=f"Error: {e}", fg="red")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# Initialize the GUI
root = tk.Tk()
app = SlotMachineApp(root)
root.mainloop()