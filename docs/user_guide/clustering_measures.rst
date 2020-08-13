Understanding Clusters
=======================

After creating a measures table, it can be useful to explore how players form clusters according to different measures.
This page uses the very basic k-means clustering algorithm as an example, although more are in development.
To begin, we load in a measures table as done in the two previous sections;

.. ipython:: python

	import gamba as gb

	measures_table = gb.data.dummy_measures_table()

	display(measures_table.head(5))

Next, we can perform the clustering algorithm once using functions from the :any:`gamba.machine_learning` module which wraps around the `scikit-learn library's clustering functions <https://scikit-learn.org/stable/modules/clustering.html>`_.


.. ipython:: python

	clustered_measures_table, inertias, silhouettes = gb.k_means(measures_table)

	display(clustered_measures_table.head(5))

You will have noticed two extra things returned by the k_means function which can be used to understand how well the final clusters fit the data.
These are more meaningful when comparing several clustering attempts with different parameters.
This can be done in gamba using clustering algorithms with '_range' in their name, e.g. k_means_range();

.. ipython:: python

	inertias, silhouettes = gb.k_means_range(measures_table)

	print(inertias)
	print(silhouettes)

It's not all that meaningful just looking at the numbers, so basic plots of the inertias and silhouettes can help here (we're plotting between 2 and 13 so that the x axis represents the number of k-means clusters);

.. ipython:: python

	import matplotlib.pyplot as plt

	@savefig inertias_plot.png width=4in
	plt.plot(range(2,14), inertias, color='blue');

.. ipython:: python

	@savefig silhouettes_plot.png width=4in
	plt.plot(range(2,14), silhouettes, color='orange');

As this clustering has been done on a random set of dummy data we don't see anything that interesting, but our exploration of clusters is not over yet.
Performing clustering once is useful but not always robust (depending on the clustering algorithm used).
To account for this, we can perform the clustering a number of times and take an average of the scores.
To do this using the gamba library, we can use functions with the ``_ensemble`` suffix, which perform the ``_range`` functions a number of times and average the resulting fitness scores;

.. ipython:: python

	mean_inertias, mean_silhouettes = gb.k_means_ensemble(measures_table, ensemble_size=10)

.. note::
	
	The ensemble_size parameter above defaults to 100, it's set to 10 here just for the example.

This should give us a better idea of the 'best' number of clusters to use (in the case of k-means), and can be plotted in the same way as those above.

.. ipython:: python

	@savefig mean_inertias_plot.png width=4in
	plt.plot(range(2,14), mean_inertias, color='blue');
	
.. ipython:: python

	@savefig mean_sihouettes_plot.png width=4in
	plt.plot(range(2,14), mean_silhouettes, color='orange');
	

This method of computing across a range and ensembling that range only works for some clustering algorithms.
For a more detailed look at different algorithms please visit the `scikit-learn library's clustering functions page <https://scikit-learn.org/stable/modules/clustering.html>`_, or `this page for an example <../research/replications/braverman2010.html>`_ of how they have been used as part of a replication.

Now that we've covered loading in data, computing a measures table, and describing, labelling, and clusting that table, the only thing left is to explore the visualisations gamba's plots module provides.
Continue on to :doc:`visualising_results` to find out more!
