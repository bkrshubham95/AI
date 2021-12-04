#!/usr/local/bin/python3
#
# Authors: [shubham bipin kumar abhinav sinha himanshu hansaria]
#
# Ice layer finder
# Based on skeleton code by D. Crandall, November 2021
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
import numpy as np


# calculate "Edge strength map" of an image
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale, 0, filtered_y)
    return sqrt(filtered_y ** 2)


# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_boundary(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range(int(max(y - int(thickness / 2), 0)), int(min(y + int(thickness / 2), image.size[1] - 1))):
            image.putpixel((x, t), color)
    return image


def draw_asterisk(image, pt, color, thickness):
    for (x, y) in [(pt[0] + dx, pt[1] + dy) for dx in range(-3, 4) for dy in range(-2, 3) if
                   dx == 0 or dy == 0 or abs(dx) == abs(dy)]:
        if 0 <= x < image.size[0] and 0 <= y < image.size[1]:
            image.putpixel((x, y), color)
    return image


# Save an image that superimposes three lines (simple, hmm, feedback) in three different colors
# (yellow, blue, red) to the filename
def write_output_image(filename, image, simple, hmm, feedback, feedback_pt):
    new_image = image.copy()
    new_image = draw_boundary(new_image, simple, (255, 255, 0), 2)
    new_image = draw_boundary(new_image, hmm, (0, 0, 255), 2)
    new_image = draw_boundary(new_image, feedback, (255, 0, 0), 2)
    new_image = draw_asterisk(new_image, feedback_pt, (255, 0, 0), 2)
    imageio.imwrite(filename, new_image)


def back_tracking(p_state, no_of_column, viterbi_array, back_tracking_pointer):
    #backtracking to find the maximum value
    max_index = argmax(p_state[:, no_of_column - 1])
    for col in range(no_of_column - 1, -1, -1):
        viterbi_array[col] = int(max_index)
        max_index = back_tracking_pointer[int(max_index)][col]
    return viterbi_array


def reccurence_check_viterbi(col_param, row_param, col_size, row_size, p_state, back_tracking_pointer, edge_strength_val,transition_offset):
    #initializing the row and column values
    r_initial, r_stop, step_row = row_param
    c_initial, c_final, step_col = col_param

    for col in range(c_initial, c_final, step_col):
        for row in range(r_initial, r_stop, step_row):
            p_maximum = 0
            for j in range(-4, 5):
                if (row + j < row_size) and (row + j >= 0):
                    if p_maximum < p_state[row + j][col - 1] * transition_offset[abs(j)]:
                        p_maximum = p_state[row + j][col - 1] * transition_offset[abs(j)]
                        back_tracking_pointer[row][col] = row + j
                    p_state[row][col] = (edge_strength_val[row][col] / 100) * p_maximum

    return p_state, back_tracking_pointer


def hmm_calculation(edge_strength_val, p_transition):
    no_of_rows = edge_strength_val.shape[0]
    no_of_col = edge_strength_val.shape[1]

    viterbi_array = zeros(no_of_col)
    col_sums = zeros(no_of_col)
    p_state = zeros((no_of_rows, no_of_col))
    back_tracking_pointer = zeros((no_of_rows, no_of_col))

    for col in range(no_of_col):
        for row in range(no_of_rows):
            col_sums[col] += edge_strength_val[row][col]
    s = sum(col_sums)
    # initial  probab
    for row in range(no_of_rows):
        p_state[row][0] = edge_strength_val[row][0] / s

    t1 = (1, no_of_col, 1)
    t2 = (0, no_of_rows, 1)
    p_state, back_tracking_pointer = reccurence_check_viterbi(t1, t2, no_of_col, no_of_rows,p_state,back_tracking_pointer,edge_strength_val,p_transition)
    viterbi_array = back_tracking(p_state, no_of_col, viterbi_array, back_tracking_pointer)

    return viterbi_array, p_state, back_tracking_pointer



# main program
#
if __name__ == "__main__":

    if len(sys.argv) != 6:
        raise Exception(
            "Program needs 5 parameters: input_file airice_row_coord airice_col_coord icerock_row_coord icerock_col_coord")

    input_filename = sys.argv[1]
    gt_airice = [int(i) for i in sys.argv[2:4]]
    gt_icerock = [int(i) for i in sys.argv[4:6]]

    # loading the  image
    input_image = Image.open(input_filename).convert('RGB')
    image_array = array(input_image.convert('L'))

    # compute edge strength mask -- in case it's helpful. Feel free to use this.
    edge_strength_val = edge_strength(input_image)
    imageio.imwrite('edges.png', uint8(255 * edge_strength_val / (amax(edge_strength_val))))

    no_of_column = edge_strength_val.shape[1]
    #print("col_size",no_of_column)
    no_of_row = edge_strength_val.shape[0]
    #print("row_size",no_of_row)

    #airice_simple = [argmax(edge_strength_val[:, i]) for i in range(edge_strength_val.shape[1])]
    airice_simple = argmax(edge_strength_val, axis=0)
    #print("airice_simple ", airice_simple)
    edge_strength_list = edge_strength_val.tolist()
    #print("edge_strength_list",edge_strength_list)

    icerock_simple = []
    for idx, row in enumerate(airice_simple):
        i = 0
        r = []
        while i < 10:
            edge_strength_list[row - i][idx] = -1
            i += 1

    #print(edge_strength_list)

    icerock_simple = argmax(edge_strength_list, axis=0)
    #print("icerock_simple ", icerock_simple)
    edge_strength_val = edge_strength(input_image)
    p_transition_offset = [0.5, 0.4, 0.1, 0.05, 0.01,0.005,0.0005]
    airice_hmm, airice_p_state, airice_back_pointer = hmm_calculation(edge_strength_val, p_transition_offset)
    #print("air ice hmm ",airice_hmm)

    for row in range(no_of_row):
        airice_p_state[row][gt_airice[0]] = 0
    airice_p_state[gt_airice[1]][gt_airice[0]] = 1

    # update forward
    p_state, airice_back_pointer = reccurence_check_viterbi((gt_airice[0] - 1, 0, -1),(gt_airice[1] - 1, -1, -1),no_of_column, no_of_row,airice_p_state,airice_back_pointer,edge_strength_val,p_transition_offset)
    # update backward
    p_state, airice_back_pointer = reccurence_check_viterbi((gt_airice[0] + 1, no_of_column, 1),(0, no_of_row, 1),no_of_column, no_of_row,airice_p_state,airice_back_pointer,edge_strength_val,p_transition_offset)
    airice_feedback = back_tracking(p_state, no_of_column, airice_hmm, airice_back_pointer)
    #print("airice_feedback ", airice_feedback)

    for index, y_coord in enumerate(airice_hmm):
        i = 0
        while i < 12:
            edge_strength_val[int(y_coord) - i][index] = 0
            edge_strength_val[int(y_coord) + i][index] = 0
            i += 1

    icerock_hmm, icerock_p_state, icerock_back_pointer = hmm_calculation(edge_strength_val, p_transition_offset)
    #print("ice rock hmm ",icerock_hmm)

    for row in range(no_of_row):
        icerock_p_state[row][gt_icerock[0]] = 0
    icerock_p_state[gt_icerock[1]][gt_icerock[0]] = 1
    # update forward
    icerock_p_state, icerock_back_pointer = reccurence_check_viterbi((gt_icerock[0] - 1, 0, -1),(gt_icerock[1] - 1, -1, -1),no_of_column, no_of_row,icerock_p_state,icerock_back_pointer,edge_strength_val,p_transition_offset)
    # update backward
    icerock_p_state, icerock_back_pointer = reccurence_check_viterbi((gt_icerock[0] + 1, no_of_column, 1),(0, no_of_row, 1),no_of_column, no_of_row,icerock_p_state,icerock_back_pointer,edge_strength_val,p_transition_offset)
    icerock_feedback = back_tracking(icerock_p_state, no_of_column, icerock_hmm, icerock_back_pointer)
    #print("icerock_feedback ", icerock_feedback)
    #edge_strength_matrix = edge_strength(input_image)

    # You'll need to add code here to figure out the results! For now,
    # just create some random lines.
    # airice_simple = [image_array.shape[0] * 0.25] * image_array.shape[1]
    # airice_hmm = [image_array.shape[0] * 0.5] * image_array.shape[1]
    #airice_feedback = [image_array.shape[0] * 0.75] * image_array.shape[1]
    # icerock_simple = [image_array.shape[0] * 0.25] * image_array.shape[1]
    # icerock_hmm = [image_array.shape[0] * 0.5] * image_array.shape[1]
    #icerock_feedback = [image_array.shape[0] * 0.75] * image_array.shape[1]

    # Now write out the results as images and a text file
    write_output_image("air_ice_output.png", input_image, airice_simple, airice_hmm, airice_feedback, gt_airice)
    write_output_image("ice_rock_output.png", input_image, icerock_simple, icerock_hmm, icerock_feedback, gt_icerock)
    with open("layers_output.txt", "w") as fp:
        for i in (airice_simple, airice_hmm, airice_feedback, icerock_simple, icerock_hmm, icerock_feedback):
            fp.write(str(i) + "\n")
