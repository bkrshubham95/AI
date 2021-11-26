# SeekTruth.py : Classify text objects into two categories
#
# Code by Shubham Bipin Kumar (sbipink) , Himanshu Hansaria (hhansar) Abhinav Sinha (sinhabhi)
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import re
import math

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):
    # This is just dummy code -- put yours here!

    #print(train_data['labels'])
    #print(test_data['labels'])
    deceptive_word_list , truthful_word_list, list_vocab,deceptive_label_count,truthful_label_count = cleartrainingdata(train_data)
    deceptive_word_freq_dict = create_word_freq_table(deceptive_word_list)
    truthful_word_freq_dict = create_word_freq_table(truthful_word_list)
    deceptive_word_probability_table = create_word_probability_table(deceptive_word_freq_dict,list_vocab)
    truthful_word_probability_table= create_word_probability_table(truthful_word_freq_dict,list_vocab)
    p_truthful = truthful_label_count/(truthful_label_count+deceptive_label_count)
    p_deceptive = deceptive_label_count/(deceptive_label_count + truthful_label_count)
    prediction_class_list = predict_class_for_test_data(deceptive_word_probability_table,truthful_word_probability_table, test_data,list_vocab,p_truthful,p_deceptive)
    return prediction_class_list
    #return [test_data["classes"][0]] * len(test_data["objects"])


###for calculating which class the reviews belong to i'll be calculating product of probablilty of each word upon class
####and take the ratio and depending on the ratio we will decide the review belongs to which class


def predict_class_for_test_data(deceptive_word_probability_table,truthful_word_probability_table, test_data,list_vocab,p_truthful,p_deceptive):
    stop_word = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    total_word = len(list_vocab)
    total_deceptive_words = len(deceptive_word_probability_table.keys())
    total_truthful_word = len(truthful_word_probability_table.keys())
    p_word_to_deceptive =0.0
    p_word_to_truthful =0.0
    final_prediction_list = []
    list_of_test_data_object = test_data['objects']
    #first clean the test_data
    #list of list for test words in all reviews
    review_word_list =[]
    for review_string in list_of_test_data_object:
        word_list = word_regex(review_string)
        review_word_list.append(word_list)

    #iterate through list of list now calulate probability of each word per class and multiply
    #Handle the new word here (also keep in mind if we can calculate log values)
    for word_list in review_word_list:
        for word in word_list:
            if (word not in stop_word):
                p_word_to_dect =deceptive_word_probability_table.get(word)
                if (p_word_to_dect == None):
                    p_word_to_dect = 1/(total_deceptive_words)
                p_word_to_deceptive = p_word_to_deceptive + math.log10(p_word_to_dect)

                p_word_to_truth = truthful_word_probability_table.get(word)
                if(p_word_to_truth == None):
                    p_word_to_truth = 1/(total_truthful_word)
                p_word_to_truthful = p_word_to_truthful + math.log10(p_word_to_truth)
            else:
                continue
        #for now I am assuming equal probability for truthful and decptive
        #we can always calculate  the no of truthful and deceptive cases in train.txt and calculate class probability accordingly
        #print(p_word_to_deceptive)
        #print(p_word_to_truthful)
        classifcation_value = (math.log10(p_deceptive)+p_word_to_deceptive)- (math.log10(p_truthful)+p_word_to_truthful)
        if (classifcation_value > 0):
            final_prediction_list.append('deceptive')
        else:
            final_prediction_list.append('truthful')

    return final_prediction_list

def stop_word_list_creation():
    stop_word = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]




### remember later to work on the stop words on as well
### as well how to handle test data to predict for each of the rows and return percentage


##will create a table which will consist of probability of all the words w.r.t a given class
##such as decptive and truthful in this case
def create_word_probability_table(word_freq_dict,list_vocab):
    vocabulary_for_class =  word_freq_dict.keys()
    total_vocab_len = len(vocabulary_for_class)
    total_word_count_of_class = sum(word_freq_dict.values())
    ##need cound of all the words in the class
    word_probab_table = {}
    for word in vocabulary_for_class:
        #word_probab_table[word] = word_freq_dict[word]/total_word_count_of_class
        word_probab_table[word] = (word_freq_dict[word] + 1) / (total_word_count_of_class + total_vocab_len)
    return word_probab_table


    ###this is the code  have in mind for the laplace transform
    ### word_probab_table[word] = (word_freq_dict[word]+1)/(total_word_count_of_class+ total_vocab_len)
    ### create a common table with all words and their probability with both classes as seperate columns
    ### don't forget to do the laplase transform as well


def create_word_freq_table(word_list):
    word_freq_dict = {}
    stop_word = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    for word in word_list:
        if word not in word_freq_dict:
            if word in stop_word:
                continue
            else:
                word_freq_dict[word] = 0
        word_freq_dict[word] += 1

    return word_freq_dict


def cleartrainingdata(train_data):
    review_object_list = train_data['objects']
    label_list = train_data['labels']
    deceptive_label_count =0
    truthful_label_count =0
    deceptive_string = ''
    truthful_string = ''
    i =0
    for label in label_list:
        if label == 'deceptive':
            deceptive_label_count = deceptive_label_count + 1
            deceptive_string = deceptive_string + review_object_list[i]
            i +=1
        elif label == 'truthful':
            truthful_label_count =truthful_label_count + 1
            truthful_string = truthful_string + review_object_list[i]
            i +=1
        else:
            continue

    deceptive_word_list = word_regex(deceptive_string)
    truthful_word_list = word_regex(truthful_string)

    ## TRYING TO create the vocabulary which will consist of  all the unique
    ## words from both the truthful as well as deceptive word list
    list_vocab = get_unique_elements_from_two_list(deceptive_word_list,truthful_word_list)
    return deceptive_word_list,truthful_word_list, list_vocab,deceptive_label_count,truthful_label_count


def get_unique_elements_from_two_list(deceptive_word_list,truthful_word_list):
    set_truthful = set(truthful_word_list)
    set_deceptive = set(deceptive_word_list)
    set_vocab = set_truthful.copy()
    set_vocab.update(set_deceptive)
    ##set_vocab = set_truthful + set_deceptive
    list_vocab = (list(set_vocab))
    return list_vocab

def word_regex(any_string):
    new_string = any_string.lower()
    regex = r'\b\w+\b'
    list_of_word = re.findall(regex, new_string)
    return list_of_word

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    #train_file = 'deceptive.train.txt'
    #test_file= 'deceptive.test.txt'

    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)
    #print(results)
    #print(len(results))
    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

