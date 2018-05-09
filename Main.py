#import skimage as sk
#import numpy as np
#import seaborn as sb
import os


# File selector
exp_loc = input("Enter the full filepath to the experiment directory (Mark_and_Find_NNN): ")
positions = os.listdir(exp_loc)
n_pos = len(positions)

for pos in positions:
    for frame in os.listdir(exp_loc + '/' + positions[pos]):
        print(frame)
