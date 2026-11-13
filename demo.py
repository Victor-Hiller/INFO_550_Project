import problems as prb
import algorithms as alg
import matplotlib.pyplot as plt

'''
This file will contain the code needed to run a demonstration of your project. 

For the progress report, it should contain code that shows a brief demonstration of random agents attempting to solve each problem. 

For the final report, it should contain code that shows a brief demonstration of each algorithm attempting to solve each problem. 

In both cases, to make sure we can grade these all in time, please ensure that each demonstration is just long enough to show some
meaningful behavior. If your problem is chess playing, for example, you might show 5 moves from each player, where one player uses one 
algorithm and one player uses another. If your problem is snake, you might show game long enough for the player to eat two apples or die
(whichever comes first).

Scenarios:
1) No green-beard population
2) Green-beard population but no survival
3) Green-beard population with survival
'''
SCENARIOS = [
    {"label": "Scene 1", "overrides": {"gb_switch": False}, "seed": 0},
    {"label": "Scene 2", "overrides": {"gb_strt": 0.5, "gb_shr": 0.75}, "seed": 5},
    {"label": "Scene 3", "overrides": {"gb_strt": 0.8, "gb_shr": 1.0}, "seed": 16}
]

# Steps taken within a run, global
STEPS = 40

def run_scenario(scenario):
    """
    Runs one of the scenarios through run_env() to produce a scavenger run. Expects
    a scenario to have entries "overrides" and "seed" to run properly.
    Returns results from the run and parameters used.
    """
    params = {**prb.ENV_PARAMS, **alg.GA_PARAMS}
    params.update(scenario["overrides"])
    prey_h, pop_h, _, extra = prb.run_env(params, scenario["seed"], STEPS, record=True)
    
    return params, prey_h, pop_h, extra

def main():
    """
    Runs entire demo where it shows three scenarios of genetic algorithm populations.
        1) No green-beards, population goes extinct early on.
        2) Partial green-beard, where some of population are green-beards with some 
           sharing, survives a little longer but goes extinct.
        3) Green-beard, where most of the population are green-beards with high 
           sharing, population never extincts but plateaus. 
    Generates a histogram animation showing the effort levels for gathering and 
    population count. Then lastly, a plot of the population of prey and scavengers
    over the entire run per step.
    """
    print("Runs three separate scenarios for genetic algorithm environment."
          "\n Scenario 1) No green-beard population."
          "\n Scenario 2) Partial green-beard population."
          "\n Scenario 3) Green-beard population, survival.")

    for  scenario in SCENARIOS:
        print(scenario["label"])
        params, prey_h, pop_h, extra = run_scenario(scenario)
        anim = prb.animate_efforts(extra["genomes"], params, prey_h)
        plt.show()
        prb.plot_populations(prey_h, pop_h)

if __name__ == "__main__":
    main()