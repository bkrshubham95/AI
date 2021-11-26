#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Shubham Bipin Kumar / sbipink@iu.edu]
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    p_coords = locate_pichus(house_map)
    return [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0, len(house_map[0])) if (
                house_map[r][c] == '.' and is_valid_col(house_map, p_coords, (r, c)) and is_valid_row(house_map,
                                                                                                      p_coords, (r,
                                                                                                                 c)) and is_valid_diag(
            house_map, p_coords, (r, c)))]
# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k 

#Get current location of the Pichu
def get_pichu_location(house_map):
    pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                 house_map[row_i][col_i] == "p"][0]


def locate_pichus(house_map):
    p_coords = [(r, c) for r in range(0, len(house_map)) for c in range(0, len(house_map[0])) if house_map[r][c] == 'p']
    return p_coords


def is_valid_row(house_map, p_coords, p_add):
    p_row_coords = [p[0] for p in p_coords]
    # for p_index, p_r in enumerate(p_row_coords):
    #     if p_r in (p_row_coords[0:p_index] + p_row_coords[p_index+1:]):
    #         #checking if there is no wall between them
    #         li_r = locate_pichus(house_map[p_r][:])
    #         _, c1 = li_r[0]
    #         _, c2 = li_r[1]
    #         # for j in range(c1+1, c2):
    #         #     if (house_map[p_r][j] != 'X' or house_map[p_r][j] != "@"):
    #         #         return False
    #         if ('X' not in house_map[p_r][c1+1:c2]) and ('@' not in house_map[p_r][c1+1:c2]):
    #             return False
    # return True
    # print(p_row_coords)
    if p_add[0] in p_row_coords:
        # There are 2 pichus in the same row
        # Getting the coordinates of both pichus
        check_in = house_map[p_add[0]]
        li_c = locate_pichus(check_in)
        for p_col in li_c:
            c, _ = p_col
            min_c = min(c, p_add[1])
            max_c = max(c, p_add[1])
            if ('X' not in check_in[min_c + 1:max_c]) and ('@' not in check_in[min_c + 1:max_c]):
                return False
    return True


def is_valid_col(house_map, p_coords, p_add):
    p_col_coords = [p[1] for p in p_coords]

    if p_add[1] in p_col_coords:
        # There are 2 pichus in the same column
        # Getting the coordinates of both pichus
        check_in = [row[p_add[1]] for row in house_map]
        li_c = locate_pichus(check_in)
        for p_col in li_c:
            r, _ = p_col
            min_r = min(r, p_add[0])
            max_r = max(r, p_add[0])
            if ('X' not in check_in[min_r + 1:max_r]) and ('@' not in check_in[min_r + 1:max_r]):
                return False
    return True


def is_valid_diag(house_map, p_coords, p_add):
    count = 0
    # print(p)
    row, col = p_add[0], p_add[1]
    # checking for left diagonal
    min_dis_from_axes = min(row, col)
    i = row - min_dis_from_axes
    j = col - min_dis_from_axes
    coord_list = []
    # marking all pichu coordinates in the left diagonal
    while (i < len(house_map) and j < len(house_map[0])):
        if house_map[i][j] == 'p':
            count += 1
            coord_list.append((i, j))
        i += 1
        j += 1
    if len(coord_list) >= 1:
        for p_col in coord_list:
            row1, col1 = p_col
            row2, col2 = p_add[0], p_add[1]
            if row1 < row2:
                row1 += 1
                col1 += 1
                wall_present = False
                while (row1 < row2 and col1 < col2):
                    if (house_map[row1][col1] == 'X' or house_map[row1][col1] == "@"):
                        wall_present = True
                    row1 += 1
                    col1 += 1
                if not wall_present:
                    return False
            else:
                row2 += 1
                col2 += 1
                wall_present = False
                while (row2 < row1 and col2 < col1):
                    if (house_map[row2][col2] == 'X' or house_map[row2][col2] == "@"):
                        wall_present = True
                    row2 += 1
                    col2 += 1
                if not wall_present:
                    return False
                    # else:
                #     break
    # checking for right diagonal
    count = 0
    max_steps = min(len(house_map) - row - 1, col)
    i = row + max_steps
    j = col - max_steps
    coord_list = []
    while (i >= 0 and j < len(house_map[0])):
        if house_map[i][j] == 'p':
            count += 1
            coord_list.append((i, j))
        i -= 1
        j += 1
    if len(coord_list) >= 1:
        for p_col in coord_list:
            row1, col1 = p_col
            row2, col2 = p_add[0], p_add[1]
            if row1 > row2:
                row1 -= 1
                col1 += 1
                wall_present = False
                while (row1 > row2 and col1 < col2):
                    if (house_map[row1][col1] == 'X' or house_map[row1][col1] == "@"):
                        wall_present = True
                    row1 -= 1
                    col1 += 1
                if not wall_present:
                    return False
                # else:
                #     break
            else:
                row2 -= 1
                col2 += 1
                wall_present = False
                while (row2 > row1 and col2 < col1):
                    if (house_map[row2][col2] == 'X' or house_map[row2][col2] == "@"):
                        wall_present = True
                    row2 -= 1
                    col2 += 1
                if not wall_present:
                    return False
                # else:
                #     break
    return True

# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.



def solve(initial_house_map,k):
    fringe = [initial_house_map]
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            fringe.append(new_house_map)
    return ([], False)
# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


