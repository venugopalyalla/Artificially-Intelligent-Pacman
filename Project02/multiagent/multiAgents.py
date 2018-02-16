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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        positions = [GhostStates.getPosition() for GhostStates in newGhostStates]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodDistance = [util.manhattanDistance(newPos, x) for x in newFood.asList()]
        foodScore = 0
        if len(foodDistance):
            foodScore = min(foodDistance)
        ghostScore = 0
        for x in positions:
            ghostScore = ghostScore + util.manhattanDistance(newPos, x)
        finalScore = successorGameState.getScore()
        if newScaredTimes[0] > 14 and foodScore != 0:
            finalScore = successorGameState.getScore() + 10 / foodScore
        if ghostScore != 0 and foodScore != 0:
            finalScore = successorGameState.getScore() + 10 / foodScore - 1 / ghostScore
        "*** YOUR CODE HERE ***"

        return finalScore


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        costmax = float('-Inf')
        finalAction = ""
        for x in gameState.getLegalActions(0):
            tempcost = costmax
            costmax = max(costmax, self.Minimize(gameState.generateSuccessor(0, x), 0, 1))
            if costmax > tempcost:
                finalAction = x
        return finalAction

        util.raiseNotDefined()

    def Maximize(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        costmax = float('-Inf')
        for x in gameState.getLegalActions(0):
            costmax = max(costmax, self.Minimize(gameState.generateSuccessor(0, x), depth, 1))
        return costmax

    def Minimize(self, gameState, depth, ghost):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        costmin = float('Inf')
        for x in gameState.getLegalActions(ghost):
            if ghost == gameState.getNumAgents() - 1:
                costmin = min(costmin, self.Maximize(gameState.generateSuccessor(ghost, x), depth + 1))
            else:
                costmin = min(costmin, self.Minimize(gameState.generateSuccessor(ghost, x), depth, ghost + 1))
        return costmin


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.maximumValue(gameState, 1, float('-Inf'), float('Inf'))

    def checkGameState(self, gameState, depth):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)

    def maximumValue(self, gameState, depth, alpha, beta):
        goalState = self.checkGameState(gameState, depth)
        if goalState != None :
            return goalState
        maxVal = float('-Inf')
        finalAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            a = self.minimumValue(gameState.generateSuccessor(0, action), depth, 1, alpha, beta)
            if a > maxVal:
                maxVal = a
                finalAction = action
            if maxVal > beta:
                return maxVal
            alpha = max(alpha, maxVal)
        if depth == 1:
            return finalAction
        else:
            return maxVal

    def minimumValue(self, gameState, depth, agent, alpha, beta):
        goalState = self.checkGameState(gameState, depth)
        if goalState != None :
            return goalState
        minVal = float('Inf')
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            if agent != gameState.getNumAgents() - 1:
                a = self.minimumValue(successor, depth, agent + 1, alpha, beta)
            else:
                if depth < self.depth:
                    a = self.maximumValue(successor, depth + 1, alpha, beta)
                else:
                    a = self.evaluationFunction(successor)
            if a < minVal:
                minVal = a
            if minVal < alpha:
                return minVal
            beta = min(beta, minVal)
        return minVal

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
        costmax = float('-Inf')
        allActions = gameState.getLegalActions(0)
        nextNodes = [gameState.generateSuccessor(0, action) for action in allActions]
        values = [self.expectimax(Nodes, 1, 0) for Nodes in nextNodes]
        finalAction = []
        for i in range(len(values)):
            if values[i] == max(values):
                finalAction = allActions[i]
        return finalAction

    def maxValue(self, gameState, d):
        if gameState.isWin() or gameState.isLose() or d == self.depth:
            return self.evaluationFunction(gameState)
        allActions = gameState.getLegalActions(0)
        nextNodes = [gameState.generateSuccessor(0, action) for action in allActions]
        values = [self.expectimax(Nodes, 1, d) for Nodes in nextNodes]
        return max(values)

    def expectimax(self, gameState, player, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        allActions = gameState.getLegalActions(player)
        nextNodes = [gameState.generateSuccessor(player, action) for action in allActions]
        if player == gameState.getNumAgents() - 1:
            values = [self.maxValue(Nodes, depth + 1) for Nodes in nextNodes]
        else:
            values = [self.expectimax(Nodes, player + 1, depth) for Nodes in nextNodes]
        value = sum(values) / len(values)
        return value


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 1. First I have calculated the foodScore and the ghostScore, which is basically the distance to food and ghost respectively
                   2. There are two ways of calculating the score:
                      a) If the Pacman has eaten the pellet, then I basically add the foodScore and ghostScore, that is the Pacman will directly go for food and
                         the ghost
                      b) In other cases the ghostScore is subtracted and the foodScore is added. The weightage for foodScore is more, to make the pacman more optimistic in his search
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    ghostPositions = [states.getPosition() for states in newGhostStates]
    ScaredTime = [states.scaredTimer for state in newGhostStates]

    foodDistance = [util.manhattanDistance(newPos, x) for x in newFood.asList()]

    foodScore = 0
    if len(foodDistance):
        foodScore = min(foodDistance)

    ghostScore = 0
    for x in ghostPositions:
        ghostScore = ghostScore + util.manhattanDistance(newPos, x)

    finalScore = currentGameState.getScore()
    if (ScaredTime[0] > 10):
        finalScore = finalScore + 1 / foodScore + 1 / ghostScore
        return finalScore
    if ghostScore != 0 and foodScore != 0:
        finalScore = finalScore + 10 / foodScore - 1 / ghostScore
        return finalScore
    return finalScore

    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction

'''successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        positions = [GhostStates.getPosition()   for GhostStates in newGhostStates]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodDistance = [util.manhattanDistance(newPos,x) for x in newFood.asList()]
        foodScore = 0
        if len(foodDistance):
          foodScore = min(foodDistance)
        ghostScore = 0
        for x in positions:
          ghostScore = ghostScore+ util.manhattanDistance(newPos,x)
        finalScore = successorGameState.getScore()
        if newScaredTimes[0]>14 and foodScore!=0:
          finalScore = successorGameState.getScore()+10/foodScore
        if ghostScore != 0 and foodScore!=0 :
          finalScore= successorGameState.getScore()+ 10/foodScore - 1/ghostScore'''