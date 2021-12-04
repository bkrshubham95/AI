#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import math
import copy

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [["".join(['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH)]) for y in
                    range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


def read_training_file(fname):
    filtered_data = []
    file = open(fname, 'r');
    for line in file:
        data = tuple([w for w in line.split()])
        filtered_data += [(data[0::2], data[1::2]), ]
    # print(filtered_data)
    return filtered_data


def get_matching_probability(test_pattern,
                             train_pattern):  # get matching probability between the test and train patterns
    matching_prob = 1
    star_prob = 1  # probability = 1 for exact match with star
    valid_space = 0.3  # probability = 0.3 for exact match with space
    invalid_pixel = 0.2  # probability of 0.2 for no match
    for i in range(len(test_pattern)):
        for j in range(len(test_pattern[i])):
            if test_pattern[i][j] != train_pattern[i][j]:  # if both the pixels match or not
                matching_prob = matching_prob * invalid_pixel
            else:
                if (test_pattern[i][j] == '*'):
                    matching_prob = matching_prob * star_prob
                else:
                    matching_prob = matching_prob * valid_space
    return matching_prob


def fit(training_data):
    combination = training_data
    for phrase, idx in combination:  # looping through the tuples in the following way --((("a","b")-->phrase,("c","d")-->position),((),()))
        for k in range(0, len(phrase)):
            if k == 0:  # initial probabilites
                if phrase[k][0] not in initial_probs:
                    initial_probs[phrase[k][0]] = 1
                else:
                    initial_probs[phrase[k][0]] += 1

        joined_phrase = " ".join(phrase)  # joining phrases with space in between
        for k in range(len(joined_phrase)):
            if k != 0:
                chr_cmb = joined_phrase[k - 1] + joined_phrase[k]
                if chr_cmb not in transition_probs:  # transition probabilities
                    transition_probs[chr_cmb] = 1
                else:
                    transition_probs[chr_cmb] += 1


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

# creating global variables for dictionaries
word_dict = {}
result_seq = []
initial_probs = {}
transition_probs = {}

train_data = read_training_file(train_txt_fname)
fit(train_data)
print("Training done...")

# Getting results for simple bayes net

for tst_pattern in test_letters:
    min_val = math.inf
    for train_char in TRAIN_LETTERS:  # given the train_char
        matching_prob = get_matching_probability(tst_pattern, train_letters[train_char])
        log_prob = -math.log(matching_prob)
        if log_prob < min_val:  # minimum value for the log probability
            min_val = log_prob
            letter_assigned = train_char
    result_seq.append(letter_assigned)  # appending the most probable character sequence for simple bayes net

# Getting results for Viterbi algorithm

lowest_val = 0.000001
prev_scores_lst = []
best_scores_lst = []

print("Getting results...")

for idx in range(len(test_letters)):  # tst_pattern in test_letters:
    prev_scores_lst_temporary = []
    minimum = math.inf
    for train_char in TRAIN_LETTERS:  # given the train_char
        if idx == 0:
            sim_prob = get_matching_probability(test_letters[idx], train_letters[train_char])
            if train_char not in initial_probs:
                initial_probs[train_char] = lowest_val
            log_prob = -math.log(sim_prob) - math.log(initial_probs[train_char] / sum(initial_probs.values()))
            prev_scores_lst_temporary.append((train_char, log_prob))
        elif idx != 0:
            j = 0
            for prev_chars in TRAIN_LETTERS:  # looping through each training letter
                sim_prob = get_matching_probability(test_letters[idx], train_letters[train_char])
                chr_cmb = prev_chars + train_char
                if chr_cmb not in transition_probs:
                    transition_probs[chr_cmb] = lowest_val
                log_prob = -math.log(sim_prob) - math.log(prev_scores_lst[j][1]) - math.log(
                    transition_probs[chr_cmb] / sum(transition_probs.values()))
                j += 1
                if log_prob < minimum:
                    minimum = log_prob
                    list_scores_best_for_each_POS = (train_char, log_prob)  # best for each layer
            prev_scores_lst_temporary.append(list_scores_best_for_each_POS)
    prev_scores_lst = copy.deepcopy(prev_scores_lst_temporary)
    best_scores_lst.append(min(prev_scores_lst, key=lambda prev_scores_lst: prev_scores_lst[1]))  # best overall
viterbi_result = [x[0] for x in best_scores_lst]

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:

print("\n".join([r for r in train_letters['o']]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
print("\n".join([r for r in test_letters[4]]))

simple_result = "".join(result_seq)
hmm_result = "".join(viterbi_result)

print("Simple: " + simple_result)
print("   HMM: " + hmm_result)
