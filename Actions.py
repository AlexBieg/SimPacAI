import math
from queue import PriorityQueue

ACTIONS = ["North", "South", "East", "West"]
ACTION_TO_DIRECTION = {"North": (0,-1), "South": (0, 1), "East": (1, 0), "West": (-1, 0)}
MAX_TURN_NUM = 1000

def is_movable_space(board, pos):
    if pos[0] < 0 or pos[0] >= board.width or\
        pos[1] < 0 or pos[1] >= board.height:
        return False

    if board.board[pos[0]][pos[1]] < 0:
        return False

    return True

def can_move(board, action, is_player=True):
    if is_player:
        pos = board.player_pos
    else:
        pos = board.ghost_pos

    direction = ACTION_TO_DIRECTION[action]
    new_pos = (pos[0] + direction[0], pos[1] + direction[1])

    return is_movable_space(board, new_pos)


def move(old_board, action, is_player=True):
    board = old_board.__copy__()

    if is_player:
        pos = board.player_pos
    else:
        pos = board.ghost_pos

    if can_move(board, action, is_player):
        direction = ACTION_TO_DIRECTION[action]
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])

        if is_player:
            # Increase turn
            board.turn_num += 1

            # update player pos
            board.player_pos = new_pos

            # Update new cell value
            board.board[new_pos[0]][new_pos[1]] = 0

            if not check_win(board):
                # move Ghost
                board = move_ghost(board)
        else:
            board.ghost_pos = new_pos

    else:
        board = move_ghost(board)

    if board.player_pos == board.ghost_pos:
        board.is_dead = True

    if board.turn_num > MAX_TURN_NUM:
        board.is_dead = True

    board.won = check_win(board)

    return board


def check_win(board):
    has_dots = False
    for x in board.board:
        for cell in x:
            if cell > 0:
                has_dots = True

    return not has_dots


def move_ghost(old_board):
    backlinks = {}
    backlinks[old_board] = old_board

    open = PriorityQueue()
    closed = []

    g_scores = {}
    g_scores[old_board] = 0

    open.put((0, old_board))

    while not open.empty():
        b_tuple = open.get()
        board = b_tuple[1]

        closed.append(board)

        # Check capture
        if board.ghost_pos == board.player_pos:
            break;

        b_g = g_scores[board]

        for action in ACTIONS:
            if can_move(board, action, False):
                new_board = move(board, action, False)
                if not (new_board in closed):
                    backlinks[new_board] = board
                    new_b_g = b_g + 1
                    g_scores[new_board] = new_b_g
                    new_b_priority = new_b_g + ghost_heur(new_board)
                    open.put((new_b_priority, new_board))


    back_board = backlinks[board]
    while not back_board.__eq__(old_board):
        board = back_board
        back_board = backlinks[board]

    return board


def ghost_heur(board):
    # Manhattan Distance
    x = abs(board.player_pos[0] - board.ghost_pos[0])
    y = abs(board.player_pos[1] - board.ghost_pos[1])
    return x + y
