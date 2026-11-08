'''
Contains genetic algorithm code for the scavenger agent.

Population:
Scavenger agents make up a population that collects waste from prey to survive
and reproduce and defends the prey from predators. Prey and predators are not
agents but only a logistic equation.

Effort:
Scavenger's can either all start with a fixed effort or a randomized starting 
effort. Effort determines how much the agent either gathers waste or defends
prey in a step.

Genetic operators:
  - Selection: Agent selection for survival and breeding determined by how much
    effort an agent allocated towards food gathering (more effort more food) 
  - Crossover: Genetic information from each parent is combined into an offspring
    by being average.
  - Mutation: A distortion from the passed down genetics through a standard deviation
    of Guassian noise.

Green-beard:
A subpopulation of the scavengers that has the green-beard gene. In this population
green-beards when gathering food share their food in a pool that is then equally split
among the green-beard population.
'''
import random

class RandomAgent:
  def __str__(self):
    return "Random Agent"
  def getMove(self, problem):
    moves = problem.getLegalMoves()
    return moves[random.randrange(len(moves))]
  
