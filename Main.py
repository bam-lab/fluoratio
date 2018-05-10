# Copyright 2018 Johanan Idicula

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#import skimage as sk
#import numpy as np
#import seaborn as sb
import os


# File selector
exp_loc = input("Enter the full filepath to the experiment directory (Mark_and_Find_NNN): ")
positions = os.listdir(exp_loc)
n_pos = len(positions)

for pos in positions:
    for frame in os.listdir(exp_loc + '/' + pos):
        print(frame)
