import copy

NUM_TO_CELL = {0: " ", 1: "*", -1: "X"}
CELL_TO_NUM = {" ": 0, "*": 1, "X": -1}
PLAYER = "P"
GHOST = "G"

COST_OF_LIVING = -.1


class State():
    '''
    A State of the board
    '''
    def __init__(self, board_arr, player_pos=(0,0), ghost_pos=(0,0), turn_num=0, is_dead=False, won=False):
        self.board = copy.deepcopy(board_arr)
        self.turn_num = turn_num
        self.player_pos = player_pos
        self.ghost_pos = ghost_pos

        self.width = len(self.board)
        self.height = len(self.board[0])

        self.is_dead = is_dead
        self.won = won

    def __str__(self):
        s = ""

        for y in range(0, self.height):
            for x in range(0, len(self.board) * 2 + 1):
                s += "-"

            s += "\n|"

            for x in range(0, len(self.board)):

                pos = (x, y)
                if pos == self.ghost_pos:
                    s += GHOST
                elif pos == self.player_pos:
                    s += PLAYER
                else:
                    val = self.board[x][y]
                    s += NUM_TO_CELL[val]

                s += "|"

            s += "\n"
        for x in range(0, len(self.board) * 2 + 1):
            s += "-"
        return s

    def __hash__(self):
        return self.__str__().__hash__()


    def __copy__(self):
        return State(self.board, self.player_pos, self.ghost_pos, self.turn_num)

    def __eq__(self, other):
        is_same = True

        if not self.board.__eq__(other.board):
           is_same = False

        if not self.player_pos == other.player_pos:
            is_same = False

        if not self.ghost_pos == other.ghost_pos:
            is_same = False

        return is_same



    def __lt__(self, other):
        # Only for priority queue
        return 0 < 0


    def is_similar(self, other):
        pos_weight = 5

        num_diffs = 0
        total_cells = self.width * self.height

        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[x])):
                self_cell = self.board[x][y]
                other_cell = other.board[x][y]

                if not self_cell.__eq__(other_cell):
                    num_diffs += 1

        if self.player_pos != other.player_pos:
            num_diffs += 1 * pos_weight

        if self.ghost_pos != other.ghost_pos:
            num_diffs += 1 * pos_weight

        possible_diffs = total_cells + 1 * pos_weight + 1 * pos_weight# Cells, player_pos, ghost_pos

        return 1 - (num_diffs / possible_diffs)



def R(s, a, sp):
    tot = 0
    if sp.is_dead:
        tot += -1000
    if sp.won:
        tot += 1000

    val = s.board[sp.player_pos[0]][sp.player_pos[1]]
    tot += val * 5

    return tot + COST_OF_LIVING