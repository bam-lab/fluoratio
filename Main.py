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
import os
import re
from fnmatch import fnmatch
import multiprocessing as mp
import time

import imgutil as iu
import metadatautil as mu

start = time.time()

# File selector
# exp_loc = input("Enter the full filepath to the experiment directory" +
#                 " (Mark_and_Find_NNN): ")
exp_loc = "/home/jidicula/johanan/prog/test/Mark_and_Find_003"
# n_frames = int(input("Number of frames in a sequence: "))
# nuc_channel = input("Which channel has the NLS protein? ch00/ch01/ch02")
# poi_channel = input("Which channel has the POI? ch00/ch01/ch02")
nuc_channel = "ch01"
poi_channel = "ch00"
n_frames = 71
cpu_num = int(mp.cpu_count()) - 1  # Be nice, leave 1 processor free.


def analyzer(filepath_prefix):
    analysis_start = time.time()
    print("Analyzing {}".format(filepath_prefix))
    # filepath construction
    poi_filepath = filepath_prefix + '_' + poi_channel + '.tif'
    nuc_filepath = filepath_prefix + '_' + nuc_channel + '.tif'
    # timestamp generation
    # Need to retrieve first time from first_time.txt
    with open("first_time.txt", "r") as time_read_f:
        first_time_string = time_read_f.read()
    first_time = dt.datetime.strptime(first_time_string,
                                      "%Y-%m-%d %H:%M:%S.%f")
    position_name = filepath_prefix.split("/")[-2]
    metadata_path = re.sub("Position\d{3}_t.*", '', filepath_prefix) + \
        "MetaData/" + position_name + "_Properties.xml"
    frame_num = filepath_prefix.split("_")[-1].split("t")[-1]
    timestamp = mu.get_time(metadata_path, int(frame_num))
    elapsed_time = timestamp - first_time
    if elapsed_time.days < 0:
        elapsed_time = dt.timedelta(0, elapsed_time.seconds,
                                    elapsed_time.microseconds)
    assert_warning = ("elapsed_time is not a timedelta: "
                      "%r" % elapsed_time)
    assert type(elapsed_time) is dt.timedelta, assert_warning
    # mask generation
    poi_mask = iu.mask_gen(poi_filepath)[-1]
    nuc_mask = iu.mask_gen(nuc_filepath)[-1]
    # segmentation
    cytoplasm, nucleus = iu.mask_segmenter(nuc_mask, poi_filepath)
    try:
        fluo_ratio = round(float(nucleus) / float(cytoplasm), 3)
    except ZeroDivisionError:
        fluo_ratio = 0
    poi_label = iu.img_labeler(poi_mask)
    poi_area = iu.area_measure(poi_label)
    poi_aspect_ratio = round(iu.aspect_ratio(poi_label), 3)
    nuc_area = iu.area_measure(iu.img_labeler(nuc_mask))
    minutes = round(elapsed_time.seconds/60.0, 3)
    print(poi_filepath, "\n", nuc_filepath)
    # Writes to Results/PositionXXtYY.csv in the form:
    # minutes, fluorescence ratio, POI aspect ratio, POI area, nucleus area
    results_filename = "Results/" + \
        position_name + '_t' + str(frame_num) + 'csv'
    with open(results_filename, "w") as result_csv:
        result_csv.write(str(minutes) + "," + str(fluo_ratio) + "," +
                         str(poi_aspect_ratio) + "," + str(poi_area) +
                         "," + str(nuc_area))
    analysis_end = time.time()
    analysis_time = round((analysis_end - analysis_start)/60, 3)
    print("Wrote {0} in {1} minutes.".format(results_filename, analysis_time))


positions = glob.glob(exp_loc + '/Position*')  # list of full filepaths
positions.sort()
n_pos = len(positions)
print(positions[0])
first_md_path = glob.glob(positions[0] + "/MetaData/*_Properties.xml")
first_time = mu.get_time(first_md_path[0], 0)

with open("first_time.txt", "w") as first_time_f:
    first_time_f.write(str(first_time))


pattern = "*.tif"
img_filepaths = []
for path, subdirs, files in os.walk(exp_loc):
    for name in files:
        if fnmatch(name, pattern):
            img_filepaths.append(os.path.join(path, name))
for k, filepath in enumerate(img_filepaths):
    new_filepath = re.sub('_ch.*', '', filepath)
    img_filepaths[k] = new_filepath

# Making the process worker pool.
if __name__ == '__main__':
    with mp.Pool(processes=(cpu_num)) as pool:
        pool.map(analyzer, img_filepaths)

# Coalesce all the result csv files into one
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
# TODO: read in all mini csv files into main results.csv
# Subdivide into position sublists, then read each one individually?
position_filenames = []
for position in positions:
    position_filenames.append(position.split('/')[-1])

for idx, position_fn in enumerate(position_filenames):
    position_results = []
    for l in range(n_frames):
        result_filepath = str("Results/", position_fn,
                              't{:03d}.csv'.format(int(l)),)
        with open(result_filepath, "r") as result_f:
            contents = result_f.read()
        position_data = re.sub('\]', '', re.sub('\[', '', str(contents)))
        position_data = re.sub(' ', '', position_data)
        position_results.append(position_data, ',')
    position_results_str = re.sub(
        '\]', '', re.sub('\[', '', str(position_results)))
    position_results_str = re.sub(' ', '', position_results_str)
    with open("Results/results.csv", "a") as fi:
        fi.write(str(idx + 1) + ',' + position_results_str + '\n')

end = time.time()
print("Runtime:", str((end-start)/3600.0), "hours")
