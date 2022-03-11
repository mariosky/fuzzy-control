import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
from itertools import groupby
from operator import itemgetter
import matplotlib.ticker as mticker

results = pd.read_csv('results.csv')
fig, ax = plt.subplots()

ax.boxplot(results,
       vert=True,  # vertical box alignment
       patch_artist=True,
       showfliers=False,
       labels=["GA", "PSO", "AO", "GWO", "AOA", "HS"])  # will be used to label x-ticks


# add a 'best fit' line
ax.set_ylabel('RMSE')
ax.yaxis.grid(True)

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()