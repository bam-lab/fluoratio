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

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fluo_ratio = pd.read_csv('Results/results.csv')
print("WIDE")
print(fluo_ratio)
y_label = "Nucleus to Cytoplasm Fluorescence Ratio, n.u."

fluo_ratio_long = pd.wide_to_long(fluo_ratio,
                                  stubnames=["t", "r", "ar", "ca", "na"],
                                  i="Position",
                                  j="Frame",
                                  sep="",
                                  suffix="\\d+")
fluo_ratio_long = fluo_ratio_long.reset_index()
# Have to reset index of dataframe after converting to long format
print("LONG")
print(fluo_ratio_long)

# size_factor = 6
# aspect_ratio = [2, 1]
# plt.figure(figsize=[size_factor * x for x in aspect_ratio])

# sns.set_context("poster")         # talk, paper, or poster
# sns.set_style("whitegrid", {"axes.linewidth": 0.75,
#                             "font": "Helvetica",
#                             'axes.edgecolor': '0',
#                             'grid.color': '0.9'})  # 0 = black, 1 = white


# lmplot for hues, regplot for single positions

plot = sns.lmplot(x="t",
                  y="r",
                  hue="Position",
                  fit_reg=False,
                  data=fluo_ratio_long)

plot = (plot.set_axis_labels("Time (min)",
                             "Nucleus to Cytoplasm Fluorescence Ratio" +
                             " (no units)"))
plot = sns.set_context("poster")
plot = sns.set_style("white", {"axes.linewidth": 0.75,
                               "font": "Helvetica",
                               'axes.edgecolor': '0'})  # 0 = black, 1 = white)

# sns.boxplot(x="Drug",
#             y=y_label,
#             linewidth=0.75,
#             boxprops={'facecolor': 'None'},
#             data=fluo_ratio)

# plt.legend().set_visible(False)
plt.savefig("Results/fluo_ratio.png")
plt.savefig("Results/fluo_ratio.svg")
plt.show()
