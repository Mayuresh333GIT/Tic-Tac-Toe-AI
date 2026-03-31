import tkinter as tk
from tkinter import messagebox

board = [""] * 9
player_symbol = "X"
ai_symbol = "O"
game_over = False

root = tk.Tk()
root.title("Tic Tac Toe - Minimax AI")

status_label = tk.Label(root, text="Choose X or O to start", font=("Arial", 16))
status_label.grid(row=0, column=0, columnspan=3, pady=10)

buttons = []
def check_winner(b):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b1,c in wins:
        if b[a] == b[b1] == b[c] != "":
            return b[a], (a,b1,c)

    if "" not in b:
        return "Draw", None

    return None, None


def minimax(b, depth, is_max, alpha, beta):

    winner, _ = check_winner(b)

    if winner == ai_symbol:
        return 10 - depth
    if winner == player_symbol:
        return depth - 10
    if winner == "Draw":
        return 0

    if is_max:
        best = -1000

        for i in range(9):
            if b[i] == "":
                b[i] = ai_symbol
                score = minimax(b, depth+1, False, alpha, beta)
                b[i] = ""
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break

        return best

    else:
        best = 1000

        for i in range(9):
            if b[i] == "":
                b[i] = player_symbol
                score = minimax(b, depth+1, True, alpha, beta)
                b[i] = ""
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break

        return best


def ai_move():
    global game_over

    best_score = -1000
    move = None

    for i in range(9):
        if board[i] == "":
            board[i] = ai_symbol
            score = minimax(board, 0, False, -1000, 1000)
            board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    if move is not None:
        board[move] = ai_symbol
        buttons[move]["text"] = ai_symbol

    check_game()


def player_move(i):
    global game_over

    if board[i] == "" and not game_over:
        board[i] = player_symbol
        buttons[i]["text"] = player_symbol
        check_game()

        if not game_over:
            root.after(200, ai_move)


def check_game():
    global game_over

    winner, combo = check_winner(board)

    if winner:
        game_over = True

        if winner == "Draw":
            status_label.config(text="Game Draw")
        else:
            status_label.config(text=f"{winner} Wins!")

            if combo:
                for i in combo:
                    buttons[i].config(bg="green", fg="white")

def restart():
    global board, game_over

    board = [""] * 9
    game_over = False
    status_label.config(text=f"You are {player_symbol}")

    for b in buttons:
        b.config(text="", bg="white", fg="black")

    if player_symbol == "O":
        ai_move()


def choose(symbol):
    global player_symbol, ai_symbol

    player_symbol = symbol
    ai_symbol = "O" if symbol == "X" else "X"

    restart()


for i in range(9):
    btn = tk.Button(root,
                    text="",
                    font=("Arial", 28),
                    width=4,
                    height=2,
                    bg="white",
                    command=lambda i=i: player_move(i))

    btn.grid(row=(i//3)+2, column=i%3)
    buttons.append(btn)

x_button = tk.Button(root, text="Play as X", command=lambda: choose("X"))
x_button.grid(row=1, column=0)

o_button = tk.Button(root, text="Play as O", command=lambda: choose("O"))
o_button.grid(row=1, column=1)

restart_button = tk.Button(root, text="Restart", command=restart)
restart_button.grid(row=1, column=2)

root.mainloop()
