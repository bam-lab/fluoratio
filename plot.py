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

sns.lmplot(x="t",
           y="r",
           hue="Position",
           fit_reg=False,
           data=fluo_ratio_long)

# sns.boxplot(x="Drug",
#             y=y_label,
#             linewidth=0.75,
#             boxprops={'facecolor': 'None'},
#             data=fluo_ratio)

# plt.legend().set_visible(False)
# plt.savefig("fluo_ratio_2-1.png")
plt.show()
