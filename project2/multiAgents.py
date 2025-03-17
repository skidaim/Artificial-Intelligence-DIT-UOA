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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        eval = successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        if (newScaredTimes[0] > 0):# eat the big dot.
            eval+=200
        
        if newFood.asList():
            mindistfood = min(util.manhattanDistance(foodpos, newPos) for foodpos in newFood.asList())
            eval += 4/mindistfood
        for ghoststate in newGhostStates:
            if (ghoststate.getPosition() == newPos and ghoststate.scaredTimer == 0):
                eval -= 9999999 # if we fall into a ghost, we lose, avoid that at all costs
                break
            if (ghoststate.scaredTimer > 0): # reward for getting close to scared ghosts, penalize for getting close to normal ghosts
                eval+=1/util.manhattanDistance(ghoststate.getPosition(), newPos)
            else:
                eval-=3/util.manhattanDistance(ghoststate.getPosition(), newPos)
        "*** YOUR CODE HERE ***"
        return eval

def scoreEvaluationFunction(currentGameState: GameState):
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
    


    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(state, depth, agentIndex):
            
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            if agentIndex == 0:
                return max(minimax(state.generateSuccessor(agentIndex, action), depth, 1) for action in state.getLegalActions(agentIndex))
            else:
                if (agentIndex + 1) == gameState.getNumAgents():# we're at the last ghost level, so we increment depth
                    depth += 1
                return min(minimax(state.generateSuccessor(agentIndex, action), depth, (agentIndex + 1)%gameState.getNumAgents()) for action in state.getLegalActions(agentIndex))
                                                                                        #this will cycle through the valid indices of the agents
        return max(gameState.getLegalActions(0), key=lambda action: minimax(gameState.generateSuccessor(0, action), 0, 1))
            
        #util.raiseNotDefined()  

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(state, depth, agentIndex, alpha, beta):
            
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            if agentIndex == 0:
                v = float('-inf')

                for action in state.getLegalActions(agentIndex):
                    v = max(v, alphabeta(state.generateSuccessor(agentIndex, action), depth, 1, alpha, beta))
                    if v > beta:
                        return v
                    alpha = max(alpha, v)
                return v
            else:
                v = float('inf')
                if (agentIndex + 1) == gameState.getNumAgents():
                    depth += 1
                
                for action in state.getLegalActions(agentIndex):
                    v = min(v, alphabeta(state.generateSuccessor(agentIndex, action), depth, (agentIndex + 1)%gameState.getNumAgents(), alpha, beta))
                    if v < alpha:
                        return v
                    beta = min(beta, v)
                return v
            
            
        
        maxscore = float('-inf')
        baction = None
        alpha = float('-inf')

        for action in gameState.getLegalActions(0):  
            successor = gameState.generateSuccessor(0, action)
            score = alphabeta(successor, 0, 1, alpha, float('inf')) # we only care about alpha for the MAX player
            if score > maxscore:
                maxscore = score
                baction = action
            alpha = max(alpha, score) # alpha is the MAX's best option on path to root so we update that

        return baction
        
            
            
                    
            
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            if agentIndex == 0:
                return max(expectimax(state.generateSuccessor(agentIndex, action), depth, 1) for action in state.getLegalActions(agentIndex))
            else:
                if (agentIndex + 1) == gameState.getNumAgents():
                    depth += 1
                return sum(expectimax(state.generateSuccessor(agentIndex, action), depth, (agentIndex + 1)%gameState.getNumAgents()) for action in state.getLegalActions(agentIndex))/len(state.getLegalActions(agentIndex))
                

        return max(gameState.getLegalActions(0), key=lambda action: expectimax(gameState.generateSuccessor(0, action), 0, 1))


        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    eval = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if (newScaredTimes[0] > 0): # eat the big dot.
        eval+=200
    
    if newFood.asList():
        mindistfood = min(util.manhattanDistance(foodpos, newPos) for foodpos in newFood.asList())
        eval += 4/mindistfood
    for ghoststate in newGhostStates:
        if (ghoststate.getPosition() == newPos and ghoststate.scaredTimer == 0):
            eval -= 9999999 # if we fall into a ghost, we lose, avoid that at all costs
            break
        if (ghoststate.scaredTimer > 0): # reward for getting close to scared ghosts, penalize for getting close to normal ghosts
            eval+=1/util.manhattanDistance(ghoststate.getPosition(), newPos)
        else:
            eval-=3/util.manhattanDistance(ghoststate.getPosition(), newPos)
    
    return eval


# Abbreviation
better = betterEvaluationFunction
