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
   """
   Prey step where the prey population either grows (when prey growth beats 
   predation) or shrinks (when predation exceeds prey growth). Returns the max 
   between 0 and new_prey.
   """
   total_def = np.sum(1 - efforts)
   real_pred = max(0, params["base_pred"] - total_def * params["def_str"])
   grw_prey = params["grw_rate"] * prey * (1 - prey / params["carry_cap"])
   new_prey = prey + grw_prey - real_pred
   return max(0, new_prey)

def scav_effort_to_food(prey, efforts, params):
   """
   Turns the scavengers' efforts into food based on the total amount of prey
   (food_pool = wste_per_prey * prey). Assigns food based off the level of effort 
   a scavenger puts towards gathering food. There are three tiers of demands that 
   the scavengers can fall into.
      - bot_tier: where no food is demanded by the scavenger (effort < gthr_min)
        * implicit, not represented as a variable
      - mid_tier: where only one food is demanded (gthr_min <= effort < gthr_max)
      - top_tier: where more food is demanded to reproduce in the range top_food_min 
        to top_food_max, this amount grows geometrically with effort (effort >= gthr_max)

   Once demands for food have been assigned it is then distributed, with highest 
   effort first until pool runs out. The function then returns an array of food 
   amounts received by each scavenger.
   """
   mid_tier = (efforts >= params["gthr_min"]) & (efforts < params["gthr_max"])
   top_tier = efforts >= params["gthr_max"]

   demands = np.zeros(len(efforts))
   demands[mid_tier] = 1

   top_eff = (efforts[top_tier] - params["gthr_max"]) / (1 - params["gthr_max"])
   base = params["top_food_max"] / params["top_food_min"]
   demands[top_tier] = params["top_food_min"] * base ** top_eff

   food_pool = prey * params["wste_per_prey"]
   order = np.argsort(efforts)[::-1]
   food = np.zeros(len(efforts))

   for i in order:
      give = min(demands[i], food_pool)
      food[i] = give
      food_pool = food_pool - food[i]

   return food
