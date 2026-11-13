import problems as prb
import algorithms as alg

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

STEPS = 40


    