import random, math, copy


class Learning():

    def __init__(self, actions, move_func, R_func, start_board):
        self.actions = actions
        self.move = move_func
        self.R = R_func
        self.start_board = start_board
        self.known_states = set()


    def get_max_action(self, board):
        best_action = None
        max_action_val = -math.inf
        for action in self.actions:
            try:
                val = self.Q[(board, action)]
            except KeyError:
                self.Q[(board, action)] = 0
                val = 0

            if val > max_action_val:
                max_action_val = val
                best_action = action

        return best_action

    def q_learning(self, discount, n_episodes, epsilon):
        self.Q = {}
        N = {}

        for ep in range(0, n_episodes):
            if ep % 50 == 0:
                print(str(round(ep/n_episodes * 100)) + "% Complete")

            board = self.start_board
            while not board.is_dead and not board.won:

                self.known_states.add(board)

                if random.random() < epsilon:
                    action = random.choice(self.actions)
                else:
                    action = self.get_max_action(board)

                prev_board = board

                board = self.move(board, action)

                try:
                    N[(prev_board, action)] += 1
                except KeyError:
                    N[(prev_board, action)] = 1

                max_new_action = self.get_max_action(board)

                try:
                    max_new_val = self.Q[(board, max_new_action)]
                except KeyError:
                    max_new_val = 0
                    self.Q[(board, max_new_action)] = 0

                sample = self.R(prev_board, action, board) + (discount * max_new_val)

                alpha = 1/N[(prev_board, action)]

                try:
                    self.Q[(prev_board, action)]
                except KeyError:
                    self.Q[(prev_board, action)] = 0

                self.Q[(prev_board, action)] = ((1-alpha) * self.Q[(prev_board, action)]) + (alpha * sample)


    def get_similar_action(self, board):
        max_sim_val = 0
        most_sim_board = None

        for key in self.Q.keys():
            sim_val = board.is_similar(key)

            if sim_val >= max_sim_val:
                max_sim_val = sim_val
                most_sim_board = key


        return self.get_max_action(most_sim_board)


    def build_policy(self):
        self.policy = {}
        for board in self.known_states:
            max_action = self.get_max_action(board)
            self.policy[board] = max_action


    def get_action(self, board):
        try:
            return self.policy[board]
        except KeyError:
            max_sim_board = None
            max_sim_val = 0

            for key in self.policy.keys():
                sim_val = board.is_similar(key)
                if sim_val >= max_sim_val:
                    max_sim_val = sim_val
                    max_sim_board = key


            return self.policy[max_sim_board]




