import Board
import Actions
import Learning
import Draw
import threading


def get_intro():
    return "Welcome to SimPac! This is an AI agent that learns how to play a simplified version of Pacman."


def show_boards(boards):
    class DrawingThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            d = Draw.Canvas(boards)
            d.show()

    dt = DrawingThread()
    dt.start()


def build_board(file_path):
    mapping = {"*": 1, " ": 0, "G": 0, "P":0, "X": -1}
    if len(file_path) == 0:
        print("\n Loading Example Board...\n")
        # Open example file
        f = open("example_board.txt", "r")
    else:
        print("\n Loading Your Board...\n")
        # open specified file
        f = open(file_path, "r")

    contents = f.read().split("\n")

    board_arr = []
    ghost_pos = None
    player_pos = None
    for y, line in enumerate(contents):
        for x, char in enumerate(line):
            val = mapping[char]

            try:
                board_arr[x].append(val)
            except:
                board_arr.append([])
                board_arr[x].append(val)

            if char == "G":
                ghost_pos = (x, y)

            if char == "P":
                player_pos = (x, y)


    return Board.State(board_arr, player_pos, ghost_pos)

if __name__ == "__main__":
    print(get_intro())

    file_path = input("Please enter a file path to a board (if you have one): ")
    board = build_board(file_path)
    l = Learning.Learning(Actions.ACTIONS, Actions.move, Board.R, board)

    discount = input("Please enter a discount value (defaults to 0.9): ")

    if discount == "":
        discount = 0.9
    else:
        discount = float(discount)


    epsilon = input("Please enter an epsilon value (defaults to 0.1): ")

    if epsilon == "":
        epsilon = 0.1
    else:
        epsilon = float(epsilon)

    episodes = input("Please enter the number of episodes you wish to run (defaults to 1000): ")

    if episodes == "":
        episodes = 1000
    else:
        episodes = int(episodes)

    print("\nStarting Q-Learning")
    l.q_learning(discount, episodes, epsilon)
    print("Ended Q-Learning")

    l.build_policy()

    boards = []
    while not board.is_dead and not board.won:
        print()
        print(board)
        action = l.get_action(board)

        boards.append((board, action))
        board = Actions.move(board, action)

    print()
    print(board)
    boards.append((board, action))

    show_resp = input("We printed the results of following the policy above. Would you like to see it animated? ")

    if show_resp.lower().startswith("y"):
        show_boards(boards)

