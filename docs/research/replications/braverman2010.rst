Braverman and Shaffer's 2010 Study
================================================

This study applies the k-means clustering algorithm to a collection of behavioural measures across a cohort of 530 players.
As the k-means algorithm is randomly initialised, it is unlikely to exactly replicate this study's findings, however the gamba library contains all of the methods needed to follow in their footsteps!

The first step is to import the gamba library, granting access to all the methods we need;

.. code-block:: Python

	import gamba as gb

Next, load in both the raw and analytic data available through the transparency project (link in sidebar);

.. code-block:: Python

    raw_data = gb.read_csv('RawDataSet2_DailyAggregation.txt', delimiter='\t', parse_dates=['TimeDATE'])
    analytic_data = gb.read_csv('AnalyticDataSet_HighRisk.txt', delimiter='\t')
    
The next step is to calculate the measures described in the paper for each of the players in the cohort, gamba has a bespoke method for the measures described in this paper;

.. code-block:: Python

    measure_table = gb.calculate_braverman_measures(all_player_bets)
    
With the measures table created, the paper describes a standardisation procedure before clustering, which computes zscores for each of the measures.
We can do this using the `standardise_measures_table()` function from the measures module.

.. code-block:: Python

    standardised_measures_table = gb.standardise_measures_table(measures_table)

The final step is to apply the k-means clustering algorithm, for which gamba provides a wrapper function around the sklearn library's implementation;

.. code-block:: Python

    clustered_data = gb.k_means(standardised_measures_table, clusters=4, data_only=True)

    gb.describe_clusters(clustered_data)
    
This will output descriptions of the centroids identified by the clustering attempt, along with the number of members for each cluster.

Although the paper contains several other techniques alongside the clustering above, this replication in particular has several caveats regarding the computation of the measures, and the reliability of the clusering (given its randomised nature). For more information feel free to :download:`download the codebook <Braverman_2010/braverman_2010.ipynb>` associated with this replication, or get in touch for questions!