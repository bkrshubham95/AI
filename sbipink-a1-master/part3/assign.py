#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: Himanshu Hansaria hhansar Shubham Bipin Kumar sbipink Arunima Shukla arushuk
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#
from itertools import product, chain
import itertools as it
import random as rn
import sys

def prepareLookupTable(textFile, partition):
    initial_teams = []
    input_dict = {}

    with open(textFile, "r") as f:
        lines = f.readlines()
        for line in lines:
            value = {}
            key, value["preffered"], value["notPreffered"] = line.split()
            value["groupSize"] = (value["preffered"].count('-')) + 1

            input_dict[key] = value


    return divide_lists(partition,input_dict)

def getTeamSizeComb(memberList, maxTeamSize):
    #print(memberList)
    #print(len(memberList))
    teamSizeRange = list(range(1, maxTeamSize + 1))
    #print(teamSizeRange)
    teamSizeDomain = []
    for n in range(1, len(memberList) + 1):
        for combination in it.combinations_with_replacement(teamSizeRange, n):
            if (sum(combination) == len(memberList)):
                teamSizeDomain.append(combination)
    return teamSizeDomain

def divide_lists(partition, initial_teams):
    userid = initial_teams.keys()
    count1 = 0
    count2 = 0
    count3 = 0

    # for partition in partitions:
    for e in partition:
        if e==1:
            count1+=1
        if e==2:
            count2+=2
        if e==3:
            count3+=3
    li1 = rn.sample(userid, count1)
    li2 = rn.sample([x for x in userid if x not in li1], count2)
    li3 = rn.sample([x for x in userid if x not in li1+li2], count3)
    return li3, li2, li1

def joinTupleWithStr(joinStr, tup):
    return joinStr.join(str(i) for i in tup)


def ListDiff(list1, list2):
    return (list(set(list1) - set(list2)))

def calculateCostFunction(teams, initialTeam):
    #print("teams", teams)
    DiffGroupSize = 0
    mismatch = 0
    timeWithDean = 0
    grading = len(teams) * 5


    for usr in initialTeam:
        for team in teams:
            if usr['user'] in team:
                thisTeam = team.split('-')
                if len(thisTeam) != len(usr['preffered']):
                    DiffGroupSize += 1
                userprefferedTeam = [member for member in usr['preffered']
                               if member != usr['user'] and member != 'xxx']
                mismatch += len(ListDiff(userprefferedTeam,
                                                      thisTeam))
                # #people with whom the user got assigned, against his choice
                userAgainst = [member for member in thisTeam if member in usr['notPreffered']]
                timeWithDean += len(userAgainst)

    return (timeWithDean * 10 + DiffGroupSize * 2 + grading + mismatch * 3)


def parseInputFiles(input_file):
    data = []
    with open(input_file, 'r') as file:
        for line in file:
            data.append([user for user in line.split()])
    #print(data)

    def mapUserData(user):
        workWith = user[1].split('-')
        # workWith.remove(user[0])
        return {'user': user[0], 'preffered': workWith, 'notPreffered': user[2].split(',')}

    #print(list(map(mapUserData, data)))
    return list(map(mapUserData, data))




def choose_grouping(li1, li2, li3):
    new_li=[li1, li2, li3]
    res = []
    for i, li in enumerate(new_li):
        items_per_group = i + 1
        cm = []
        for x in it.combinations(li, items_per_group):
            cm.append(x)
        if (len(cm) > 1):

            groups = [[] for _ in range(int(len(cm) / items_per_group))]
            # groups = [[]*30]
            while len(cm) > 0:

                a = cm.pop(0)

                for group in groups:

                    # create flattened list and check if all elements of tuple are absent
                    current_entries = list(chain.from_iterable(group))

                    if not sum([x in current_entries for x in a]):
                        group.append(a)
                        break
            # print(groups)
            groups = [group for group in groups if group]
            # print(groups)
            x = rn.choice(groups)
            res.append(x)
        elif (len(cm) == 1):
            res.append(cm)
    # print(res)
    flat_list = [e for li in res for e in li]
    # print(flat_list)
    return flat_list



# Driver Function
def calculate_result(input_file, input_table,li3, li2, li1):
    for _ in range(1):
        # li3, li2, li1 = prepareLookupTable(input_file)
        res = choose_grouping(li1, li2, li3)
        count = 0
        for a in res:
            for b in a:
                count += 1
        if count == len(li1) + len(li2) + len(li3):

            # print(res)
            result = []
            for r in res:
                r = joinTupleWithStr('-', r)
                result.append(r)
            # print(result)
            cost = calculateCostFunction(result, input_table)
            return {"assigned-groups": result, "total-cost": cost}

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    input_table = parseInputFiles(input_file)
    # print(input_table)

    input_dict = {}

    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            value = {}
            key, value["preffered"], value["notPreffered"] = line.split()
            value["groupSize"] = (value["preffered"].count('-')) + 1

            input_dict[key] = value

    # print(li1, li2, li3)
    min_cost = float('inf')
    count = 0
    # try:
    partitions = getTeamSizeComb(input_dict.keys(), 3)
    range_lst = [1, 10, 100, 250, 500, 1000]
    while (True):
        count += 1
        for i in range(len(partitions)):
            for k in range_lst:
                for j in range(k):
                    try:
                        li3, li2, li1 = prepareLookupTable(input_file, partitions[i])
                        f_result = calculate_result(input_file, input_table, li3, li2, li1)
                        cost = f_result["total-cost"]
                    except TypeError:
                        continue
                    except StopIteration:
                        pass
                    if cost < min_cost:
                        min_cost = cost
                        yield f_result



if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):

        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
