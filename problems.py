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
ENV_PARAMS = {
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
   # Green beard:
   "gb_shr": 0.5,          # fraction of each beard's food put into share pool
}

def step_prey(prey, efforts, params):
    total_def = np.sum(1 - efforts)
    real_pred = max(0, params["base_pred"] - total_def * params["def_str"])
    grw_prey = params["grw_rate"] * prey * (1 - prey / params["carry_cap"])
    new_prey = prey + grw_prey - real_pred
    return max(0, new_prey)






