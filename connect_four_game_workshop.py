from collections import deque


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InvalidColumnError(Exception):
    pass


class FullColumnError(Exception):
    pass


# Print matrix.
def print_matrix(M):
    for sub_matrix in M:
        print(f'{bcolors.HEADER}{bcolors.BOLD}[ {bcolors.ENDC}', end='')
        for el in sub_matrix:
            if el == 1:
                print(f'{bcolors.OKBLUE}{bcolors.BOLD}{el}{bcolors.BOLD}{bcolors.ENDC}', end=' ')
            elif el == 2:
                print(f'{bcolors.FAIL}{bcolors.BOLD}{el}{bcolors.BOLD}{bcolors.ENDC}', end=' ')
            else:
                print(f'{bcolors.OKGREEN}{el}{bcolors.ENDC}', end=' ')
        print(f'{bcolors.HEADER}{bcolors.BOLD}]{bcolors.ENDC}')


def validate_column_choice(selected_col_num, max_col_index):
    # Verify player choice of column number of is correct.
    if not (0 <= selected_col_num <= max_col_index):
        raise InvalidColumnError


def place_player_choice(M, selected_col_index, current_player_num):
    # Place player marker on the spot.
    # Check if the column  is full if so - throw error.
    row_count = len(M)
    for row_index in range(row_count - 1, -1, -1):
        current_element = M[row_index][selected_col_index]
        if current_element == 0:
            M[row_index][selected_col_index] = current_player_num
            return
    raise FullColumnError


def is_inside(r, c, N, M):
    return 0 <= r < N and 0 <= c < M


# All winning positions -> left,right,up,down and all diagonals.
def check_for_win(ma, current_player):
    win_happened = False
    all_pos = {
        'right': [(0, 1), (0, 2), (0, 3)],
        'left': [(0, - 1), (0, - 2), (0, - 3)],
        'up': [(- 1, 0), (- 2, 0), (- 3, 0)],
        'down': [(1, 0), (2, 0), (3, 0)],

        'right_up': [(1, 1), (2, 2), (3, 3)],
        'right_down': [(-1, 1), (-2, 2), (-3, 3)],
        'left_up': [(-1, -1), (-2, -2), (-3, -3)],
        'left_down': [(1, -1), (2, -2), (3, -3)],
    }
    for r_index in range(rows_count):
        for c_index in range(cols_count):
            if ma[r_index][c_index] == current_player:

                for direction, positions in all_pos.items():
                    win_steps = 0
                    for curr_pos in positions:
                        if not is_inside(r_index + curr_pos[0], c_index + curr_pos[1], rows_count, cols_count) or \
                                not ma[r_index + curr_pos[0]][c_index + curr_pos[1]] == current_player:
                            continue
                        else:
                            win_steps += 1

                    if win_steps >= 3:
                        win_happened = True
                        # If True , break them all outer loops.
                        break

                if win_happened:
                    break
            if win_happened:
                break
        if win_happened:
            break

    return win_happened


rows_count = 6
cols_count = 7
# create matrix
matrix = [[0 for _ in range(cols_count)] for row_num in range(rows_count)]
print_matrix(matrix)
total_turns = 0
turns = deque([1, 2])
while True:
    player_turn = turns[0]
    try:
        # Read column choice from input
        colum_num = int(input(f"{bcolors.OKCYAN}Player {player_turn}{bcolors.ENDC}, please choose a column: ")) - 1
        validate_column_choice(colum_num, cols_count - 1)
        place_player_choice(matrix, colum_num, player_turn)
        print_matrix(matrix)
    except InvalidColumnError:
        print(f"{bcolors.WARNING} This column is not valid. "
              f"Please select a number between {bcolors.ENDC} "
              f"{bcolors.HEADER}{bcolors.BOLD}1 and {cols_count}{bcolors.BOLD}{bcolors.ENDC} {bcolors.ENDC}")
        continue
    except ValueError:
        print(f"{bcolors.WARNING} Please select a valid digit!{bcolors.ENDC}")
        continue
    except FullColumnError:
        print(f"{bcolors.WARNING} This column is already full! Please, select other column number!{bcolors.ENDC}")
        continue

    total_turns += 1
    if total_turns >= 7:
        if check_for_win(matrix, player_turn):
            print()
            if player_turn == 1:
                print(f'{bcolors.OKBLUE}{bcolors.BOLD}Player {player_turn} WINS :) !{bcolors.ENDC}')
            elif player_turn == 2:
                print(f'{bcolors.FAIL}{bcolors.BOLD}Player {player_turn} WINS :) !{bcolors.ENDC}')
            break

    turns.rotate()
