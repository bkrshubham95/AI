# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
import time
import sys
import copy
from math import ceil, inf
from statistics import mean


class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands = {"b": quintris.left, "h": quintris.hflip,
                        "n": quintris.rotate, "m": quintris.right, " ": quintris.down}
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#


class ComputerPlayer:
    # This function should generate a series of commands to move the piece
    # into the "optimal"
    # position. The commands are a string of letters, where b and m represent
    # left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board,
    # e.g.:
    #   - quintris.col, quintris.row have the current column and row of the
    # upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece()
    # is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and
    # quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a
    # list of strings.
    #
    def get_moves(self, quintris):
        # super simple current algorithm: just randomly move left, right, and
        # rotate a few times
        fringe, visited = self.succ(quintris)
        new_fringe = self.prune_fringe(ceil(0.5*len(fringe)), fringe)
        if new_fringe:
            return self.next_succ(quintris, new_fringe)
        else:
            return ''

    # This is the version that's used by the animted version. This is really
    # similar to get_moves,
    # except that it runs as a separate thread and you should access various
    # methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the
    # upper-left corner of the
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece()
    # is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(),
    # and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a
    # list of strings.
    #

    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full
        # column

        while 1:
            fringe, visited = self.succ(quintris)
            new_fringe = self.prune_fringe(ceil(0.2*len(fringe)), fringe)
            if fringe:
                for c in self.next_succ(quintris, new_fringe):
                    if c == 'h':
                        quintris.hflip()
                    elif c == 'n':
                        quintris.rotate()
                    elif c == 'm':
                        quintris.right()
                    elif c == 'b':
                        quintris.left()
                quintris.down()
            else:
                quintris.down()

    def combine(str1, str2):
        return "".join(
            [c if c != " " else str2[i] for (i, c) in enumerate(str1)])
    # Determine all possible states given a specific board and piece

    def succ(self, quintris):
        board_width = quintris.BOARD_WIDTH
        current_piece, current_row, current_col = quintris.get_piece()
        fringe = []
        h_flip = 2
        rotate = 4
        visited = {}
        for col in range(board_width+len(current_piece)):
            lefts = rights = 0
            if current_col-col > 0:
                lefts = current_col-col
                rights = 0
            elif current_col-col < 0:
                lefts = 0
                rights = col-current_col
            for j in range(rotate):
                for i in range(h_flip):
                    quintris2 = copy.deepcopy(quintris)
                    move = '' + 'h'*i + 'n'*j + 'm'*rights + 'b'*lefts
                    try:
                        for _ in range(i):
                            quintris2.move(0, quintris2.hflip_piece(quintris2.piece))
                        for _ in range(j):
                            quintris2.move(0, quintris2.rotate_piece(quintris2.piece, 90))
                        for _ in range(rights):
                            quintris2.move(1, quintris2.piece)
                        for _ in range(lefts):
                            quintris2.move(-1, quintris2.piece)
                        quintris2.down()
                    except EndOfGame:
                        continue
                    cost = self.cost(quintris, quintris2)
                    if quintris2.get_board() in visited.values():
                        pass
                    else:
                        visited.update(
                            {move: [cost, quintris2.get_board()]})
                        fringe.append([move, cost])
        return fringe, visited

    # level-2 search

    def next_succ(self, quintris, fringe):
        min_cost = inf
        min_path = ''
        for i in range(len(fringe)):
            quintris3 = copy.deepcopy(quintris)
            try:
                for c in fringe[i][0]:
                    if c == 'h':
                        quintris3.move(0, quintris3.hflip_piece(quintris3.piece))
                    elif c == 'n':
                        quintris3.move(0, quintris3.rotate_piece(quintris3.piece, 90))
                    elif c == 'm':
                        quintris3.move(1, quintris3.piece)
                    elif c == 'b':
                        quintris3.move(-1, quintris3.piece)
                quintris3.down()
            except EndOfGame:
                continue
            temp_fringe, temp_visited = self.succ(quintris3)
            # new_temp_fringe = self.prune_fringe(ceil(0.05*len(temp_fringe)),
            #                                     temp_fringe)
            # for k in range(len(new_temp_fringe)):
            #     quintris4 = copy.deepcopy(quintris)
            #     try:
            #         for c in new_temp_fringe[k][0]:
            #             if c == 'h':
            #                 quintris4.move(0, quintris3.hflip_piece(quintris4.piece))
            #             elif c == 'n':
            #                 quintris4.move(0, quintris4.rotate_piece(quintris4.piece, 90))
            #             elif c == 'm':
            #                 quintris4.move(1, quintris4.piece)
            #             elif c == 'b':
            #                 quintris4.move(-1, quintris4.piece)
            #         quintris4.down()
            #     except EndOfGame:
            #         continue
            #     new_temp_fringe[k][1] += self.chance(quintris4)
            # for j in range(len(new_temp_fringe)):
            #     min_cost = min(min_cost, fringe[i][1]+new_temp_fringe[j][1])
            # for j in range(len(new_temp_fringe)):
            #     if fringe[i][1]+new_temp_fringe[j][1] <= min_cost:
            #         min_path = fringe[i][0]
            for j in range(len(temp_fringe)):
                min_cost = min(min_cost, fringe[i][1]+temp_fringe[j][1])
            for j in range(len(temp_fringe)):
                if fringe[i][1]+temp_fringe[j][1] <= min_cost:
                    min_path = fringe[i][0]
        return min_path

    # Chance Layer

    def chance(self, quintris):
        cost = [0*n for n in range(len(quintris.PIECES))]
        for i in range(len(quintris.PIECES)):
            min_cost = inf
            current_piece = quintris.PIECES[i]
            board_width = quintris.BOARD_WIDTH
            h_flip = 2
            rotate = 4
            visited = {}
            for col in range(board_width+len(current_piece)):
                lefts = 0
                rights = col
                for j in range(rotate):
                    for i in range(h_flip):
                        quintris5 = copy.deepcopy(quintris)
                        move = '' + 'h'*i + 'n'*j + 'm'*rights + 'b'*lefts
                        try:
                            for _ in range(i):
                                quintris5.move(0, quintris5.hflip_piece(current_piece))
                            for _ in range(j):
                                quintris5.move(0, quintris5.rotate_piece(current_piece, 90))
                            for _ in range(rights):
                                quintris5.move(1, current_piece)
                            for _ in range(lefts):
                                quintris5.move(-1, current_piece)
                            quintris5.down()
                        except EndOfGame:
                            continue
                        if quintris5.get_board() in visited.values():
                            pass
                        else:
                            visited.update(
                                {move: quintris5.get_board()})
                            cost[i] += self.cost(quintris, quintris5)
                if visited:
                    cost[i] = min_cost
                else:
                    cost[i] = inf
        return mean(cost)

    # Evaluation function
    # TODO: Count blocks above holes
    # TODO: Holes should have high weightage initially

    def cost(self, quintris, quintris2):
        new_board = quintris2.get_board()
        holes, max_height, empty_space, wells, blocks = \
            self.cost_params(new_board)
        line_clear = self.line_clear(quintris.state, quintris2.state)

        board_height = quintris.BOARD_HEIGHT
        if max_height == board_height:
            return 99999
        # return int(3*(holes+1) + max_height**1.5 + empty_space -
        #            line_clear + 3*wells)
        # return int(2*holes + max_height**1.5 + empty_space - line_clear + 3*wells)
        return int(2*(holes+1) + max_height**1.5 + 0*empty_space -
                   line_clear + 2*wells)

    def cost_params(self, board):
        new_board = copy.deepcopy(board)
        new_board.append('x'*len(new_board[0]))

        # compute holes
        b_holes = [''.join(s) for s in zip(*new_board)]
        for i in range(len(b_holes)):
            b_holes[i] = b_holes[i].strip()
        holes = sum(s.count(' ') for s in b_holes)

        # compute max_height
        b_max_height = [''.join(s) for s in zip(*new_board)]
        for i in range(len(b_max_height)):
            b_max_height[i] = b_max_height[i].lstrip()
        max_height = max(len(s) for s in b_max_height)

        # compute min_height
        b_min_height = [''.join(s) for s in zip(*new_board)]
        for i in range(len(b_min_height)):
            b_min_height[i] = b_min_height[i].lstrip()
        min_height = min(len(s) for s in b_min_height)

        # compute empty_space
        b_empty_space = [''.join(s) for s in zip(*new_board)]
        for i in range(len(b_empty_space)):
            b_empty_space[i] = b_empty_space[i].lstrip()
        empty_space = sum((max(len(s) for s in b_empty_space)-s.count('x'))
                          for s in b_empty_space)

        # compute wells
        b_wells = [''.join(s) for s in zip(*new_board)]
        wells = 0
        for r in range(len(b_wells)-1):
            for c in range(len(b_wells[0])):
                if b_wells[r][c] != b_wells[r+1][c] and b_wells[r][c] == ' ':
                    wells += 1
        for r in range(len(b_wells)-2):
            for c in range(len(b_wells[0])):
                if b_wells[r][c] == b_wells[r+1][c] and b_wells[r][c] != b_wells[r+2][c] and b_wells[r][c] == ' ':
                    wells += 2
        for c in range(len(b_wells[-1])):
            if b_wells[-1][c] != b_wells[-2][c] and b_wells[-1][c] == ' ':
                wells += 1

        # compute number of blocks
        blocks = sum(s.count('x') for s in board)
        return holes, max_height-min_height, empty_space, wells, blocks

    def line_clear(self, old_state, new_state):
        if new_state[1]-old_state[1] == 0:
            return 0
        else:
            # print('clear possible! ', end='')
            # return 2**(new_state[1]-old_state[1]+5)
            return 99

    def prune_fringe(self, n, l1):
        pruned_fringe = []
        for i in range(len(l1)):
            pruned_fringe.append([l1[i][1], l1[i][0]])
        pruned_fringe.sort()
        for i in range(len(l1)):
            pruned_fringe[i] = [pruned_fringe[i][1], pruned_fringe[i][0]]
        return pruned_fringe[:n]


###################
# main program


(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)
