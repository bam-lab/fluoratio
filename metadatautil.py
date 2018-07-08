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

# New functions for file utilities to parse metadata xml file,

# In another module called results?:
# generate gif from colour merge of channels
# csv generation?
# plot generation?

import xml.etree.ElementTree as ET
from datetime import datetime


# Get first absolute time for a position.
def get_time(mdpath, frame):
    tree = ET.parse(mdpath)
    root = tree.getroot()
    date = root[0][3][frame].attrib['Date']
    timestring = root[0][3][frame].attrib['Time']
    ms = root[0][3][frame].attrib['MiliSeconds']
    timestamp = "{0} {1} ".format(
        date, timestring) + '{:03d} EST'.format(int(ms))
    # Parse "hh:mm:ss ms" string into its components
    #print(timestamp)
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S %p %f %Z")


# Get scale in microns per pixel
def get_scale(mdpath):
    tree = ET.parse(mdpath)
    root = tree.getroot()
    scale = root[0][2][4][0].attrib['Voxel']
    return float(scale)
