Loading Transaction Data
==========================

All analysis using the gamba library revolves around creating a measures table from a set of transaction data.
Before a measures table can be created, the transaction data we're interested in must be loaded in, parsed into a format that other functions in the library can use, and cleaned.

The first step is to import gamba so that all of its functions can be accessed;

.. ipython:: python

	import gamba as gb

Next, assuming you have a set of transaction data saved as a CSV file, it needs to be loaded and the columns renamed.
The data module has a help() function for printing out the names of the columns used by the rest of the functions in the library.

.. ipython:: python

	gb.data.help()

The help printed shows that the column in your data corresponding to the name or identifier of each player should be renamed to 'player_id'.
The column in your data corresponding to the date/time of when the bet was placed should be renamed to 'bet_time'.
Data describing the sizes of bets placed, also known as the stake or the amount wagered, shoud be renamed to 'bet_size'.
Finally, the data describing the amount won by the player should be renamed to 'payout_size'.

Before getting to renaming columns, we can load in an example CSV file to use as an example.
We can use the 'dummy_data' parameter in the read_csv() function to return some generated data just for this guide.
In your code, don't use this parameter and instead just write the name and directory of your CSV file as the first parameter, e.g. 'Oliver/Data/TX_Data.csv'.


.. ipython:: python

	data = gb.read_csv('your_file_name_here.csv', dummy_data=True)
	display(data)

By displaying the data we can see that the column names don't match the ones printed above, to rename them simply set the columns attribute of the data object equal to a list of new names (make sure it's the same length!).

.. ipython:: python

	data.columns = ['player_id','bet_time','bet_size','payout_size']
	display(data)

At this point the data is ready to be used by the other functions in the library, although it may need cleaning (removing empty values, etc.).
If you've successfully loaded in your own data then feel free to progress to the :doc:`measures_tables` page.

If you're looking to load in existing data or have more detailed data than the four columns above, continue down this page.

.. raw:: html

	<h2>Parsing Existing Data</h2>

.. note::
	
	Please be sure to follow all legal and ethical guidelines when using gamba to analyse existing transaction data, and get local institutional review board approval as required!

gamba's data module contains several methods for parsing existing open access data sets into the usable format described above.
These can be called as follows;

.. code-block:: python

	gb.prepare_labrie_data('dataset_name.csv', year=2007)

	gb.prepare_braverman_data('dataset_name.csv')

This list will be expanded as more studies are replicated using the library.
It's important to remember the level of granularity (e.g. daily aggregate or individual transactions) of the data set when it comes to analysing it later on.
For examples on how these are used in replications of several studies, see the :doc:`../research/replications/index` page.



.. raw:: html

	<h2>Detailed Data</h2>

If you have access to more detailed data - that is, more columns which describe different information about any given bet - then you can load it in and use it with some of the more advanced functions in the library.

An example would be data describing the time a payout was made, as in some games there is a substantial delay between betting and payouts.
Another is the odds of a given bet being successful.
This type of information is useful for computing the potential payouts of a given bet, and different measures of risk the player is exposing themselves to.

The gamba.data module's help function can be given an optional 'advanced' parameter, which will print out the column names corresponding to more detailed data;


.. ipython:: python

	gb.data.help(advanced=True)

If you are using more detailed data, rename your columns to those printed above accordingly, and continue on to the :doc:`measures_tables` page!


