'''
Scavenger environment, logistic prey population that is attacked
by predation. Scavengers expend effort either gathering waste for
food or defending prey, defense is shared while food is private.
Toggle for green-beard allows beard population to share food with
each other.
'''

import numpy as np

# Prey and predation parameters:
# prey_strt, base_pred, grd_str, grw_rate, carry_cap
PARAMS = {
    #Prey and predation:
    "prey_strt": 50,       # starting population of prey
    "base_pred": 15,       # number of prey eaten per step
    "def_str": 0.5,        # unit of defense that cancels amount of predation
    "grw_rate": 0.5,       # rate of logisitic growth of prey population
    "carry_cap": 100,      # growth slows as prey approaches this number
   # Food allocation:
   "wste_per_prey": 1,     # amount of waste made by a single prey
   "gthr_min": 0.4,        # minimum effort threshold for gathering
   "gthr_max": 0.75,       # maximum effort threshold for gathering
   "top_food_min": 2,      # minimum amount of food for top demand
   "top_food_max": 5,      # maximum amount of food for top demand
   # Population and genetics:
   "scav_strt": 20,        # scavenger starting population
   "scav_eff": 0.75,       # starting effort for scavengers when not randomized
   "mut_sd": 0.03,         # mutation standard deviation (Gaussian noise)
   # Green beard:
   "gb_switch": False,     # toggle for green-beard gene
   "gb_strt": 0.2,         # fraction of starting population that are green-beard
   "gb_shr": 0.5,          # fraction of each beard's food put into share pool
   "gb_flip": 0.01,        # probability that each offspring's beard flips (both directions)
}


