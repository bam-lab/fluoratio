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
import re


# File selector
exp_loc = input("Enter the full filepath to the experiment directory (Mark_and_Find_NNN): ")
positions = os.listdir(exp_loc)
n_pos = len(positions)
position_regex = re.compile('Position.*')

for pos in positions:
    pos_filepath = exp_loc + '/' + pos
    timepoint = os.listdir(pos_filepath)
    for frame in timepoint:
        if not position_regex.search(frame):
            timepoint.remove(frame)
            metadata = os.listdir(pos_filepath + '/' + frame)
            # New function for file utilities to parse metadata xml file,
            # generate gif from colour merge of channels. See file_util.py
    print(metadata)
    print(timepoint)
    print(len(timepoint))
