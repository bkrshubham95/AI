# hhansar-sbipink-sinhabhi-a3
a3 created for hhansar-sbipink-sinhabhi

### [Part 1: Part-of-speech tagging](https://github.iu.edu/cs-b551-fa2021/hhansar-sbipink-sinhabhi-a3)
***

### Problem Analysis
 ==================

#### Problem Statement:

Part of Speech Tagging using Simplified Bayes Net, HMM and Gibbs Sampling

#### Inputs:

**bc.train** is a text file containing training data with sentences. Each sentence has words and their corresponding part of speech

**bc.test** is a text file containing test data with sentences. Each sentence has words and its corresponding part of speech

#### Expected Output:

display the output of Steps 1-3 - Simple, HMM and Complex approach
display the logarithm of the joint probability P(S|W) foreach solution
display a running evaluation showing the percentage of words and whole sentences that have been labeled correctly so far

#### Command:

<code> python3 ./label.py training_file testing_file </code>

***
### Solution Analysis
==================

In this problem, we started with calculating the emission and transition probabilities.
For HMM, we used Viterbi algorithm to maximize the posterior probabilities
For Complex MCMC, we used Gibbs sampling to sample from the posterior distribution obtained from the Simple model. 

### References:
1. https://en.wikipedia.org/wiki/Forward%E2%80%93backward_algorithm
2. Viterbi code from Canvas

<br>
<br>


***

REPORT Q2:

Problem statement- The Goal is to find the air-ice and ice-rock boundary using the echogram images where the horizontal axis represent the distance along the surface and the vertical axis represent the depth beneath the surface .

Assumptions:
The air-ice boundary is always above the ice-rock boundary by a significant margin  10 pixels).
The two boundaries span the entire width of the image. Taken together these, two assumptions mean that in each column of the image, there is exactly one air-ice boundary and exactly one ice-rock boundary, and the ice-rock boundary is always below.


Approach:-

1.Using the Bayes net - 
	In this approach we find the maximum row index ie the maximum intensity pixel in each column for the air ice boundary and for the ice rock boundary we set air ice boundary strength to zero and try find the pixel with highest intensity in each column.


2. Using Viterbi - HMM
	In this approach we have used Viterbi algorithm with the backtracking approach.we have used the the transmission probabilities as below
	trans_p = [0.5, 0.4, 0.1, 0.05, 0.01,0.005,0.0005]  which is close to Gaussian distribution .
We have also used backtracking where we check the the intensity of the neighboring pixel and assign the probability in such a way that the smoothness is maintain .

Below are the few results that we obtained :


<img width="276" alt="Screen Shot 2021-12-01 at 11 15 19 PM" src="https://media.github.iu.edu/user/18346/files/b1850400-5301-11ec-807a-4880bdeefcea">

<img width="257" alt="Screen Shot 2021-12-01 at 11 15 56 PM" src="https://media.github.iu.edu/user/18346/files/b649b800-5301-11ec-8177-ecf9db1db057">

<img width="270" alt="Screen Shot 2021-12-01 at 11 15 01 PM" src="https://media.github.iu.edu/user/18346/files/bb0e6c00-5301-11ec-85a9-89c70d29016b">
<img width="320" alt="Screen Shot 2021-12-01 at 11 16 03 PM" src="https://media.github.iu.edu/user/18346/files/c5c90100-5301-11ec-8305-db08a20a3b07">

PART 3

In this problem, we implement a solution for reading letters from a given noisy image by using simple bayes net and HMM with MAP (Viterbi algorithm).

For solving this problem, we first used train text file with which we calculated the initial probabilities and transition probabilities. 
We calculated the emission probabilities by comparing the matching pixels between the train and the test patterns.

- Fit phase

1. First, we read and cleaned the file by removing invalid english characters.
2. We calculated the initial probabilities and transition probabilities using this train file.

- Simple Bayes Net

For each test character, we calculated the emission probability with each training character and the ouput for that test character is the corresponding 
training character with the highest emission probability.

- HMM MAP (Viterbi Algorithm)
In this algorithm, we consider the transition probability, emission probability, and the best probability till that state.

1. We calculated the highest probable sequence of characters by backtracking in the viterbi matrix.
2. We calculated the probability for the first test character by using the emission and initial probabilities.
3. For the rest of the test characters, we calculated the probability by using transition and emission probabilities.
4. We get the best combination of characters by choosing the minimum log probability corresponding to each test character. We get this sequence by backtracking
through the last test character in the viterbi matrix.
