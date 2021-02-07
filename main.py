
from time import sleep
from copy import copy, deepcopy
import sys
from operator import add, sub

# write 6 lines to the screeen (anything)
# below put an input
# when the input is entered, rewrite the above 6 lines to the new input

COLUMNS = 7
ROWS = 6
HEADER = ["  A |","  B |","  C |","  D |","  E |","  F |","  G |"]
EMPTY = "    |"
CROSS = "  x |"
NAUGHT = "  o |"
MAX_TURNS = COLUMNS * ROWS
INPUT_ATTEMPTS = 2
VALID_COLUMNS = ["A", "B", "C", "D", "E", "F", "G"]
COLUMNS_MAPPING = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
}

players = "1"

player_input = input("Hello, how many players [1 or 2]:")
if player_input in ["1", "2"]:
    players = player_input
else:
    sys.stdout.write(
        "... Please read the instructions. "
        "Better luck next time."
    )

board = []
row = []

board.append(HEADER)

for col in range(COLUMNS):
    row.append(EMPTY)

for j in range(ROWS):
    copied_row = deepcopy(row)
    board.append(copied_row)

def print_to_screen(text: str):
    """Helper function for printing out/updating the board on the terminal"""
    print(text, file=sys.stdout)
    # sys.stdout.flush()

def up_a_line():
    sys.stdout.write("\033[F")

def clear_line():
    sys.stdout.write("\x1b[2K")

def reset_writer():
    for i in range(ROWS):
        up_a_line()
    sys.stdout.flush()

def update_board():
    for current_row in board:
        clear_line()
        string_row = current_row.copy()
        row_to_print = "".join(string_row)
        print_to_screen(f'|{row_to_print}')
    sys.stdout.flush()

def update_board_f():
    for current_row in board:
        clear_line()
    sys.stdout.flush()

def play_position(position: int, token: str):
    current_index = len(board) - 1
    while current_index >= 0:
        if board[current_index][position] == EMPTY:
            board[current_index][position] = token
            break
        current_index -= 1

def check_for_win(column: int, token: str):
    return any([
        check_winning_columns(column, token),
        check_winning_rows(token),
        check_winning_diagonal(column, token)
    ])

def check_winning_columns(column: int, token: str):
    current_index = len(board) - 1
    matches = 0
    while current_index >= 0:
        if board[current_index][column] == token:
            matches += 1
            if matches >= 4:
                return True
        else:
            matches = 0
        current_index -= 1
    return False

def check_winning_rows(token: str):
    current_index = len(board) - 1
    matches = 0
    while current_index >= 0:
        for col in range(COLUMNS):
            if board[current_index][col] == token:
                matches += 1
                if matches >= 4:
                    return True
            else:
                matches = 0
        matches = 0
        current_index -= 1
    return False

def find_diagonal(left: bool, row: int, column: int, token: str):
    # row = 3
    # column = 3
    # left = true
    # token = CROSS

    for index in range(1, 5):
        
        # add rows to go down
        board_row = add(row, index)

        operation = sub if left else add
        board_column = operation(column, index)
        
        if board_column < 0:
            return False
        if board_column > COLUMNS - 1 :
            return False
        if board_row < 1:
            return False
        if board_row > ROWS:
            return False

        if board[board_row][board_column] != token:
            return False
    return True

def check_winning_diagonal(column: int, token: str):
    current_index = len(board) - 1

    while current_index >= 0:
        if board[current_index][column] == token:
            #  downwards possible
            # start down left, move to up right
            # then start down right, move to up left
            if any([
                find_diagonal(
                    left=True,
                    row=current_index,
                    column=column,
                    token=token
                ),
                find_diagonal(
                    left=True,
                    row=current_index-1,
                    column=column+1,
                    token=token
                ),
                find_diagonal(
                    left=True,
                    row=current_index-2,
                    column=column+2,
                    token=token
                ),
                find_diagonal(
                    left=True,
                    row=current_index-3,
                    column=column+3,
                    token=token
                ),
                find_diagonal(
                    left=False,
                    row=current_index,
                    column=column,
                    token=token
                ),
                find_diagonal(
                    left=False,
                    row=current_index-1,
                    column=column-1,
                    token=token
                ),
                find_diagonal(
                    left=False,
                    row=current_index-2,
                    column=column-2,
                    token=token
                ),
                find_diagonal(
                    left=False,
                    row=current_index-3,
                    column=column-3,
                    token=token
                ),
            ]):
                return True
        current_index -= 1
    return False

# draw the empty board
update_board()

winner = ""

# player 1 = true, player 2 = false
player_one = True

for turn in range(MAX_TURNS):
    if player_one:
        name = "One"
        token = CROSS
    else:
        name = "Two"
        token = NAUGHT

    user_input = input(f"Player {name}, your turn: ")
    for attempts in range(INPUT_ATTEMPTS):
        user_input = user_input.upper()
        if user_input in VALID_COLUMNS:
            # move up to the board
            up_a_line()
            # move to the top of the board
            reset_writer()
            # user_input >> position
            position = COLUMNS_MAPPING[user_input]
            play_position(position, token)
            up_a_line()
            update_board()
            if check_for_win(position, token):
                winner = name
            break
        else:
            valid_columns = ", ".join(VALID_COLUMNS)
            up_a_line()
            sys.stdout.write(
                "This was wrong... please enter one of the valid coluns "
                f"{valid_columns}"
            )
            sys.stdout.flush()
            # up_a_line()
            sleep(2)
            clear_line()
            user_input = input(f"\rPlayer {name}, your turn: ")

    if winner != "":
        break

    if players == "2":
        player_one = not player_one

# if no winner
if winner == "" :
    print(" ------ DRAW -----  ")
else:
    print(f" ------ PLAYER {winner} WIN!!-----  ")
