# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    
    #Search the deepest nodes in the search tree first.

    #Your search algorithm needs to return a list of actions that reaches the
    #goal. Make sure to implement a graph search algorithm.

    #To get started, you might want to try some of these simple commands to
    #understand the search problem that is being passed in:
    
    "*** YOUR CODE HERE ***"

    stack = util.Stack()
    initial_state = problem.getStartState()
    visited = []
    stack.push((initial_state, [], []))
   
   #while we have stuff in the stack
    while not stack.isEmpty():
        current_location, action, visited = stack.pop()

        if not current_location in visited:
            visited.append(current_location)

            if problem.isGoalState(current_location):
                return action

            for position, direction, step in problem.getSuccessors(current_location):
                stack.push((position, action + [direction], visited + [current_location]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #two lists, explored and actions
    queue = util.Queue()
    initial_state = problem.getStartState()
    queue.push((initial_state, [], []))
    visited = []

    #when nested for loop took too long to run during exectution
    #try seperating them out

    #while we have stuff in the queue
    while not queue.isEmpty():
        current_location, action, cost  = queue.pop()

        #if we havent been here add it to places we have been
        if not current_location in visited:
            visited.append(current_location)

            if problem.isGoalState(current_location):
                return action
            
            #get the info we need for each position and add it to the queue
            for position, direction, step in problem.getSuccessors(current_location):
                queue.push((position, action + [direction], cost + [step]))
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    priority = util.PriorityQueue()
    initial_state = problem.getStartState()
    priority.push((initial_state, []), 0)
    visited = []
    
    #execution time took too long while nested for loop follow implimetation from above

    while not priority.isEmpty():
        current_location, action = priority.pop()

        if problem.isGoalState(current_location):
            return action
    
        if not current_location in visited:
            visited.append(current_location)

            for position, direction, step in problem.getSuccessors(current_location):
                #we need the cost of our actions
                cost = problem.getCostOfActions(action) + step
                #update the cost and push it on the queue
                priority.update((position, action + [direction]), cost)
                #priority.push((position, action + [direction]), cost)
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    open_list = util.PriorityQueue()
    
    initial_state = problem.getStartState()
    closed_list = []
    open_list.push((initial_state, [], 0), heuristic(initial_state, problem))

    while not open_list.isEmpty():
        #add something for f score
        current_location, action, cost  = open_list.pop()
        if problem.isGoalState(current_location):
            return action
    
        if not current_location in closed_list:
            closed_list.append(current_location)

            for position, direction, step in problem.getSuccessors(current_location):
                #g is the cost of each move, h is the heurstic value
                g = problem.getCostOfActions(action) + step
                #we need two lists, only want to visit it 
                open_list.update(position, action)
                h = heuristic(position, problem)
                f_score = g + h
                open_list.push((position, action + [direction], g), f_score)
    return []
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
