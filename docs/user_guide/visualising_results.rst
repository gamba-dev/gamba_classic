Visualising Results
=======================

Data visualisation techniques can be used as a powerful exploratory aid, and to present your findings in a clear and accessible way.
Because gamba can be used to analyse players at different levels of granularity, e.g. from an individual player's career up to groups of players, the library contains a few plotting functions which each accept different types of data.
To get started, you can import gamba as follows, we'll also create some dummy data to use in the examples;
We can start by looking at the distributions of each of the measures in the population using `plot_measure_pair_plot()` as follows;

.. plot::

	import gamba as gb
	measures_table = gb.data.dummy_measures_table()
	gb.plot_measure_pair_plot(measures_table)
