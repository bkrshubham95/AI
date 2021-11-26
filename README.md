# a0
Part1: Navigation

The expectation is to find the optimum path from between the observer and the pichu.

Following parameters have been considerd:

valid states: It defines all the possible coordinates where pichu can travel which is represented by .

Goal state: It defines the state where the pichu meets the observer

cost function: It is uniform for all the movements.

Successor function: It returns all the possible location where pichu can travel

The existing program uses depth first search but it does not guarentees the optimum solution everytime and can go into the infinite loop. So i have used depth first search which gave the optimum solution 

The program often fails because it goes into infinite loop where it adds some nodes to the fringe repeatedly.

Solution:
I have implemented dfs with visited node to avoid infinite loop.


Part2:Hide and seek 

To fix the program I have decided to add checks for checking the row , column and diagonal if other pichu is present
- if they are present then i am checking if there is any obstacle between them 


- I have added this in my successor function to check all the valid successor function so that only those are returned.