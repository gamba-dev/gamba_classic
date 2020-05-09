"""
Behavioural Measures Centile Plot
===================================

The gamba.plot_measure_centile accepts a top_heavy parameter, which if set to True groups the bars into five-percentile chunks.
From the 95th percentile its scheme changes, with each further bar representing only one percent of the population.
See the image below for an example, and note that the x axis here is not continuous towards the end!


"""

import gamba as gb
import numpy as np # for generating some data
import pandas as pd

# create a measures table to use for the example
measures_table = pd.DataFrame()
measures_table['duration'] = np.random.exponential(scale=1,size=(1000,5)).sum(axis=1)

top_heavy_centile = gb.plot_measure_centile(measures_table, 'duration', top_heavy=True)
top_heavy_centile.show()

#%%
# 
# Without the top_heavy parameter, each centile will be plotted on a continuous x-axis.
# This can be useful early on in your analysis to get a feel for the distribution of a measure without doing any of the more complicated plots!


centile = gb.plot_measure_centile(measures_table, 'duration')
centile.show()