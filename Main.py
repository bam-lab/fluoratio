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
import datetime as dt
import glob

import imgutil as iu
import metadatautil as mu


# File selector
# exp_loc = input("Enter the full filepath to the experiment directory" +
#                 " (Mark_and_Find_NNN): ")
exp_loc = "/home/jidicula/johanan/prog/test/Mark_and_Find_001"
# n_frames = int(input("Number of frames in a sequence: "))
# nuc_channel = input("Which channel has the NLS protein? ch00 or ch01 ")
nuc_channel = "ch01"
n_frames = 71
positions = glob.glob(exp_loc + '/Position*')  # list of full filepaths
positions.sort()
n_pos = len(positions)
print(positions[0])
first_time = mu.get_time(positions[0] + "/MetaData/Position001_Properties.xml",
                         0)
# print(timeshift)
print("hello there")
with open("Results/results.csv", "w") as f:
    f.write("Position")
    for i in range(n_frames):
        f.write(",t" + str(i))  # time
        f.write(",r" + str(i))  # fluorescence ratio
        f.write(",ar" + str(i))  # aspect ratio
        f.write(",ca" + str(i))  # cell area
        f.write(",na" + str(i))  # nucleus area
    f.write("\n")
    # Iterates through positions in mark & find experiment
    for index, pos in enumerate(positions):
        time_series = glob.glob(pos + '/' + '*.tif')  # list of full filepaths
        time_series.sort()
        metadata_dir = pos + '/MetaData/'
        f.write(str(index + 1) + ',')
        # iterate through time series for position
        for idx, frame in enumerate(time_series):  # this counts each channel
            timestamp = mu.get_time(
                metadata_dir +
                str(pos.split('/')[-1]) + '_Properties.xml', idx)
            # print(str(timestamp) + " " + str(pos) + " " + str(frame))
            if idx % 2 == 0:
                elapsed_time = timestamp - first_time
                if elapsed_time.days < 0:
                    elapsed_time = dt.timedelta(0, elapsed_time.seconds,
                                                elapsed_time.microseconds)
                assert_warning = ("elapsed_time is not a timedelta: "
                                  "%r" % elapsed_time)
                assert type(elapsed_time) is dt.timedelta, assert_warning
                if nuc_channel == "ch01":
                    poi_filepath = time_series[idx]
                    nuc_filepath = time_series[idx + 1]
                else:
                    poi_filepath = time_series[idx + 1]
                    nuc_filepath = time_series[idx]
                # area and aspect ratio
                poi_mask = iu.mask_gen(poi_filepath)[-1]
                # area and segmentation
                nuc_mask = iu.mask_gen(nuc_filepath)[-1]
                cytoplasm, nucleus = iu.mask_segmenter(nuc_mask, poi_filepath)
                try:
                    fluo_ratio = round(float(nucleus.sum()) /
                                       float(cytoplasm.sum()), 3)
                except ZeroDivisionError:
                    fluo_ratio = 0
                poi_label = iu.img_labeler(poi_mask)
                poi_area = iu.area_measure(poi_label)
                poi_aspect_ratio = round(iu.aspect_ratio(poi_label), 3)
                nuc_area = iu.area_measure(iu.img_labeler(nuc_mask))
                minutes = round(elapsed_time.seconds/60.0, 3)
                print(poi_filepath + "\n" + nuc_filepath)
                f.write(str(elapsed_time.seconds/60.0) + ',')
                f.write(str(fluo_ratio) + ',')
                f.write(str(poi_aspect_ratio) + ',')
                f.write(str(poi_area) + ',')
                f.write(str(nuc_area) + ',')
            f.write('\n')
        # print(time_series)
    #       print('frames:' + len(time_series))
    # print(positions)
