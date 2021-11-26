# REPORT:
## PART 1:
- This misere Rubic's cude puzzle can be thought as a search problem where we define  state space, successor function, edge weights, goal state, and heuristic function(s) as follows:
-  State Space: Set of state space includes all the possible configurartions of the board given any of the 24 possible moves taken.
-  Successor function: Given by the successors(state) in the code returns all the possible states given the current state. All the next states that are led by moving according to any of the 24 moves form valid successor set for a given board state.
- If the nodes are assumed to be the successor states connected by their prent state, the edge cost is 1 and same for all. Hence, the cost function is a plus 1 to the parent state for each of the 24 possible childern states.
- Goal state is the cononical configuration of the of the board
- Heuristic Function is calculating the sum of the shortest path taken by each cell of the board to reach to it's canonical configuration's position. As each of the possible 24 moves can change the position of the cell by atmost 1 in one move, calculating the absolute disctance between the rows and colums individually works for us. This is an admissible heuristic because we can never reach the goal state in less that the mod difference between the cell's goal cell and current cell. Adding the constraints like movement of the whole row with a R1 only would increase the cost.
- The search is basically based of priortizing the least F(n) valued node. We pop the node with the least f(n) and search for all it's successors. If the successors have not been visited, we add the in out priority queue and again check for the poped node with the least f(n).
- Not tracking the visited nodes in this case gives bad results and determining a good heuristic is extremely essential in terms of pruning the tree and getting good runtime.
- Branching factor of the search tree at a specific level can be defined as the number of the nodes at the child level devided my the number of the nodes at the current level. In other words how many clildren would one node lead to must give us the branching factor. In the worst case it would be 24 (one for each) possible move in this case.
- If a solution is reached in 7 moves, in terms of search free we can say that depth of the solution node is 7. In the worst case, we would need to explore all the nodes up-untill the level 7 to get the solution. Each level(l) has 24^l nodes. Hence BFS might have to explore 24^1 + 24^2 +24^3....24^7 nodes in the worst case. 24^8-1 can be an approx answer. However, A* algorithm can also end up exploring all the nodes with bad heuristic. In our code it searched less that 1000 nodes for 7 ruote answer which is significantly improving the performance 
## PART 2:
- This program is working using the A* algorithm. 
- We are handling missing latitudes and longitudes by taking their default value as 0 and checking them while calculating the heuristic. If they are zero, we are assigning a zero heuristic value in that case.
- Cost function for :-
	* segments - We are keeping the edge cost as 1 and adding 1 to current cost till now every time we are taking a successor
	* distance - We are keeping the edge cost as the distance between the current vertex and the successor vertex in miles and adding this distance to the trip distance travelled till now
	* time - We are keeping the edge cost as the time taken between the current vertex and the successor vertex based on the speed given between them and adding this time taken to the current time taken till now
	* delivery - We are keeping the cost the same as time, just that in case the speed >= 50, we add an additional cost of time as given by the formula in the question.
- First we're building the vertices and the edges of the graph using the given text files. 
- For the Successor function, we check the neighbours of the current vertex at each instance.
- For the heuristic, the admissibility is ensured based on how the triangle inequality works. 
## PART 3:
- The grouping problem can be formulated as a Local search problem of the optimal solution of the minimized total cost of all the teams of the given member set.
- We are parsing the input file to map the relevent infomation like team member number choice and preferences etc. for a given user_id
- The idea is to have all the possible combinations of teams for a given set and then check for combination with minimum cost. Hence our state space would be the all the possible combinations of teams possible for a given member.
- We create 3 different lists based on groups of 3, 2, 1 and then apply randomization sampling without replacement to assign members to those groups.
- Cost Function- we calculate the cost based on number of teams , groupsize prference , people not getting desired group and people having to work with people they don't want to work with . We have have tried to minimise the cost by forming more no of groups of 3 people but avoiding the against one as much as possible
- We check all valid combinations and yield based on the minimum cost. 