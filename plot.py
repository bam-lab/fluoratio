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
import matplotlib as mpl
import seaborn as sns
import re

fluo_ratio = pd.read_csv('./Results/results.csv')
print("WIDE")
print(fluo_ratio)


def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        if re.match("(f\d+)", feature_name):
            avg = df.filter(regex="(f\d+)").mean(axis=1)
            result[feature_name] = df[feature_name]/avg
    return result


fluo_ratio_norm = normalize(fluo_ratio)
print(fluo_ratio_norm)

# normalized_fluo_ratio = fluo_ratio.divide(means["r"])

fluo_ratio_long = pd.wide_to_long(fluo_ratio_norm,
                                  stubnames=["t", "f", "ar", "ca", "na"],
                                  i="Cell",
                                  j="Frame",
                                  sep="",
                                  suffix="\\d+")
fluo_ratio_long = fluo_ratio_long.reset_index()
# Have to reset index of dataframe after converting to long format
print("LONG")
print(fluo_ratio_long)

drug_in = 18.0
drug_out = 87.0

size_factor = 6
aspect_ratio = [1.5, 4]

sns.set(font_scale=2,rc={'figure.figsize': [size_factor * x for x in aspect_ratio]})
sns.set_style("white", {"axes.linewidth": 0.75,
                        'axes.edgecolor': '0'})  # 0 = black, 1 = white)
mpl.rcParams['font.family'] = "TeX Gyre Heros"

lm = sns.lmplot(x="t",
                y="f",
                hue="Cell",
                fit_reg=False,
                legend_out=False,
                data=fluo_ratio_long, scatter_kws={"zorder": 2, "s": 25})

axes = lm.axes

axes[0, 0].set_ylim(0, )

drug = plt.axvspan(drug_in, drug_out, color='#5D6465', alpha=0.3, lw=0,
                   zorder=1)
plt.legend([drug], ["CytoD"], loc='upper right', bbox_to_anchor=(1.3, 1.0))

plt.xlabel("Time (min)", size=28)
plt.ylabel("Nucleus to Cytoplasm\nFluorescence Ratio Change\n(no units)", size=28)
plt.xticks(size=20)
plt.yticks(size=20)
# plt.setp(lm.get_legend().get_texts(), fontsize='12')  # for legend text
# plt.setp(lm.get_legend().get_title(), fontsize='12')  # for legend title

plt.savefig("Results/fluo_ratio.png")
plt.savefig("Results/fluo_ratio.svg")
plt.show()
