'''
Contains genetic algorithm code for the scavenger agent.

Population:
Scavenger agents make up a population that collects waste from prey to survive
and reproduce and defends the prey from predators. Prey follows a logistic growth,
that is subtracted by predation which defense is able to reduce.

Effort:
Scavengers can either all start with a fixed effort or a randomized starting 
effort. Effort determines the fraction of their energy spent towards gathering
while the remainder goes towards defense (1 - effort = defense).

Genome:
Each scavenger has two genes, one for effort (continuous number between 0 and 1)
and one for having green-beard (0 no beard 1 has beard).

Genetic operators:
  - Selection: Agent selection is done through both survival and breeding. Surviving
    occurs when a scavenger has at least one (rounded) food at the end of a step. 
    Breeding occurs when a scavenger is deemed a parent by having two or more (rounded)
    food by the end of the step. Each food beyond the two food allows for an extra slot
    for offspring, all the parents are pooled together and paired within this pool.
  - Crossover: Uses intermediate crossover, where information from each parent is
    combined into an offspring by being average.
  - Mutation: Mutation is done by adding Gaussian noise that is added to the offspring's 
    effort and clipped to [0,1].


Green-beard:
A subpopulation of the scavengers that has the green-beard gene. In this population
green-beards have a trait of sharing with each other. This means that once they have 
gathered, a fraction of it is split into a communal pool that is equally shared across
all green-beards. This genetic trait is inherited from a single parent and has the 
probability to be flipped.
'''
import random
import numpy as np

GA_PARAMS = {
  # Scavenger parameters
  "scav_strt": 20,    # starting population of scavengers
  "scav_eff": 0.75,   # effort amount for population when fixed
  "mut_sd": 0.03,     # gaussian noise added to offspring's effot
  "rand_eff": True,   # switch for randomizing effort at start, random is uniform in [0,1]
  # Green-beard
  "gb_switch": True,  # switch for toggling on and off green-beard population
  "gb_strt": 0.2,     # fraction of starting population that has green-beard
  "gb_flip": 0.01,    # probability of flipping beard gene in both directions
}

def create_fixed_effort(n, effort):
  """Returns array of n effort values."""
  return np.full(n, effort)
 
def create_random_efforts(n):
  """Returns array of n uniform random effort values."""
  return np.random.uniform(0, 1, size=n)

def create_population(params):
  """
  Generates scavenger population for start of run. 
  When rand_eff=True, scavengers have a uniform random effort at start,
  however, when rand_eff=False all scavengers start with a fixed effort.
  When gb_switch=True, this allows for the start to contain a subpopulation
  of green-beard scavengers, when gb_switch=False, there are no green-beards
  at the start.
  This returns an array with the shape of (scav_strt, 2), column 0 contains 
  effort (float in [0,1]) and column 1 contains beard (0.0 or 1.0).
  """
  if params["rand_eff"]:
    efforts = create_random_efforts(params["scav_strt"])
  else:
    efforts = create_fixed_effort(params["scav_strt"], params["scav_eff"])

  if params["gb_switch"]:
    beards = (np.random.random(params["scav_strt"]) < params["gb_strt"]).astype(float)
  else:
    beards = np.zeros(params["scav_strt"])

  genomes = np.column_stack([efforts, beards])
  return genomes

class RandomAgent:
  def __str__(self):
    return "Random Agent"
  def getMove(self, problem):
    moves = problem.getLegalMoves()
    return moves[random.randrange(len(moves))]
  
