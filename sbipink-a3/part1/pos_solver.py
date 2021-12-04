###################################
# CS B551 Spring 2021, Assignment #3
#
# Your names and user ids: sinhabhi, sbipink, hhansar
#
# (Based on skeleton code by D. Crandall)
#


import numpy as np
import math
import random


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.pos_tags = ['adj', 'adv', 'adp', 'conj', 'det',
                         'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        self.emission_probabilities = {}
        self.pos_counts = {}
        self.word_counts = {}
        self.word_pos_counts = {}
        self.n_words = 0
        self.n_lines = 0
        self.pos_probabilities = {}
        self.pos_transition_counts = {}
        self.pos_transition_probabilities = {}

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        # Posterior Prob = P(S1, S2, ..., SN|W1, W2, ..., Wn) =
        # Product over i = 1...n of P(Si) * P(Wi|Si)
        if model == "Simple":
            log_p_posterior = 0
            for i in range(len(sentence)):
                log_p_posterior += self.calc_log_p_posterior(sentence[i],
                                                             label[i])
            return log_p_posterior

        # Posterior Prob = P(S1, S2, ..., SN|W1, W2, ..., Wn) =
        # P(S0) * Product over i = 0...n-1 of P(Si+1|Si) * Product over
        # i = 0...n of P(Wi|Si)
        elif model == "HMM":
            log_p_posterior = 0
            for i in range(len(sentence)-1):
                if i == 0:
                    log_p_posterior += math.log(
                        self.pos_transition_probabilities.get(
                            (label[i], ''), 0.0000000000000000001))
                else:
                    log_p_posterior += math.log(
                        self.pos_transition_probabilities.get(
                            (label[i+1], label[i]), 0.0000000000000000001))
            for i in range(len(sentence)):
                log_p_posterior += math.log(
                    self.emission_probabilities.get(
                        (sentence[i], label[i]), 0.0000000000000000001))

            return log_p_posterior
        elif model == "Complex":
            log_p_posterior = 0
            for i in range(len(sentence)-1):
                if i == 0:
                    log_p_posterior += math.log(self.emission_probabilities.get((sentence[i], label[i]), 0.00000000000000001)) \
                        + math.log(
                        self.pos_transition_probabilities.get((label[i], ''), 0.00000000000000001)) \
                        + math.log(
                        self.pos_transition_probabilities.get((label[i + 1], label[i]), 0.00000000000000001))
                else:
                    log_p_posterior += math.log(self.emission_probabilities.get((sentence[i], label[i]), 0.00000000000000001)) \
                        + math.log(
                        self.emission_probabilities.get((sentence[i - 1], label[i - 1]), 0.00000000000000001)) \
                        + math.log(
                        self.emission_probabilities.get((sentence[i], label[i - 1]), 0.00000000000000001)) \
                        + math.log(
                        self.emission_probabilities.get((sentence[i + 1], label[i]), 0.00000000000000001)) \
                        + math.log(
                        self.emission_probabilities.get((sentence[i + 1], label[i + 1]), 0.00000000000000001)) \
                        + math.log(
                        self.pos_transition_probabilities.get((label[i], label[i - 1]), 0.00000000000000001)) \
                        + math.log(
                        self.pos_transition_probabilities.get((label[i + 1], label[i]), 0.00000000000000001))

            return log_p_posterior
        else:
            print("Unknown algo!")

    def calc_log_p_posterior(self, word, pos):
        return math.log(self.pos_probabilities.get(pos, 0.00000000000000001)) +\
            math.log(self.emission_probabilities.get(
                (word, pos), 0.00000000000000001))

    def calc_probability(self, prob_list):
        probability_list = [math.exp(i) for i in prob_list]
        Total_sum = sum(probability_list)
        for i in range(len(probability_list)):
            probability_list[i] = probability_list[i]/Total_sum
        return probability_list

    def gibbs_random(self, sentence):
        label = self.simplified(sentence)
        return label

    # Do the training!
    #

    def train(self, data):
        for word_tup, pos_tup in data:
            self.n_lines += 1
            for word, pos in zip(word_tup, pos_tup):
                self.n_words += 1
                if word in self.word_counts:
                    self.word_counts[word] += 1
                else:
                    self.word_counts[word] = 1
                if pos in self.pos_counts:
                    self.pos_counts[pos] += 1
                else:
                    self.pos_counts[pos] = 1
                if (word, pos) in self.word_pos_counts:
                    self.word_pos_counts[(word, pos)] += 1
                else:
                    self.word_pos_counts[(word, pos)] = 1
            # Calculate Transition Probabilities
            for i in range(len(pos_tup)-1):
                if i == 0:
                    if (pos_tup[i], '') in self.pos_transition_counts:
                        self.pos_transition_counts[(pos_tup[i], '')] += 1
                    else:
                        self.pos_transition_counts[(pos_tup[i], '')] = 1
                else:
                    if (pos_tup[i+1], pos_tup[i]) in \
                            self.pos_transition_counts:
                        self.pos_transition_counts[
                            (pos_tup[i+1], pos_tup[i])] += 1
                    else:
                        self.pos_transition_counts[
                            (pos_tup[i+1], pos_tup[i])] = 1

        # Calculate counts of each pos
        for pos in self.pos_counts:
            self.pos_probabilities[pos] = self.pos_counts[pos] / self.n_words

        # Calculate Emission Probabilities
        for (word, pos) in self.word_pos_counts:
            self.emission_probabilities[(word, pos)] = (self.word_pos_counts[(
                word, pos)]/self.n_words)/self.pos_probabilities[pos]

        # Calculate Transition Probabilities
        for (pos_t_1, pos_t) in self.pos_transition_counts:
            if pos_t != '':
                self.pos_transition_probabilities[(pos_t_1, pos_t)] = self.pos_transition_counts[(pos_t_1, pos_t)] /\
                    self.pos_counts[pos_t]
            else:
                self.pos_transition_probabilities[(pos_t_1, pos_t)] = self.pos_transition_counts[(pos_t_1, pos_t)] /\
                    self.n_lines

        # Functions for each algorithm. Right now this just returns nouns -- fix this!
        #

    def simplified(self, sentence):
        generated_label = []
        for word in sentence:
            max_log_p_posterior = -math.inf
            temp_pos = 'noun'
            for pos in self.pos_tags:
                temp_log_p_posterior = self.calc_log_p_posterior(word, pos)
                if temp_log_p_posterior != 0 and \
                        temp_log_p_posterior > max_log_p_posterior:
                    max_log_p_posterior = temp_log_p_posterior
                    temp_pos = pos
            generated_label.append(temp_pos)
        return generated_label

    def hmm_viterbi(self, sentence):
        v_table = np.zeros((len(self.pos_tags), len(sentence)))
        v_path = np.zeros((len(self.pos_tags), len(sentence) - 1))
        count = 0
        for i in range(len(sentence)):
            if i == 0:
                for j in range(len(self.pos_tags)):
                    temp = math.log(self.emission_probabilities.get((sentence[i], self.pos_tags[j]), 0.0000000000000000001)) +\
                        math.log(self.pos_transition_probabilities.get(
                            (self.pos_tags[j], ''), 0.0000000000000000001))
                    v_table[j][0] = temp
            else:
                for j in range(len(self.pos_tags)):
                    emmission_prob = math.log(self.emission_probabilities.get(
                        (sentence[i], self.pos_tags[j]), 0.0000000000000000001))
                    max_temp_state = []
                    for k in range(len(self.pos_tags)):
                        transition_prob = math.log(self.pos_transition_probabilities.get((self.pos_tags[k], self.pos_tags[j]),
                                                                                         0.0000000000000000001))
                        value = v_table[k][count - 1] + transition_prob
                        max_temp_state.append(value)
                    max_value = max(max_temp_state)
                    max_index = max_temp_state.index(max_value)
                    v_path[j][count - 1] = max_index
                    v_table[j][count] = emmission_prob + max_value
            count += 1

        v_path = v_path.astype('int')
        ind = np.argmax(v_table, axis=0)[-1]
        label = [ind]
        i = len(sentence) - 2
        while i >= 0:
            ind = v_path[ind][i]
            label.append(ind)
            i -= 1
        label = label[:: -1]
        generated_label = [self.pos_tags[i] for i in label]
        return generated_label

    def complex_mcmc(self, sentence):
        random_pos = self.gibbs_random(sentence)
        final_count = {}

        for i in range(500):
            for word in range(len(sentence)):
                prob_list1 = []
                if len(sentence) == 1:
                    for pos in self.pos_tags:
                        P = [math.log(self.emission_probabilities.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((pos, ''), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                # gibbs sampling
                elif word == 0:
                    for pos in self.pos_tags:
                        P = [math.log(self.emission_probabilities.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((pos, ''),
                                        0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((random_pos[word + 1], pos), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                elif word == len(random_pos) - 1:
                    for pos in self.pos_tags:
                        P = [math.log(self.emission_probabilities.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get(
                                 (random_pos[0], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.emission_probabilities.get((sentence[word], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((random_pos[word - 1], pos), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)
                else:
                    for pos in self.pos_tags:
                        P = [math.log(self.emission_probabilities.get((sentence[word], pos), 0.00000000000000001))
                             + math.log(self.emission_probabilities.get((sentence[word - 1], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.emission_probabilities.get((sentence[word], random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.emission_probabilities.get((sentence[word + 1], random_pos[word]), 0.00000000000000001))
                             + math.log(self.emission_probabilities.get((sentence[word + 1], random_pos[word + 1]), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((pos,
                                        random_pos[word - 1]), 0.00000000000000001))
                             + math.log(self.pos_transition_probabilities.get((random_pos[word + 1], pos), 0.00000000000000001))]
                        for i in P:
                            prob_list1.append(i)

                possible_prob = self.calc_probability(prob_list1)
                x = random.uniform(0, 1)
                max_value = 0
                for p in range(len(possible_prob)):
                    max_value += possible_prob[p]
                    if max_value > x:
                        random_pos[word] = self.pos_tags[p]
                        break
                for i in range(len(random_pos)):
                    if (i, random_pos[i]) not in final_count:
                        final_count[i, random_pos[i]] = 1
                    else:
                        final_count[i, random_pos[i]] += 1
        generated_label = []
        for i in range(len(random_pos)):
            max = 0
            max_pos = ''
            for pos in self.pos_tags:
                if (i, pos) in final_count:
                    if max <= final_count[i, pos]:
                        max = final_count[i, pos]
                        max_pos = pos
            generated_label.append(max_pos)
        return generated_label

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #

    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")
