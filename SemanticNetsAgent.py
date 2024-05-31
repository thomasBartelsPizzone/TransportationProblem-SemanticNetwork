import numpy as np
#import heapq


class SemanticNetsAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_sheep, initial_wolves):
        # Add your code here! Your solve method should receive
        # the initial number of sheep and wolves as integers,
        # and return a list of 2-tuples that represent the moves
        # required to get all sheep and wolves from the left
        # side of the river to the right.
        #
        # If it is impossible to move the animals over according
        # to the rules of the problem, return an empty list of
        # moves.
        #print(f"solve: {initial_sheep} sheep and {initial_wolves} wolves are on the left bank")
        moves_list_list = []
        # depth = 0
        # if initial_sheep + initial_wolves < 3:
        #     depth = 1
        # elif initial_sheep >= 10:
        #     depth = initial_wolves + initial_sheep + 5
        # else:
        #     depth = 5 * initial_sheep
        # while depth > 0:
        #     moves_ = 0
        #     agents_agent = ScorpionAndToad()
        #     moves_ = agents_agent.real_solve(initial_sheep, initial_wolves)
        #     moves_list_list.append(moves_)
        #     #
        #     depth -= 1
        #
        # moves_list = path_cost_(moves_list_list)
        # print("moves_list")
        # return moves_list
        agents_agent = ScorpionAndToad()
        return agents_agent.search_bfs(initial_sheep, initial_wolves)
        #ans = agents_agent.search_bfs(initial_sheep, initial_wolves)
        #print(f"solve: {initial_sheep} sheep and {initial_wolves} wolves are on the left bank")
        #print(ans)
        #return ans


class ScorpionAndToad:
    def __init__(self):
        # binary direction value True means next move is right
        self.direction = True
        self.total_players = 0
        self.all_legal_moves = [(1, 1), (0, 1), (1, 0), (0, 2), (2, 0)]
        self.states_history = np.array([[0, 0, 0, 0, 0]])
        # the teams
        self.sheep_left = 0
        self.sheep_right = 0
        self.wolves_left = 0
        self.wolves_right = 0

    def check_move(self, sheep_left, sheep_right, wolves_left, wolves_right, direction):
        # print("sheepLeft: ", sheep_left)
        # print("sheepRight: ", sheep_right)
        # print("wolvesLeft: ", wolves_left)
        # print("wolvesRight: ", wolves_right)
        # print("direction: ", direction)
        if sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0:
            # print("failed bc - (sheep_left < 0 or sheep_right < 0 or wolves_left < 0 or wolves_right < 0)")
            return False
        elif (wolves_left > sheep_left) and (sheep_left > 0):
            # print("failed bc - (wolves_left > sheep_left) and (sheep_left > 0)")
            return False
        elif (wolves_right > sheep_right) and (sheep_right > 0):
            # print("failed bc - ((wolves_right > sheep_right) and (sheep_right > 0))")
            return False
        elif sheep_left + wolves_left == self.total_players:
            # print("failed bc - (sheep_left + wolves_left == self.total_players)")
            return False
        elif (sheep_left == 0 and wolves_right == 0) and direction is False:
            # print("failed bc - ((sheep_left == 0 and wolves_right == 0) and direction is False)")
            return False
        elif (wolves_right + sheep_right == 1) and direction is False:
            #elif (wolves_right + sheep_right == 1) and self.total_players < 5 and direction is False:
            # print("failed bc - ((wolves_right + sheep_right == 1) and direction is False)")
            # elif (wolves_right == 1) and direction is False:
            return False
        else:
            return True

    def state_check(self, sheep_left, sheep_right, wolves_left, wolves_right, direction, st_hist):
        new_move = np.array([[sheep_left, sheep_right, wolves_left, wolves_right, direction]])
        states_copy = np.copy(st_hist)
        new_states = np.vstack((states_copy, new_move))
        unique_moves = np.unique(new_states, axis=0)
        #
        # if np.equal(new_states, unique_moves).all():
        if new_states.shape == unique_moves.shape:
            return True, new_states
        else:
            return False, states_copy

    def next_move(self, mov, sheep_left, sheep_right, wolves_left, wolves_right, direction, history):
        #
        non_d_sheep_mov, non_d_wolf_mov = mov
        if direction:
            # print(f"in direction: {non_d_sheep_mov} and {non_d_wolf_mov}")
            sheep_left -= non_d_sheep_mov
            sheep_right += non_d_sheep_mov
            wolves_left -= non_d_wolf_mov
            wolves_right += non_d_wolf_mov
        else:
            # print(f"in !direction: {non_d_sheep_mov} and {non_d_wolf_mov}")
            sheep_left += non_d_sheep_mov
            sheep_right -= non_d_sheep_mov
            wolves_left += non_d_wolf_mov
            wolves_right -= non_d_wolf_mov
        #########
        # check #
        #########
        # print("check the check_move")
        mov_check_ = self.check_move(sheep_left, sheep_right, wolves_left, wolves_right, not direction)
        # print("mov_check_ was: ", mov_check_)
        if mov_check_:
            # print("check the state_check")
            st_check_, st_hist = self.state_check(sheep_left, sheep_right, wolves_left, wolves_right, not direction
                                                  , history)
            # print("state_check was: ", st_check_)
            if st_check_:
                return True, st_hist
        return False, history

    def bfs(self):
        # default_tuple = np.random.choice(np.array(self.all_legal_moves))
        #
        shuffle_moves = np.copy(self.all_legal_moves)
        np.random.shuffle(shuffle_moves)
        default_tuple = tuple(shuffle_moves[0])
        default_score = float("-inf")
        #default_tuple = self.all_legal_moves[0]
        valid_count = 0
        #
        for mv in shuffle_moves:
            #for mv in self.all_legal_moves:
            # for mv in aaa:
            # print("the move was: ", mv)
            # print("b4 move")
            # print("move: ", mv,"\nsheep_left: ", self.sheep_left, "\nsheep_right: ", self.sheep_right
            #       , "\nwolves_left: ", self.wolves_left, "\nwolves_right: ", self.wolves_right
            #       , "\ndirection: ", self.direction, "\nstates_history: ", self.states_history)
            valid_mov, new_his = self.next_move(mv, self.sheep_left, self.sheep_right, self.wolves_left
                                                , self.wolves_right, self.direction, self.states_history)
            #
            if valid_mov:
                # #
                # print(new_his)
                valid_count += 1
                ####
                non_d_sheep_mov, non_d_wolf_mov = mv
                ##
                # check score
                if self.direction:
                    if (self.sheep_right + non_d_sheep_mov + self.wolves_right + non_d_wolf_mov) > default_score:
                        default_score = self.sheep_right + non_d_sheep_mov + self.wolves_right + non_d_wolf_mov
                        default_tuple = tuple(mv)
                else:
                    if (self.sheep_right - non_d_sheep_mov + self.wolves_right - non_d_wolf_mov) > default_score:
                        default_score = self.sheep_right - non_d_sheep_mov + self.wolves_right - non_d_wolf_mov
                        default_tuple = tuple(mv)
        if valid_count > 0:
            non_d_sheep_mov, non_d_wolf_mov = default_tuple
            if self.direction:
                self.sheep_left -= non_d_sheep_mov
                self.sheep_right += non_d_sheep_mov
                self.wolves_left -= non_d_wolf_mov
                self.wolves_right += non_d_wolf_mov
            else:
                # print("self.direction is false")
                self.sheep_left += non_d_sheep_mov
                self.sheep_right -= non_d_sheep_mov
                self.wolves_left += non_d_wolf_mov
                self.wolves_right -= non_d_wolf_mov
            self.states_history = new_his
            self.direction = not self.direction
            ####
            return default_tuple, valid_count
                #return mv, valid_count
        # if valid_count == 0:
        #     print("no valid move")
        #
        return default_tuple, valid_count

    def search_bfs(self, initial_sheep, initial_wolves):
        moves_list = []
        #
        self.total_players = initial_sheep + initial_wolves
        self.sheep_left = initial_sheep
        self.wolves_left = initial_wolves
        self.states_history[0, 0] = self.sheep_left
        self.states_history[0, 1] = self.sheep_right
        self.states_history[0, 2] = self.wolves_left
        self.states_history[0, 3] = self.wolves_right
        self.states_history[0, 4] = self.direction
        #print("direction?")
        #print(self.direction)
        #print("stop")
        #
        # depth = 0
        # if initial_sheep >= 10:
        #     depth = initial_wolves + initial_sheep + 5
        # else:
        #     depth = 10 * initial_sheep
        #
        # while (self.sheep_left + self.wolves_left > 0) and depth > 0:
        global_reset = 0
        #catch_reset = 0
        while self.sheep_left + self.wolves_left > 0:
            mov, validate = self.bfs()
            #if validate == 0 and global_reset < 900:
            if validate == 0:
                self.__init__()
                #print("here?")
                self.total_players = initial_sheep + initial_wolves
                self.sheep_left = initial_sheep
                self.wolves_left = initial_wolves
                self.states_history[0, 0] = self.sheep_left
                self.states_history[0, 1] = self.sheep_right
                self.states_history[0, 2] = self.wolves_left
                self.states_history[0, 3] = self.wolves_right
                self.states_history[0, 4] = self.direction
                global_reset += 1
                if global_reset < 899:
                    moves_list = []
            elif global_reset >= 900:
                return moves_list
            else:
                moves_list.append(mov)
                # if len(moves_list) > self.total_players * 100:
                #     print("len(moves_list)")
                #     print(len(moves_list))
                #     self.__init__()
                #     self.total_players = initial_sheep + initial_wolves
                #     self.sheep_left = initial_sheep
                #     self.wolves_left = initial_wolves
                #     self.states_history[0, 0] = self.sheep_left
                #     self.states_history[0, 1] = self.sheep_right
                #     self.states_history[0, 2] = self.wolves_left
                #     self.states_history[0, 3] = self.wolves_right
                #     self.states_history[0, 4] = self.direction
                #     moves_list = []
                #     global_reset += 1

                # print("real_solve")
                #print("moves_list solution\n", moves_list)
                #print("self.states_history")
                #print(self.states_history)
                # print("what is direction now? - ", self.direction)
                # print("stop here")
            # if self.terminal(self.states_history):
            #     return moves_list
        #print("moves_list solution\n", moves_list)
        #print("self.states_history")
        #print(self.states_history)
        #print("search bfs gets")
        #print(moves_list)
        return moves_list
