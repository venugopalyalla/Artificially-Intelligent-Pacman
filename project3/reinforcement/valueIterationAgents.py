# valueIterationAgents.py
# -----------------------
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


import mdp, util
import qlearningAgents

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(0,self.iterations):
          tmpValues = util.Counter()
          for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
              tmpValues[state] = 0
            else:
              best = float('-Inf')
              actions = self.mdp.getPossibleActions(state)
              for action in actions:
                total = self.getTotalValue(state,action)
                best = max(total, best)
                tmpValues[state] = best
          self.values = tmpValues

    def getTotalValue(self, state, action):
        total = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            total += prob * (self.mdp.getReward(state, action, nextState) + (self.discount * self.values[nextState]))
        return total

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        return self.getTotalValue(state,action)

    def computeBestQValue(self, state):
        actions = self.mdp.getPossibleActions(state)
        bestQVal = float('-Inf')
        #iterated through all the actions and best q value is stored
        for action in actions:
          if self.getQValue(state,action) > bestQVal:
            bestQVal = self.getQValue(state,action)
        return bestQVal

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        #bestvalue is initiated with negative infinity
        #iterated over each action to obtain best value
        #the policy with the best value is returned
        bestValue = self.computeBestQValue(state)
        policy = None
        for action in self.mdp.getPossibleActions(state):
            qValue = self.computeQValueFromValues(state, action)
            if qValue == bestValue:
                policy = action
        return policy

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
