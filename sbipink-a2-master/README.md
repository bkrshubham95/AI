# <div align="center"> CS B551 - Assignment 2: Games and Bayesian Classifiers
#####  <div align="center"> CSCI B551 - Elements of Artificial Intelligence!

<br>



### AIM
***To practice with game playing and probability.***

***
### [Part 1: Raichu]

***

### Info:


Report Part1:

1.For the board game we have defined the movement function for all     the pieces taking into consideration of all the pieces on the board.
2. We have defined a valid move function which will define if the move is valid
3. For each board we are calculating the valid moves for all the all the pieces and putting the new board into the  successor function .
4. We are using minimax here with alpha beta pruning.
5. For move generation, we are calculating all the possible moves using the rules and then passing each successor board in the minimax function.
6. Furthermore, we’re checking for raichus and converting it if we are reaching on the same board.

### References:
1. https://en.wikipedia.org/wiki/Minimax

***

***
### [Part 2: The Game of Quintris!](https://github.iu.edu/cs-b551-fa2021/hhansar-sbipink-sinhabhi-a2/tree/master/part2)

***
#### Problem Statement:
The game of Quintris will likely seem familiar. It starts off with a blank board. One by one, random pieces
(each consisting of 5 blocks arranged in different shapes) fall from the top of the board to the bottom. As
each piece falls, the player can change the shape by rotating it or flipping it horizontally, and can change its
position by moving it left or right. It stops whenever it hits the ground or another fallen piece. If the piece
completes an entire row, the row disappears and the player receives a point. The goal is for the player to
score as many points before the board  fills up.

#### Inputs:

The program generates a string of moves ('mnbh') that correspond to right, rotate, left, horizontal flip movements
of the current piece in the game

#### Expected Output:

Corresponding to each move, the game prints the current board state on the screen.

#### Command:

<code> python3 ./quintris.py computer simple </code>

***

### Info:
- The program is designed to find the a combination of moves for which the cost function "def cost(self, quintris, quintris2)" is minimum.
- State Space: The state space is the set of all possible combinations of moves that can be made without the piece colliding with another piece on the board, or the edge of the board itself.
- Successor Function: To find all possible states, We calculate all the possible moves corresponding to each piece. For example, each piece can be moved horizontally from one edge of the board to another, also, they can be flipped horizontally two times, and rotated 4 times.
- Cost funtion: We assign weights to the following components based on hit and trial while testing:
  a. number of holes in the board 
  b. difference between the maximum and minimum height of tiles
  c. difference in heights of adjacent tiles
  d. depth of wells in the board: empty spaces surrounded by tiles
  e. line clears
- Goal state: The goal state is a state with minimum cost -> this would ideally lead to a high score on the game over time
- Search algorithm: We use Expectimax algorithm to find the best move. We use a chance node to calculate the expected cost of a subsequent piece and add it to the cost for the next_piece and the cost for the current_piece.

### References:
1. https://inst.eecs.berkeley.edu/~cs188/fa18/assets/slides/lec7/FA18_cs188_lecture7_expectimax_search_and_utilities_1pp.pdf

***
***
### [Part 3: Truth be Told](https://github.iu.edu/cs-b551-fa2021/hhansar-sbipink-sinhabhi-a2/tree/master/part3)

***
#### Problem Statement:
User-generated reviews are transforming competition in the hospitality industry, because they are valuable for both the guest
and the hotel owner. For the potential guest, it's a valuable resource during the search for an overnight stay.
For the hotelier, it's a way to increase visibility and improve customer contact. So it really affects both the
business and guest if people fake the reviews and try to either defame a good hotel or promote a bad one.
Our task is to classify reviews into faked or legitimate, for 20 hotels in Chicago.

#### Command:

<code> python3 ./SeekTruth.py deceptive.train.txt deceptive.test.txt </code>

***

### Info:

The aim is to create a bayesian classifier for detecting the reviews as truthful or deceptive . We want to calculate the class  of the review given words in reviews . Using the bayesian law that translates to calculating the probability of the words given class . Using the training data we calculate the prior probability of the word given class .The design format is as below:

1.We have parsed the training text file and get the reviews as list of objects .

2.We have used regex to remove unnecessary symbols and numbers that are not useful to us .

3.We have created two dictionary to maintain the word count of the of all unique word based on class.

4.We have created two probability table for words given class and applied the Laplace smoothing by adding 1 to count of all the words and calculated probability by dividing it by total word count + length of vocabulary (unique word ) in that class

5.For finding the class of the new reviews we iterate over the word and fetch the probability of the word given class from the probability class table and the idea is to multiply the probability taking the independence that comes with baysian hypothesis .But the probabilities are so small and over multiplication of hundreds of similar probabilities it becomes even smaller so I have used log transformation where we can add the log of all the probabilities and instead of dividing it with other class probabilities using log principles we subtract it and used on the the values we decide which class it belongs to .

6.Have added the stop words list as well to avoid common words and calculating their probabilities and also avoid it durning classification as well as they are common words and do not impact classification in general.

### References:
1. https://en.wikipedia.org/wiki/Naive_Bayes_classifier

***
