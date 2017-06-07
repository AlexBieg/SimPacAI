import tkinter


CELL_SIZE = 100
OFFSET = 5
BALL_OFFSET = 40
PLAYER_OFFSET = 20

class Canvas():
    def __init__(self, boards_actions):
        self.boards_actions = boards_actions

        self.master = tkinter.Tk()
        self.master.title = "Simple Pacman AI"

        width = self.boards_actions[0][0].width * CELL_SIZE + OFFSET
        height = self.boards_actions[0][0].height * CELL_SIZE + OFFSET

        self.canvas = tkinter.Canvas(self.master, width=width, height=height)
        self.canvas.pack()

        self.board_index = 0

        self.current_board_action = self.boards_actions[self.board_index]


    def show(self):

        self.update()

        self.master.mainloop()


    def update(self):
        self.draw_board(self.current_board_action[0])
        self.draw_ghost(self.current_board_action[0])

        if not self.current_board_action[0].is_dead:
            self.draw_player(self.current_board_action[0], self.current_board_action[1])

        self.board_index += 1
        if self.board_index < len(self.boards_actions):
            self.current_board_action = self.boards_actions[self.board_index]
        else:
            self.board_index = -1

        self.canvas.after(400, self.update)


    def draw_ghost(self, board):
        x = board.ghost_pos[0]
        y = board.ghost_pos[1]

        x1 = x * CELL_SIZE + OFFSET + PLAYER_OFFSET
        y1 = y * CELL_SIZE + OFFSET + PLAYER_OFFSET

        x2 = x * CELL_SIZE + CELL_SIZE - PLAYER_OFFSET
        y2 = y * CELL_SIZE + CELL_SIZE - PLAYER_OFFSET

        width = x2 - x1
        height = y2 - y1


        # Draw body
        self.canvas.create_arc(x1,y1,
                               x2,y2,
                               start = 0,
                               extent = 180,
                               fill="#FFA500")

        self.canvas.create_polygon(x1, y1 + (height/2),
                                   x2, y1 +(height/2),
                                   x2, y2,
                                   x2 - (width / 4), y2 - (height / 4),
                                   x2 - (width / 2), y2,
                                   x1 + (width / 4), y2 - (height / 4),
                                   x1, y2,
                                   fill="#FFA500")

        # Draw eyes
        eye_d = 15
        iris_d = 5
        width_div = 7
        iris_offset = 10
        self.canvas.create_oval(x1 + (width / width_div), y1 + (height / 5),
                               x1 + (width/width_div) + eye_d, y1 + (height/5) + eye_d,
                                fill="#FFFFFF",
                                width = 0)

        self.canvas.create_oval(x2 - (width / width_div), y1 + (height / 5),
                               x2 - (width/width_div) - eye_d, y1 + (height/5) + eye_d,
                                fill="#FFFFFF",
                                width = 0)

        self.canvas.create_oval(x1 + (width / width_div) + iris_offset, y1 + (height / 5) + (eye_d / 2),
                               x1 + (width/width_div) + iris_d, y1 + (height/5) + iris_d,
                                fill="#0000FF",
                                width = 0)

        self.canvas.create_oval(x2 - (width / width_div) - iris_offset, y1 + (height / 5) + (eye_d / 2),
                               x2 - (width/width_div) - iris_d, y1 + (height/5) + iris_d,
                                fill="#0000FF",
                                width = 0)

    def draw_player(self, board, action):
        x = board.player_pos[0]
        y = board.player_pos[1]
        extent = 270

        mapping = {"North": 135, "South": -45, "East": 45, "West": 225}

        self.canvas.create_arc(x * CELL_SIZE + OFFSET + PLAYER_OFFSET,
                                y * CELL_SIZE + OFFSET + PLAYER_OFFSET,
                                x * CELL_SIZE + CELL_SIZE - PLAYER_OFFSET,
                                y * CELL_SIZE + CELL_SIZE - PLAYER_OFFSET,
                                fill="#FFFF00",
                                start = mapping[action],
                               extent = extent,
                               style = tkinter.PIESLICE)

    def draw_board(self, board):
        for x in range(0, board.width):
            for y in range(0, board.height):
                cell_val = board.board[x][y]

                if cell_val == -1:
                    rec_color = "#0000FF"
                else:
                    rec_color = "#000000"

                self.canvas.create_rectangle(x * CELL_SIZE + OFFSET,
                                             y * CELL_SIZE + OFFSET,
                                             x * CELL_SIZE + CELL_SIZE,
                                             y * CELL_SIZE + CELL_SIZE,
                                             fill=rec_color)

                if cell_val == 1:
                    self.canvas.create_oval(x * CELL_SIZE + OFFSET + BALL_OFFSET,
                                            y * CELL_SIZE + OFFSET + BALL_OFFSET,
                                            x * CELL_SIZE + CELL_SIZE - BALL_OFFSET,
                                            y * CELL_SIZE + CELL_SIZE - BALL_OFFSET,
                                            fill="#FFFFFF")
