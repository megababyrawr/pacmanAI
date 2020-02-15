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

def genericGraphSearchAlgorithm(problem, dataStructure):
    # This is a general graph search algo that is implementable with different data structures
    # The data structure will hold a "plan" that includes 3-tuple info: (current state, action plan, total cost)

    #add the initial state to the dataStructure
    visitedStates = set()
    dataStructure.push((problem.getStartState(), [], 0))

    while not dataStructure.isEmpty():

        currentTuple = dataStructure.pop()
        currentState = currentTuple[0]


        #check for goal state, then return the action plan if it is goal state
        if problem.isGoalState(currentTuple[0]):
            return currentTuple[1]
        else:
            #check if we have already visited this state
            if currentTuple[0] not in visitedStates:

                visitedStates.add(currentState)

                for successor in problem.getSuccessors(currentState):
                    if successor[0] not in visitedStates:
                        dataStructure.push((successor[0], currentTuple[1]+[successor[1]], currentTuple[2]+successor[2]))
    return False  # if no solution is found

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stackStructure = util.Stack()
    return genericGraphSearchAlgorithm(problem, stackStructure)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queueStructure = util.Queue()
    return genericGraphSearchAlgorithm(problem, queueStructure)
    util.raiseNotDefined()

def RecursiveDLS(initialStateTuple, problem, limit):
    currentTuple = initialStateTuple
    currentState = initialStateTuple[0]

    if problem.isGoalState(currentState):
        return currentTuple[1]
    elif limit == 0:
        return "cutoff"
    else:
        cutoff_occured = False
        for successor in problem.getSuccessors(currentState):
            child = (successor[0], currentTuple[1] + [successor[1]], currentTuple[2] + successor[2])
            result = RecursiveDLS(child, problem, limit - 1)
            if result == "cutoff":
                cutoff_occured = True
            elif result != "failure":
                return result
        if cutoff_occured:
            return "cutoff"
        else:
            return "failure"

def DepthLimitedSearch(problem, limit):
    initialTuple = (problem.getStartState(), [], 0)
    return RecursiveDLS(initialTuple, problem, limit)

def iterativeDeepeningSearch(problem):
    """Search the tree iteratively for goal nodes."""
    "*** YOUR CODE HERE ***"

    for depth in range(0, 1000):
        result = DepthLimitedSearch(problem, depth)
        if result != "cutoff":
            return result
        print(depth)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    functionQueue = util.PriorityQueueWithFunction(lambda x: problem.getCostOfActions(x[1]))
    return genericGraphSearchAlgorithm(problem, functionQueue)
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

    functionQueue = util.PriorityQueueWithFunction(lambda x: problem.getCostOfActions(x[1]) + heuristic(x[0], problem))
    return genericGraphSearchAlgorithm(problem, functionQueue)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
iddfs = iterativeDeepeningSearch
