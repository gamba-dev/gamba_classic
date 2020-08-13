Philander's 2014 Study
====================================

This study applies a collection of supervised machine learning techniques to analytical data created during Braverman and Shaffer's 2010 study on high-risk gamblers.
These include logistic regressions, neural networks, support vector machines, and random forests.
The learning module in the gamba library contains methods for performing these techniques, where each accept a measures table as a parameter, like other analytical methods in the library.
To get started, import gamba as follows;

.. code-block:: Python

	import gamba as gb

With gamba ready to go, the next step is to get the dataset used in the paper into a usable form. To do this, gamba's data module contains a 'prepare_philander_data' method, which loads the original analytic data and renames the columns to be compatable with other methods in the library.

.. code-block:: Python
	
	data = gb.prepare_philander_data('AnalyticDataSet_HighRisk.txt', loud=True)

The data is now ready, and is already in the form of a measures table. As we are using some machine learning methods for this replication, the next step is to create training and testing subsets for the following algorithms to use. Gamba's split_measures_table method does just that, and to create a split as found in the original paper, a fraction of 0.696 (0.7 doesn't quite do it), works great.

.. code-block:: Python
	
	train_measures, test_measures = gb.split_measures_table(data, frac=.696, loud=True)




``---page under construction--``
