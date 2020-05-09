"""
Pair Plot Between Behavioural Measures
=======================================

We can visualize the relationships between different behavioural measures using a pair plot.
This should help you gain insight into both the distributions of each measure, and how players typically score across each measure.
To create this plot using the :any:`gamba.plots` module, use the following code;


"""

import gamba as gb
import numpy as np # for generating some data
import pandas as pd

# create a measures table to use for the example
# using mixed distributions to see the full effects
num_players = 500
measures_table = pd.DataFrame()
measures_table['player_id'] = ['anonymous'] * num_players
measures_table['duration'] = np.random.standard_exponential(size=num_players)
measures_table['frequency'] = np.random.normal(loc=50, scale=1,size=num_players)
measures_table['num_bets'] = np.random.standard_exponential(size=num_players)
measures_table['bet_size'] = np.random.uniform(low=1, high=500,size=num_players)

scatter_variant = gb.plot_measure_pair_plot(measures_table)
scatter_variant.show()

#%%
# 
# Pair plots are really useful for exploring relationships between different behavioural measures, but using scatter plots makes it difficult to see the density of different areas.
# To address this problem, the pair_plot method comes with a 'thermal' parameter, which if True will intead use a 2D histogram with a thermal blur in place of the scatter plots above.
# This is much more useful (and colourful), but maybe a bit garish for academic publication - feel free to experiment with different colours and blurs by using the function in your own work!
# 

thermal_variant = gb.plot_measure_pair_plot(measures_table, thermal=True)
thermal_variant.show()