Statistics and Labelling
===============================


.. raw:: html

	<h2>Descriptive Statistics</h2>

Once a measures table has been created, a good place to start is to describe how the each of the measures vary across the population.
One way to do this is by computing descriptive statistics across the measures table.
To do this using gamba, first import the library so that we can access the necessary functions;

.. ipython:: python

	import gamba as gb

Next, we'll load in a dummy measures table to use as an example.
If you're following along with the user guide for your own analysis, replace this with your own measures table calculated in the previous section.


.. ipython:: python

	measures_table = gb.data.dummy_measures_table()
	display(measures_table.head(5))

With a measures table ready, here are just a few ways that the :any:`gamba.tests` module can help;

.. ipython:: python

	gb.descriptive_table(measures_table, extended=True)

You can also explore the relationships between the measures by computing Spearman's R between each of the pairs.

.. ipython:: python

	gb.spearmans_r(measures_table)

Past this point you may want to develop your own functions which compute something across each of the measures.
You may also want to label sub-cohorts of players within your data set, and explore how groups in the labels differ.
Before moving on to labelling you may want to explore some of the :doc:`../research/replications/index` for a better idea of how these functions can be used as part of a larger study.

.. raw:: html

	<h2>Labelling Players</h2>

After developing an understanding of a data set in its entirety, many studies go on to explore how sub-groups within their sample vary in different ways.
In practical terms, this means applying a label to each player in the measures table.
How this label is applied, and how many different labels there are, depends on the motivation behind the study.

One example of a labelling heuristic (way of assigning labels to players) is to split them into groups according to their presence in the upper portion of values of some metric.
An example of this would be labelling players in the top 5% of players by the total amount they have wagered.
To do this using gamba, the following function exists;


.. ipython:: python

	labelled_measures_table = gb.top_split(measures_table, 'total_wagered')
	display(labelled_measures_table.head(5))

We can see that a new column has been added which is either 0 or 1 indicating a players presence in the top 5% by total amount wagered.
This 'labelled' measures table invites some more tests such as a Cohen's d between the groups;

.. ipython:: python

	gb.cohens_d(labelled_measures_table, 'top_total_wagered')


Applying a fixed labelling heuristic and exploring groups is a good way to get to know the data sample, and uncover some interesting properties about differences between groups of players.
Recent research has highlighted the potential uses of clustering algorithms, which can be described as a way to apply labels without using a fixed heuristic.
To explore how gamba's functions use the `scikit-learn library's clustering functions <https://scikit-learn.org/stable/modules/clustering.html>`_, continue on to the :doc:`clustering_measures` page!
