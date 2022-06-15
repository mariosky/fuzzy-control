import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import scikit_posthocs as sp
results = pd.read_csv('results.csv')

algorithms = ["GA", "PSO", "AO", "GWO", "AOA", "HS"]
print(stats.shapiro(results.GA))
print(stats.friedmanchisquare(results.GA, results.PSO, results.AO, results.GWO))
print(sp.posthoc_nemenyi_friedman(results ))
print(results.melt())
heatmap_args = {'linewidths': 0.25, 'linecolor': '0.5', 'clip_on': False, 'square': True}
#sp.sign_plot(sp.posthoc_wilcoxon(results.melt(), val_col='value', group_col='variable'), **heatmap_args)
print(sp.posthoc_mannwhitney(results.melt(), val_col='value', group_col='variable', alternative="less"))

#print(stats.mannwhitneyu(results.PSO, results.AOA, alternative="less"))
#print(stats.ttest_ind(results.PSO, results.AOA, alternative="less"))
#print(sp.posthoc_wilcoxon(results.melt(), val_col='value', group_col='variable'))
#print(sp.posthoc_ttest(results.melt(), val_col='value', group_col='variable'))
for alg1 in algorithms:
    print(alg1, end=" ")
    for alg2 in algorithms:
        if alg1 != alg2:
            print(stats.mannwhitneyu(results[alg1], results[alg2], alternative="two-sided")[1], end=" ")
            #print("{} < {}".format(alg1, alg2), p_value)
        else:
            print(1.0, end=" ")
    print()
# for alg1 in algorithms:
#     for alg2 in algorithms:
#         if alg1 != alg2:
#             p_value = stats.ttest_ind(results[alg1], results[alg2], alternative="two-sided")[1]
#             print("{} = {}".format(alg1,alg2), p_value)
#
#
# stats.probplot(results['GA'], dist="norm", plot=plt)
# plt.title("Blood Pressure After Q-Q Plot")
print(stats.wilcoxon(results.PSO, results.GA, alternative="less"))
plt.show()