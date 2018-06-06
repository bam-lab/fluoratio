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

# import skimage as sk
# import numpy as np
# import seaborn as sb
# import re
import glob
import datetime
import metadatautil as mu
import imgutil as iu


# File selector
# exp_loc = input("Enter the full filepath to the experiment directory" +
#                 " (Mark_and_Find_NNN): ")
exp_loc = "/Users/johanan/prog/test/Mark_and_Find_001"
# n_frames = int(input("Number of frames in a sequence: "))
n_frames = 71
positions = glob.glob(exp_loc + '/Position*')  # list of full filepaths
n_pos = len(positions)

first_time = mu.get_time(positions[0] + "/Metadata/Position001_Properties.xml", 0)

# print(timeshift)
print("hello")

with open("results.csv", "w") as f:
    f.write("Position")
    for i in range(n_frames):
        f.write(",t" + str(i))  # time
        f.write(",r" + str(i))  # fluorescence ratio
        f.write(",ar" + str(i))  # aspect ratio
        f.write(",ca" + str(i))  # cell area
        f.write(",na" + str(i))  # nucleus area
    f.write("\n")

for pos in positions:
    time_series = glob.glob(pos + '/' + '*.tif')  # list of full filepaths
    metadata_dir = pos + '/MetaData/'
    for idx, frame in enumerate(time_series):  # this counts each channel
        timestamp = mu.get_time(metadata_dir +
                                str(pos.split('/')[-1]) +
                                '_Properties.xml',
                                idx)
        # print(str(timestamp) + " " + str(pos) + " " + str(frame))
        if idx % 2 == 0:
            elapsed_time = timestamp - first_time
            if elapsed_time.days < 0:
                elapsed_time = datetime.timedelta(0,
                                                  elapsed_time.seconds,
                                                  elapsed_time.microseconds)
            # New function for file utilities to parse metadata xml
            # file, generate gif from colour merge of channels.
            assert type(elapsed_time) is datetime.timedelta, "elapsed_time is not a timedelta: %r" % elapsed_time

            ch00_filepath = time_series[idx]
            ch01_filepath = time_series[idx+1]
            ch00_mask = iu.mask_gen(ch00_filepath)[-1]
            ch01_mask = iu.mask_gen(ch01_filepath)[-1]
            print(ch00_filepath + "\n" + ch01_filepath)
    # print(time_series)
#       print('frames:' + len(time_series))
# print(positions)
