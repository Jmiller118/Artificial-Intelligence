# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #we want to eat the closest food while knowing where the ghosts are
        foodList = newFood.asList()
        foodDistance = -1

        for food in foodList:
            newDistance = util.manhattanDistance(newPos, food)
            if foodDistance >= newDistance or foodDistance == -1:
                foodDistance = newDistance

        proxGhost = 0
        oneStep = 1
        for ghost in successorGameState.getGhostPositions():
            distance = util.manhattanDistance(newPos, ghost)
            oneStep += distance
            if distance <= 1:
                proxGhost += 1

        foodRecprical = ( 1 / float(foodDistance))
        ghostRecprical = (1 / float(oneStep))

        return successorGameState.getScore() + foodRecprical - ghostRecprical - proxGhost

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        legalMoves = gameState.getLegalActions(0)
        bestRoute = None
        rootValue = -99999

        for move in legalMoves:
            successor = gameState.generateSuccessor(0, move)
            actionCost = self.MinValue(successor, 1, 0)
            if actionCost > rootValue:
                rootValue = actionCost
                bestRoute = move
        return bestRoute

    def MaxValue(self, gameState, depth):
        moves = len(gameState.getLegalActions(0))
    
        if depth == self.depth or moves == 0: 
            return self.evaluationFunction(gameState)

        return max([self.MinValue(gameState.generateSuccessor(0, move), 1, depth) for move in gameState.getLegalActions(0)])

    def MinValue(self, gameState, index, depth):
        moves = len(gameState.getLegalActions(index))
        legalMoves = gameState.getLegalActions(index)

        if moves == 0:
            return self.evaluationFunction(gameState)

        if index < gameState.getNumAgents() - 1:
            return min([self.MinValue(gameState.generateSuccessor(index, move), index + 1, depth) for move in gameState.getLegalActions(index)])

        else:
            return min([self.MaxValue(gameState.generateSuccessor(index, move), depth + 1) for move in gameState.getLegalActions(index)])
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -99999
        beta = 99999

        actionCost = -99999
        bestRoute = None
        legalMoves = gameState.getLegalActions(0)

        for move in legalMoves:
            successor = gameState.generateSuccessor(0, move)
            actionCost = self.MinValue(successor, 1, 0, alpha, beta)

            if alpha < actionCost:
                alpha = actionCost
                bestRoute = move

        return bestRoute

    def MaxValue(self, gameState, depth, alpha, beta):
        moves = gameState.getLegalActions(0)

        if depth == self.depth or len(moves) == 0:
            return self.evaluationFunction(gameState)

        actionCost = -99999

        for move in moves:
            successor = gameState.generateSuccessor(0, move)
            actionCost = max(actionCost, self.MinValue(successor, 1, depth, alpha, beta))

            if actionCost > beta:
                return actionCost

            alpha = max(alpha, actionCost)

        return actionCost
    
    def MinValue(self, gameState, index, depth, alpha, beta):
        moves = gameState.getLegalActions(index)

        if len(moves) == 0:
            return self.evaluationFunction(gameState)

        actionCost = 99999
        
        for move in moves:
            if index < gameState.getNumAgents() - 1:
                successor = gameState.generateSuccessor(index, move)
                actionCost = min(actionCost, self.MinValue(successor, index + 1, depth, alpha, beta))
            else:
                successor = gameState.generateSuccessor(index, move)
                actionCost = min(actionCost, self.MaxValue(successor, depth + 1, alpha, beta))

            if actionCost < alpha:
                return actionCost

            beta = min(beta, actionCost)

        return actionCost


        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        legalMoves = gameState.getLegalActions(0)
        rootValue = -99999
        bestRoute = None

        for move in legalMoves:
            successor = gameState.generateSuccessor(0, move)
            actionCost = self.Min_Value(successor, 1, 0)
            if actionCost > rootValue:
                rootValue = actionCost
                bestRoute = move

        return bestRoute
    
    def Max_Value(self, gameState, depth):
        moves = len(gameState.getLegalActions(0))
        legalMoves = gameState.getLegalActions(0)

        if depth == self.depth or moves == 0:
            return self.evaluationFunction(gameState)

        return max([self.Min_Value(gameState.generateSuccessor(0, action), 1, depth) for action in gameState.getLegalActions(0)])


    def Min_Value(self, gameState, index, depth):
        moves = len(gameState.getLegalActions(index))

        if moves == 0:
            return self.evaluationFunction(gameState)
        
        if index < gameState.getNumAgents() - 1:
            return sum([self.Min_Value(gameState.generateSuccessor(index, move), index + 1, depth) for move in gameState.getLegalActions(index)]) / float(moves)

        else:
            return sum([self.Max_Value(gameState.generateSuccessor(index, move), depth + 1) for move in gameState.getLegalActions(index)]) / float(moves)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: I took the code from question one and added a function for the number of power pellets. This is then subtracted from the value that is returned.
      When there are a lot of power pellets left, the pacman will try to eat them sooner because it subtracts from the score until they are not longer there.
    """
    "*** YOUR CODE HERE ***"
    ghostPosition = currentGameState.getGhostPositions()
    pacmanPosition = currentGameState.getPacmanPosition()
    foodList = (currentGameState.getFood()).asList()
    power = currentGameState.getCapsules()
    numPower = len(power)

    score = 0
    foodDistance = -1

    for food in foodList:
        newDistance = util.manhattanDistance(pacmanPosition, food)
        if foodDistance >= newDistance or foodDistance == -1:
            foodDistance = newDistance

    proxGhost = 0
    oneStep = 1
    
    for ghost in ghostPosition:
        distance = util.manhattanDistance(pacmanPosition, ghost)
        oneStep += distance
        if distance <= 1:
            proxGhost =+ 1
    

    
    foodRecprical = ( 1 / float(foodDistance))
    ghostRecprical = (1 / float(oneStep))
    return currentGameState.getScore() + foodRecprical - ghostRecprical - proxGhost - numPower

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

