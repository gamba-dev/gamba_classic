

API Reference
================

This section describes each of the modules and functions in more detail than the user guide, but is not geared towards first-time use.
Quick links to each of the individual module pages is directly below, followed by longer summaries of each of the modules and links to all of the methods they contain.

.. toctree::
	:maxdepth: 3

	data
	measures
	labels
	tests
	machine_learning
	plots
	studies 



.. raw:: html

	<h2>Data</h2>

The :any:`gamba.data` module contains a set of functions designed to address parts of the data cleaning process.
The goal here is to take existing data and transform it so that it can be accepted by other methods in the library.
Some methods are wrappers for those found in other libraries provided for convenience, and others are specific to data sources described in the :doc:`../research/replications/index`.

.. automodsumm:: gamba.data
	:functions-only:


.. raw:: html

	<h2>Behavioural Measures</h2>

The :any:`gamba.measures` module contains code for computing behavioural measures based on player transaction data. 
These include those used in existing academic work such as betting frequency, duration, net loss, total amount wagered, etc. 
All methods in this module accept player_bets as their sole parameter. 
This is a dataframe containing all bets made by a player, and should contain columns corresponding to the type of data needed to calculate each of the behaivoural measures - for example, the :meth:`total_wagered` cannot be calculated without a `bet_size` column being present in the player_bets.

Each function in this module checks the data provided meets the minimum requirements (has the correct columns) before continuing, raising an exception if these checks fail. 
This check is implemented as :meth:`check_measure_data`.

.. automodsumm:: gamba.measures
	:functions-only:


.. raw:: html

	<h2>Labelling</h2>

The :any:`gamba.labels` module contains methods for labelling behavioural measures according to some labelling heuristic. 
Examples include those in the top 5% of players by some measure versus the remaining 95%.
These methods append a columnn to the measures table provided, indicating presence in a group with a 1 or 0.
The :meth:`get_labelled_groups` method is provided as a convenient way to split the table by a given measure.

.. automodsumm:: gamba.labels
	:functions-only:


.. raw:: html

	<h2>Machine Learning</h2>

The :any:`gamba.machine_learning` module contains methods for clustering behavioural measures using the k-means clustering and agglomerate clustering algorithms (see the `sklearn library <https://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster>`_ for details).
These are useful when detecting high-dimensional groups within a collection of behavioural measures, but can get complicated quite quickly.

It also contains methods for creating and training computational models like neural networks (using the `keras library <https://keras.io>`_), which have been used in several recent studies to predict player behaviours.

.. automodsumm:: gamba.machine_learning
	:functions-only:


.. raw:: html

	<h2>Testing</h2>

Performing statistical tests on collections of behavioural measures is important in presenting differences between groups, and descriptions of the groups themselves.
The :any:'gamba.tests' module contains functions capable of performing tests found in several academic studies on a table of behavioural measures.


.. automodsumm:: gamba.tests
	:functions-only:


.. raw:: html

	<h2>Plotting</h2>

The :any:`gamba.plots` module provides a collection of methods for visualising data throughout the analytical pipeline.
These methods are useful for developing an understanding of the data at the exploratory stages of analysis, or for confirming findings which appear as a result of statistical tests or clustering.
The :doc:`../gallery/index` page contains a showcase of each of these methods on synthetic data - the code provided may be a useful skeleton upon which to build your study!

.. automodsumm:: gamba.plots
	:functions-only:


.. raw:: html

	<h2>Studies</h2>

Finally, the :any:`gamba.studies` module contains some higher level methods specific to some of the studies this library can be used to replicate.
These methods are extremely specific so may not find as much use as those above, but are included here for reference.

.. automodsumm:: gamba.studies
	:functions-only: