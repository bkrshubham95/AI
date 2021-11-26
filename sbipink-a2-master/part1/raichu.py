#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import random
from math import inf
def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def parse_map(board, N):
    board_str = board_to_string(board, N)
    return board_str.split("\n")

def locate_w_pichus(board_map):
    p_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == 'w']
    return p_coords

def locate_b_pichus(board_map):
    p_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == 'b']
    return p_coords

def locate_w_pikachus(board_map):
    p_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == 'W']
    return p_coords

def locate_b_pikachus(board_map):
    p_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == 'B']
    return p_coords

def locate_w_raichus(board_map):
    r_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == '@']
    return r_coords

def locate_b_raichus(board_map):
    r_coords = [(r,c) for r in range(0, len(board_map)) for c in range(0,len(board_map[0])) if board_map[r][c] == '$']
    return r_coords

def count_w_pichus(board_map):
    return sum([ row.count('w') for row in board_map ] )
def count_w_pikachus(board_map):
    return sum([ row.count('W') for row in board_map ] )
def count_w_raichus(board_map):
    return sum([ row.count('@') for row in board_map ] )
def count_b_pichus(board_map):
    return sum([ row.count('b') for row in board_map ] )
def count_b_pikachus(board_map):
    return sum([ row.count('B') for row in board_map ] )
def count_b_raichus(board_map):
    return sum([ row.count('$') for row in board_map ] )

def add_w_pichu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + 'w' + board_map[row][col+1:]] + board_map[row+1:]

def add_b_pichu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + 'b' + board_map[row][col+1:]] + board_map[row+1:]

def add_w_pikachu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + 'W' + board_map[row][col+1:]] + board_map[row+1:]

def add_b_pikachu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + 'B' + board_map[row][col+1:]] + board_map[row+1:]

def add_w_raichu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + '@' + board_map[row][col+1:]] + board_map[row+1:]

def add_b_raichu(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + '$' + board_map[row][col+1:]] + board_map[row+1:]

def make_empty(board_map, row, col):
    return board_map[0:row] + [board_map[row][0:col] + '.' + board_map[row][col + 1:]] + board_map[row + 1:]

def is_valid_coord(r, c, N):
    return (r >= 0 and r < N) and (c >=0 and c < N)
def moves(board_map, N, player):
    moves = []
    if player == 'w':
        p_coords = locate_w_pichus(board_map)
        pa_coords = locate_w_pikachus(board_map)
        r_coords = locate_w_raichus(board_map)
        for p in p_coords:
            try:
                r, c = p
                #check right diagonal

                if is_valid_coord(r+1, c+1, N):
                    if board_map[r+1][c+1]== '.':
                        #make_move
                        board_map = make_empty(board_map, r, c)
                        moves.append(add_w_pichu(board_map, r+1, c+1))
                        #unmake_move
                        board_map = add_w_pichu(board_map, r, c)
                        board_map = make_empty(board_map, r+1, c+1)
                    elif board_map[r+1][c+1] == 'b':
                        if is_valid_coord(r+2, c+2, N):
                            if board_map[r+2][c+2]=='.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r+1, c+1)
                                moves.append(add_w_pichu(board_map, r + 2, c + 2))
                                # unmake_move
                                board_map = add_w_pichu(board_map, r, c)
                                board_map = add_b_pichu(board_map, r + 1, c + 1)
                                board_map = make_empty(board_map, r + 2, c + 2)
                #check left diagonal
                if is_valid_coord(r + 1, c - 1, N):
                    if board_map[r+1][c-1] == '.':
                        # make_move
                        board_map = make_empty(board_map, r, c)
                        moves.append(add_w_pichu(board_map, r + 1, c - 1))
                        # unmake_move
                        board_map = add_w_pichu(board_map, r, c)
                        board_map = make_empty(board_map, r + 1, c - 1)
                    elif board_map[r+1][c-1]== 'b':
                        if is_valid_coord(r+2, c-2, N):
                            if board_map[r+2][c-2]=='.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r+1, c-1)
                                moves.append(add_w_pichu(board_map, r + 2, c - 2))
                                # unmake_move
                                board_map = add_w_pichu(board_map, r, c)
                                board_map = add_b_pichu(board_map, r + 1, c - 1)
                                board_map = make_empty(board_map, r + 2, c - 2)
            except:
                continue
        #Generate moves for white Pikachu
        for p in pa_coords:
            try:

                r, c = p
                for step in range(1,3):
                    #forward
                    if is_valid_coord(r+step,c, N):
                        if board_map[r+step][c] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_w_pikachu(board_map, r + step, c))
                            # unmake_move
                            board_map = add_w_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r + step, c)
                        elif board_map[r+step][c] =='b':
                            if board_map[r+step+1][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r + step, c)
                                moves.append(add_w_pikachu(board_map, r + step + 1, c))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pichu(board_map, r + step, c)
                                board_map = make_empty(board_map, r + step + 1, c)
                        elif board_map[r+step][c] =='B':
                            if board_map[r+step+1][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r + step, c)
                                moves.append(add_w_pikachu(board_map, r + step + 1, c))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pikachu(board_map, r + step, c)
                                board_map = make_empty(board_map, r + step + 1, c)
                    #right
                    if is_valid_coord(r,c-step, N):
                        if board_map[r][c-step] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_w_pikachu(board_map, r, c - step))
                            # unmake_move
                            board_map = add_w_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r, c - step)
                        elif board_map[r][c-step] =='b':
                            if board_map[r][c-step-1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c - step)
                                moves.append(add_w_pikachu(board_map, r, c - step - 1))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pichu(board_map, r, c - step)
                                board_map = make_empty(board_map, r, c - step - 1)
                        elif board_map[r][c-step] =='B':
                            if board_map[r][c-step-1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c-step)
                                moves.append(add_w_pikachu(board_map, r, c-step-1))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pikachu(board_map, r, c - step)
                                board_map = make_empty(board_map, r, c - step - 1)
                    #left
                    if is_valid_coord(r,c+step, N):
                        if board_map[r][c+step] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_w_pikachu(board_map, r, c + step))
                            # unmake_move
                            board_map = add_w_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r, c + step)
                        elif board_map[r][c+step] =='b':
                            if board_map[r][c+step+1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c + step)
                                moves.append(add_w_pikachu(board_map, r, c + step + 1))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pichu(board_map, r, c + step)
                                board_map = make_empty(board_map, r, c + step + 1)
                        elif board_map[r][c+step] =='B':
                            if board_map[r][c+step+1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c+step)
                                moves.append(add_w_pikachu(board_map, r, c+step+1))
                                # unmake_move
                                board_map = add_w_pikachu(board_map, r, c)
                                board_map = add_b_pikachu(board_map, r, c + step)
                                board_map = make_empty(board_map, r, c + step + 1)
            except:
                continue
        # Generate moves for white Raichu
        for p in r_coords:
            try:

                r, c = p
                r_orig, c_orig = r, c
                #backward
                r -= 1
                while(is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r-= 1
                        while(is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break

                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break
                    else:
                        break
                    r -= 1

                r, c = p
                r_orig, c_orig = r, c
                # forward
                r += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)
                            else:
                                break
                            r += 1
                        break


                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                        break
                    else:
                        break
                    r += 1
                r, c = p
                r_orig, c_orig = r, c
                # left
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break

                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break
                    else:
                        break
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # right
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break
                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break
                    else:
                        break
                    c -= 1
                r, c = p
                r_orig, c_orig = r, c
                # down left
                r -= 1
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break

                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break
                    else:
                        break
                    r -= 1
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # down right
                r -= 1
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    else:
                        break
                    r -= 1
                    c -= 1
                r, c = p
                r_orig, c_orig = r, c
                # up left
                r += 1
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break

                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break
                    else:
                        break
                    r += 1
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # up right
                r += 1
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_w_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_w_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'b':
                        r_b, c_b = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_b, c_b)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pichu(board_map, r_b, c_b)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    elif board_map[r][c] == 'B':
                        r_B, c_B = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_B, c_B)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_pikachu(board_map, r_B, c_B)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    elif board_map[r][c] == '$':
                        r_dollar, c_dollar = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_dollar, c_dollar)
                                moves.append(add_w_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_w_raichu(board_map, r_orig, c_orig)
                                board_map = add_b_raichu(board_map, r_dollar, c_dollar)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    else:
                        break
                    r += 1
                    c -= 1
            except:
                continue

    elif player=='b':
        p_coords = locate_b_pichus(board_map)
        pa_coords = locate_b_pikachus(board_map)
        r_coords = locate_b_raichus(board_map)
        for p in p_coords:
            try:
                r, c = p
                # check right diagonal
                if is_valid_coord(r - 1, c + 1, N):
                    if board_map[r - 1][c + 1] == '.':
                        # make_move
                        board_map = make_empty(board_map, r, c)
                        moves.append(add_b_pichu(board_map, r - 1, c + 1))
                        # unmake_move
                        board_map = add_b_pichu(board_map, r, c)
                        board_map = make_empty(board_map, r - 1, c + 1)
                    elif board_map[r - 1][c + 1] == 'w':
                        if is_valid_coord(r - 2, c + 2, N):
                            if board_map[r - 2][c + 2] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r - 1, c + 1)
                                moves.append(add_b_pichu(board_map, r - 2, c + 2))
                                # unmake_move
                                board_map = add_b_pichu(board_map, r, c)
                                board_map = add_w_pichu(board_map, r - 1, c + 1)
                                board_map = make_empty(board_map, r - 2, c + 2)
                # check left diagonal
                if is_valid_coord(r - 1, c - 1, N):
                    if board_map[r - 1][c - 1] == '.':
                        # make_move
                        board_map = make_empty(board_map, r, c)
                        moves.append(add_b_pichu(board_map, r - 1, c - 1))
                        # unmake_move
                        board_map = add_b_pichu(board_map, r, c)
                        board_map = make_empty(board_map, r - 1, c - 1)
                    elif board_map[r - 1][c - 1] == 'w':
                        if is_valid_coord(r - 2, c - 2, N):
                            if board_map[r - 2][c - 2] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r - 1, c - 1)
                                moves.append(add_b_pichu(board_map, r - 2, c - 2))
                                # unmake_move
                                board_map = add_b_pichu(board_map, r, c)
                                board_map = add_w_pichu(board_map, r - 1, c - 1)
                                board_map = make_empty(board_map, r - 2, c - 2)
            except:
                continue
        # Generate moves for black Pikachu
        for p in pa_coords:
            try:
                r, c = p
                for step in range(1, 3):
                    # forward
                    if is_valid_coord(r - step, c, N):
                        if board_map[r - step][c] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_b_pikachu(board_map, r - step, c))
                            # unmake_move
                            board_map = add_b_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r - step, c)
                        elif board_map[r - step][c] == 'w':
                            if board_map[r - step - 1][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r - step, c)
                                moves.append(add_b_pikachu(board_map, r - step - 1, c))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pichu(board_map, r - step, c)
                                board_map = make_empty(board_map, r - step - 1, c)
                        elif board_map[r - step][c] == 'W':
                            if board_map[r - step - 1][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r - step, c)
                                moves.append(add_b_pikachu(board_map, r - step - 1, c))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pikachu(board_map, r - step, c)
                                board_map = make_empty(board_map, r - step - 1, c)
                    # right
                    if is_valid_coord(r, c + step, N):
                        if board_map[r][c + step] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_b_pikachu(board_map, r, c + step))
                            # unmake_move
                            board_map = add_b_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r, c + step)
                        elif board_map[r][c + step] == 'w':
                            if board_map[r][c + step + 1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c + step)
                                moves.append(add_b_pikachu(board_map, r, c + step + 1))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pichu(board_map, r, c + step)
                                board_map = make_empty(board_map, r, c + step + 1)
                        elif board_map[r][c + step] == 'W':
                            if board_map[r][c + step + 1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c + step)
                                moves.append(add_b_pikachu(board_map, r, c + step + 1))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pikachu(board_map, r, c + step)
                                board_map = make_empty(board_map, r, c + step + 1)
                    # left
                    if is_valid_coord(r, c - step, N):
                        if board_map[r][c - step] == '.':
                            # make_move
                            board_map = make_empty(board_map, r, c)
                            moves.append(add_b_pikachu(board_map, r, c - step))
                            # unmake_move
                            board_map = add_b_pikachu(board_map, r, c)
                            board_map = make_empty(board_map, r, c - step)
                        elif board_map[r][c - step] == 'w':
                            if board_map[r][c - step - 1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c - step)
                                moves.append(add_b_pikachu(board_map, r, c - step - 1))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pichu(board_map, r, c - step)
                                board_map = make_empty(board_map, r, c - step - 1)
                        elif board_map[r][c - step] == 'W':
                            if board_map[r][c - step - 1] == '.':
                                # make_move
                                board_map = make_empty(board_map, r, c)
                                board_map = make_empty(board_map, r, c - step)
                                moves.append(add_b_pikachu(board_map, r, c - step - 1))
                                # unmake_move
                                board_map = add_b_pikachu(board_map, r, c)
                                board_map = add_w_pikachu(board_map, r, c - step)
                                board_map = make_empty(board_map, r, c - step - 1)
            except:
                continue
        for p in r_coords:
            try:

                r, c = p
                r_orig, c_orig = r, c
                #forward
                r -= 1
                while(is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r-= 1
                        while(is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                        break
                    else:
                        break
                    r -= 1
                r, c = p
                r_orig, c_orig = r, c
                # backward
                r += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                        break
                    else:
                        break
                    r += 1
                r, c = p
                r_orig, c_orig = r, c
                # right
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c += 1
                        break
                    else:
                        break
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # left
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break

                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            c -= 1
                        break
                    else:
                        break
                    c -= 1
                r, c = p
                r_orig, c_orig = r, c
                # upper right
                r -= 1
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break

                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r -= 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c += 1
                        break
                    else:
                        break
                    r -= 1
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # upper left
                r -= 1
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r -= 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r -= 1
                            c -= 1
                        break
                    else:
                        break
                    r -= 1
                    c -= 1
                r, c = p
                r_orig, c_orig = r, c
                # down right
                r += 1
                c += 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r += 1
                        c += 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c += 1
                        break
                    else:
                        break
                    r += 1
                    c += 1
                r, c = p
                r_orig, c_orig = r, c
                # down left
                r += 1
                c -= 1
                while (is_valid_coord(r, c, N)):
                    if board_map[r][c] == '.':
                        # make_move
                        board_map = make_empty(board_map, r_orig, c_orig)
                        moves.append(add_b_raichu(board_map, r, c))
                        # unmake_move
                        board_map = add_b_raichu(board_map, r_orig, c_orig)
                        board_map = make_empty(board_map, r, c)

                    elif board_map[r][c] == 'w':
                        r_w, c_w = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_w, c_w)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pichu(board_map, r_w, c_w)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    elif board_map[r][c] == 'W':
                        r_W, c_W = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_W, c_W)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_pikachu(board_map, r_W, c_W)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    elif board_map[r][c] == '@':
                        r_at, c_at = r, c
                        r += 1
                        c -= 1
                        while (is_valid_coord(r, c, N)):
                            if board_map[r][c] == '.':
                                # make_move
                                board_map = make_empty(board_map, r_orig, c_orig)
                                board_map = make_empty(board_map, r_at, c_at)
                                moves.append(add_b_raichu(board_map, r, c))
                                # unmake_move
                                board_map = add_b_raichu(board_map, r_orig, c_orig)
                                board_map = add_w_raichu(board_map, r_at, c_at)
                                board_map = make_empty(board_map, r, c)

                            else:
                                break
                            r += 1
                            c -= 1
                        break
                    else:
                        break
                    r += 1
                    c -= 1
            except:
                continue
    return moves

def get_heuristic(board_map, maximizing_color):
    if maximizing_color == 'w':
        return get_white_score(board_map) - get_black_score(board_map)
    elif maximizing_color== 'b':
        return get_black_score(board_map) - get_white_score(board_map)

def get_white_score(board_map):
    return 1 * count_w_pichus(board_map) + 3 * count_w_pikachus(board_map) + 5 * count_w_raichus(board_map)

def get_black_score(board_map):
    return 1 * count_b_pichus(board_map) + 3 * count_b_pikachus(board_map) + 5 * count_b_raichus(board_map)

def minimax(board_map, depth, alpha, beta, maximizing_player, maximizing_color):

    if depth==0:
        return None, get_heuristic(board_map, maximizing_color)

    succ_boards = moves(board_map, N, maximizing_color)
    for i, board in enumerate(succ_boards):
        if maximizing_color == 'w':
           p_coords = locate_w_pichus(board)
           pa_coords = locate_w_pikachus(board)

           for p in p_coords:
               if p[0] == (N -1):
                succ_boards[i] = add_w_raichu(board, p[0], p[1])
           for p in pa_coords:
               if p[0] == (N -1):
                succ_boards[i] = add_w_raichu(board, p[0], p[1])
        elif maximizing_color == 'b':
            p_coords = locate_b_pichus(board)
            pa_coords = locate_b_pikachus(board)

            for p in p_coords:
                if p[0] == 0:
                    succ_boards[i] = add_b_raichu(board, p[0], p[1])
            for p in pa_coords:
                if p[0] == 0:
                    succ_boards[i] = add_b_raichu(board, p[0], p[1])
    best_board = random.choice(succ_boards)

    if maximizing_player:
        max_eval = -inf
        for board in succ_boards:
            current_eval = minimax(board, depth-1, alpha, beta, False, maximizing_color)[1]

            if current_eval > max_eval:
                max_eval = current_eval
                best_board = board
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break
        return best_board, max_eval
    else:
        min_eval = inf
        for board in succ_boards:
            current_eval = minimax(board, depth-1, alpha, beta, True, maximizing_color)[1]
            if current_eval < min_eval:
                min_eval = current_eval
                best_board = board
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        return best_board, min_eval
def find_best_move(board, N, player, timelimit):
    board_map = parse_map(board, N)
    # for move in moves(board_map, N, player):
    #     print(move)
    # print(get_heuristic(board_map, player))
    yield ''.join(minimax(board_map, 3, inf, -inf, True, player)[0])
    # while True:
    #     time.sleep(1)
    #     yield board


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")

    (_, N, player, board, timelimit) = sys.argv
    N = int(N)
    timelimit = int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N * N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)