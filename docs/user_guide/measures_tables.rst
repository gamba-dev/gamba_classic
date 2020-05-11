Creating a Measures Table
============================


Having loaded a set of transaction data into a format compatable with the rest of the library, the next step is to compute a measures table.

.. note:: **What is a measures table?**

	A measures table is a `Pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_ containing a player_id column and a collection of behavioural measures computed using those player's transactions. It can optionally contain labelling columns, see :doc:`stats_and_labelling`.

	.. figure:: ../images/measures_table.*


The first step in creating a measures table is to import the Pandas library, and create an empty DataFrame which we can add data to.
This is the only explicit exposure to the Pandas library in this documentation so don't worry if you aren't super familiar with the syntax!

.. ipython:: python

	import pandas as pd

	measures_table = pd.DataFrame()


With an empty measures table ready to receive some data, the next step is to load in the player transactions if they aren't loaded in already.


.. ipython:: python
	
	import gamba as gb

	data = gb.read_csv('your_file_name_here.csv', dummy_data=True)
	data.columns = ['player_id','bet_time','bet_size','payout_size']
	display(data)


We now have all player's bets in one place. Next, for each unique player in that data, we can get their ID to begin populating the measures table.

.. note:: 

	The next few steps can be done in a single loop over the data, but are seperated here to cover each step in more detail.

.. ipython:: python

	unique_player_ids = list(set(data['player_id'].values))

We can now add the unique player id's to the measures table, and display it to see what it looks like.

.. ipython:: python

	measures_table['player_id'] = unique_player_ids

	display(measures_table)

Now that the player_id column of the measures table is ready, for each of the unique players we've found we need to get their bet data and calculate a measure from it.
For this example we'll use the total_wagered measure, and the net_loss measure.

.. ipython:: python

	wager_totals = []
	loss_totals = []
	for player_id in unique_player_ids:
		player_bets = data[data['player_id'] == player_id]
		wager_totals.append(gb.total_wagered(player_bets))
		loss_totals.append(gb.net_loss(player_bets))

We now have two lists corresponding to the total amounts wagered for each player, and the net losses for each player.
To add these to the measures table, we use the same technique as we did for the player id's;

.. ipython:: python

	measures_table['total_wagered'] = wager_totals
	measures_table['net_loss'] = loss_totals
	display(measures_table)

We now have a very simple measures table with two measures per player.
Creating larger and more complicated measures tables is a case of adding more measures in the same way we did here.
If you're interested in creating and testing new measures, just replace a measures method with your own and give it a name.
The column names of the measures table must start with 'player_id' so that the library knows whose measures are who's, but the measures columns themselves can be named in any way - the analytical methods will handle it!


.. raw:: html

	<h2>Pre-coded Measures Tables</h2>

The academic articles whose figures can be reproduced using gamba each make use of a methods table with a specific collection of measures.
An example is LaBrie et al's 2008 study on casino gamblers, which calculated eight behavioural measures for each of the players in the sample.
To make replicating this work easier, and to make computing comparable measures tables in other domains easier, gamba contains a bespoke function for doing so.
This function works on the data format used in the original paper, after it has been parsed by the :any:`gamba.data`



.. note:: Developer Note

	It would be really nice to have a generic ``gb.create_measures_table()`` function which wraps all of this code into one and optimises the computations.
	It's currently under development but is not ready for this release.

