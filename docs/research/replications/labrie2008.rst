LaBrie et al's 2008 Study
======================================

This study explored internet casino gambling using data from the operator Bwin.
This data included 4222 gamblers to calculate a collection of behavioural measures and then calculate descriptive statistics on those measures.
The code needed to replicate this analysis using the gamba library follows this logical order.

First, we used the :any:`gamba.data` module to parse the data into a format that other methods in the library can use.

.. code-block:: Python

	import gamba as gb
	gb.prepare_labrie_data('RawDataSet2_DailyAggregCasinoTXT.txt')
	all_player_bets = gb.load_directory("labrie_individuals/")

From there, the behavioural measures described in the original paper can be calculated using implementations of them in the :any:`gamba.measures` module. These measures are automatically saved as a CSV file so that if anything goes wrong we don't have to do this computation again;

.. code-block:: Python

	gb.calculate_labrie_measures(all_player_bets, loud=True)
	labrie_measures = gb.read_csv('gamba_labrie_measures.csv')

With the *measures table* ready to use, the rest of the replication simply applies different analytical methods from the :any:`gamba.tests` module to this table.

.. code-block:: Python
	
	labrie_table = gb.descriptive_table(labrie_measures)
	spearman_coefficient_table = gb.calculate_labrie_coefficients(labrie_measures)
	top5, other95 = gb.split_labrie_measures(labrie_measures)
	top5_table = gb.descriptive_table(top5)
	other95_table = gb.descriptive_table(other95)

These each describe different tables in the original paper, and are now ready to be displayed or saved. For this replication we used Jupyter Lab, so to display all of the tables above takes just one line of code;

.. code-block:: Python
	
	display(labrie_table, spearman_coefficient_table, top5_table, other95_table)

And that's it! This is one of the simplest replications of those performed so far using the gamba library, and is a great reference point for doing more studies on new data, or delving deeper into some of the methods to see how they could be built upon to make something new!

As with all areas of the library, if you encounter any issues or bugs and can't find answers on the `issues page <https://github.com/gamba-dev/gamba/issues>`_, please reach out over `Twitter <https://www.twitter.com/gamba_dev>`_ or via `Email <mailto:oliver@gamba.dev>`_!

