# solver2021#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Shubham Bipin Kumar 
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
import copy
import heapq
import time

ROWS=5
COLS=5

class State():
    def __init__(self, parent_state=None, curr_state=None):
        self.parent = parent_state
        self.state = curr_state

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def printable_board(board):
    return [ ('%3d ')*5  % board[j:(j+5)] for j in range(0, 5*5, 5) ]

def move_right(board, row):
  """Move the given row to one position right"""
#   print(board)
#   print(row)
  board[row] = board[row][-1:] + board[row][:-1]
  return board

def move_left(board, row):
  """Move the given row to one position left"""
  board[row] = board[row][1:] + board[row][:1]
  return board

def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def move_clockwise(board):
    """Move the outer ring clockwise"""
    board[0]=[board[1][0]]+board[0]
    residual=board[0].pop()
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,0,residual)
    board=transpose_board(board)
    return board

def move_cclockwise(board):
    """Move the outer ring counter-clockwise"""
    board[0]=board[0]+[board[1][-1]]
    residual=board[0].pop(0)
    board=transpose_board(board)
    residual=rotate_right(board,0,residual)
    board=transpose_board(board)
    residual=rotate_right(board,-1,residual)
    board=transpose_board(board)
    residual=rotate_left(board,-1,residual)
    board=transpose_board(board)
    return board

def transpose_board(board):
  """Transpose the board --> change row to column"""
  return [list(col) for col in zip(*board)]
# reference from the test file given for state change
def new_state(state, move):
    if set(move).intersection(set(['U','D','R','L'])):
        move,index=move
        index=int(index)-1
    if move == "R":
        state = move_right(state, index)
    elif move == "L":
        state = move_left(state, index)
    elif move == "U":
        state = transpose_board(move_left(transpose_board(state), index))
    elif move == "D":
        state = transpose_board(move_right(transpose_board(state), index))
    elif move == 'Oc':
        state = move_clockwise(state)
    elif move == 'Occ':
        state = move_cclockwise(state)
    elif move == 'Ic':
        state=np.array(state)
        inner_board=state[1:-1,1:-1].tolist()
        inner_board = move_clockwise(inner_board)
        state[1:-1,1:-1]=np.array(inner_board)
        state=state.tolist()
    elif move == 'Icc':
        state=np.array(state)
        inner_board=state[1:-1,1:-1].tolist()
        inner_board = move_cclockwise(inner_board)
        state[1:-1,1:-1]=np.array(inner_board)
        state=state.tolist()
    return state
    
def heuristic(new_board):
    state_heuristic = 0 
    num_of_rows = len(new_board)
    num_of_col = len(new_board[0])
    for r in range(0, num_of_rows):
        for c in range(0, num_of_col):
            # print(new_board[r][c])
            dest_row = new_board[r][c]/5
            if dest_row ==1 or dest_row ==2 or dest_row == 3 or dest_row == 4 or dest_row ==5:
                dest_row = dest_row-1
            else:
                dest_row = int(dest_row)
            dest_col = new_board[r][c]%5
            if dest_col == 0:
                dest_col = 4
            else:
                dest_col = dest_col - 1
            state_heuristic = state_heuristic + abs(dest_row - r) + abs(dest_col - c)

    # print("state heuristic")
    # print(state_heuristic)
    return state_heuristic

# return a list of possible successor states and move for the successor
def successors(state):
    valid_succ = []
    # for all valid successors possible with given moves :
    # calculate cost+heuristic(distance if each cell from where it should be)
    # append the one with least cost in valid_succ
    valid_moves_set=['R1','R2','R3','R4','R5','L1','L2','L3','L4','L5','U1','U2','U3','U4','U5','D1','D2','D3','D4','D5','Oc','Ic','Occ','Icc']
    for possible_move in valid_moves_set:
        state_copy = copy.deepcopy(state)
        _state = new_state(state_copy, possible_move)
        _state_tuple = (_state, possible_move)
        valid_succ.append(_state_tuple)
        # print("State:")
        # print(_state_tuple)
    return valid_succ

# check if we've reached the goal
def is_goal(state):
    goal_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]  
    if state == goal_state:
        return True
    else:
        return False

def convert_to_tuple(board):
    board_cell_list = []
    for i in range(5):
        for j in range(5):
            board_cell_list.append(board[i][j])
    return tuple(board_cell_list)


def solve(board_tuple):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # initial_board = []
    initial_board = np.array(board_tuple).reshape(5, 5).tolist()
#     print(initial_board)
    path = []
    heap = []
    cost = 0
    f_n = 0
    fringe = (f_n, initial_board, [])
    moves = []
    heapq.heappush(heap, fringe)
    visited = []
    while heap:
        # print("Solving for the Fringe or Taken Move: ")
        # print(heapq.heappop(heap)[1])
        f_n, board_state, move = heapq.heappop(heap)
#         print("moves")
#         print(move)
        # if f_n != 0:
        #     print(move)
        #     path.append(str(move))
        # print("Board state: \n" +"\n".join(printable_board(convert_to_tuple(board_state))))
        
        visited.append(board_state)
        if is_goal(board_state):
                return move
        cost = cost+1
        for succ in successors(board_state):
            if succ[0] in visited:
                continue
            h_succ = heuristic(succ[0])
            f_succ = cost + h_succ
            # if succ in [e[1] for e in heap]:
                # if f_succ < heap's f_succ; push with lesser f_succ
            updated_path = move + [succ[1]]
            succ_fringe = (f_succ, succ[0], updated_path)
            heapq.heappush(heap, succ_fringe)

# Please don't modify anything below this line
# ##############################change before pushing######################
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
#     start = time.time()
    route = solve(tuple(start_state))
#     time_taken = time.time()-start
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
#     print(time_taken)
