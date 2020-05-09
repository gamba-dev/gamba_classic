"""
Behavioural Measures Histogram
================================

We can get an idea for the distribution of a given behavioural measure by creating a histogram.
This simple visualisation also adds labels for the mean and median values of the measure provided.
"""

import gamba as gb
import numpy as np # for generating some data
import pandas as pd

# create a measures table to use for the example
measures_table = pd.DataFrame()
measures_table['duration'] = np.random.exponential(scale=1,size=(1000,5)).sum(axis=1)

histogram = gb.plot_measure_hist(measures_table, 'duration')

histogram.show()