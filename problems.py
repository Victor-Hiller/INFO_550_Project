'''
Scavenger environment, logistic prey population that is attacked
by predation. Scavengers expend effort either gathering waste for
food or defending prey, defense is shared while food is private.
Toggle for green-beard allows beard population to share food with
each other.
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from algorithms import GA_PARAMS, create_population, next_gen

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

def share_food(food, genomes, params):
   """
   Only when green-beard population (bearders) is present, this function is used to 
   distributedcfood amongst them. Portion of each bearder's food is taken equal to
   gb_shr, this amount is added to a pool. This total pool is then shared among
   all the bearders equally. Returns whole food pool after sharing.
   """
   bearders = genomes[:,1] > 0.5
   n_bearders = np.sum(bearders)

   if n_bearders == 0:
      return food

   new_food = food.copy()
   given = params["gb_shr"] * new_food[bearders]
   shr_pool = np.sum(given)
   new_food[bearders] = new_food[bearders] - given + shr_pool / n_bearders
   return new_food

def run_env(params, seed, steps, record=True):
   """
   Runs the environment with a random seed and selected amount of steps, note params
   must be dictionary {**ENV_PARAMS, **GA_PARAMS}, and toggle for recording genome. 
   Start of function generates the scavenger population with either fixed or randomized
   effort (toggled with rand_eff). If record=True, the genomes each step for the 
   population will be recorded and returned at the end.
   After runs through steps in the following order:
      - Prey population calculation
      - Food pool distribution (sharing only if gb_switch=True)
      - Next generation of scavengers
      - Population statistics
   
   After each step statistics for that step are added to lists, three lists and a 
   dictionary are returned as the result. The following statistics are returned:
      - prey_h: Population of prey
      - pop_h: Population of scavengers
      - mean_h: Mean effort of population
      * Dictionary statistics
      - beard_h: Fraction of population that are green-beards
      - beff_h: Mean effort of bearders
      - neff_h: Mean effort of non-bearders
      - gene_h: History of population's genome throughout run
   """
   np.random.seed(seed)

   genomes = create_population(params)

   prey = params["prey_strt"]
   prey_h, pop_h, mean_h, beard_h, beff_h, neff_h, gene_h = [], [], [], [], [], [], []

   if record:
      gene_h.append(genomes)

   for t in range(steps):
      efforts = genomes[:,0]
      prey = step_prey(prey, efforts, params)
      food = scav_effort_to_food(prey, efforts, params)
      if params["gb_switch"]:
         food = share_food(food, genomes, params)

      genomes = next_gen(genomes, food, params)

      if record:
         gene_h.append(genomes)

      prey_h.append(prey)
      pop_h.append(len(genomes))
      mean_h.append(np.mean(genomes[:,0]) if len(genomes) > 0 else np.nan)

      bearders = genomes[:,1] > 0.5
      beard_h.append(np.mean(bearders) if len(genomes) > 0 else np.nan)
      beff_h.append(np.mean(genomes[bearders, 0]) if bearders.any() else np.nan)
      neff_h.append(np.mean(genomes[~bearders, 0]) if (~bearders).any() else np.nan)

      if len(genomes) == 0:
         break

   return prey_h, pop_h, mean_h, {"beard": beard_h, "beff": beff_h, "neff": neff_h, "genomes": gene_h}

def plot_populations(prey_h, pop_h):
   """
   Plot population for both prey and scavengers for a run.
   """
   fig, ax1 = plt.subplots()
   ax1.plot(prey_h, color='blue', label='Prey population')
   ax1.set_xlabel('Steps')
   ax1.set_ylabel('Prey population')
   ax1.set_ylim(bottom=0)

   ax2 = ax1.twinx()
   ax2.plot(pop_h, color='red', label='Scavenger population')
   ax2.set_ylabel('Scavenger population')
   ax2.set_ylim(bottom=0)

   lines1, labels1 = ax1.get_legend_handles_labels()
   lines2, labels2 = ax2.get_legend_handles_labels()
   ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

   plt.title('Prey and Scavenger Population For Run.')
   plt.show()
   return fig

def animate_efforts(genomes, params, prey_h):
   """
   Generates a live display of histogram depicting effort of gathering for both
   green beards and non-green breard populations. Shows the total population count
   for both scavengers and prey population within the title. Also shows threshold
   lines for gathering effort maximum and minimum.
   """
   fig, ax = plt.subplots()
   bins = np.linspace(0, 1, 21)
   ylim = max(len(g) for g in genomes)

   def update(frame):
      ax.clear()
      ax.set_ylim(0, ylim)
      ax.set_xlim(0, 1)
      g = genomes[frame]
      if len(g) == 0:
         ax.text(0.5, 0.5, 'Population Extinct', transform=ax.transAxes, ha='center')
         ax.set_title(f'Step {frame}: Population now extinct')
         return
      
      beards = g[:,1] > 0.5
      b_eff = g[beards, 0]
      nb_eff = g[~beards, 0]

      if frame > 0:
         prey_text = f'prey population: {prey_h[frame - 1]:.1f}'
      else:
         prey_text = f'prey population: {params["prey_strt"]:.1f}'

      ax.hist(b_eff, bins=bins, alpha=0.6, label='bearders effort')
      ax.hist(nb_eff, bins=bins, alpha=0.6, label='non-bearder effort')
      ax.axvline(params["gthr_min"], linestyle='--', label='Minimum effort for gathering')
      ax.axvline(params["gthr_max"], linestyle='--', label='Maximum effort for gathering')
      ax.legend()
      ax.set_xlabel("Effort (fraction spent gathering)")
      ax.set_ylabel("Scavenger count")
      ax.set_title(f'Step {frame} | scavenger population: {len(g)}, {prey_text}')


   animation = FuncAnimation(fig, update, frames=len(genomes), interval=400, repeat=False)
   return animation 