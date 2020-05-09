LaBrie et al's 2007 Study
======================================

This page will guide you through replicating `LaBrie et al's 2007 study on internet sports gambling behaviour <https://www.researchgate.net/profile/Howard_Shaffer/publication/6261653_Assessing_the_Playing_Field_A_Prospective_Longitudinal_Study_of_Internet_Sports_Gambling_Behavior/links/0fcfd50a6bc690d200000000/Assessing-the-Playing-Field-A-Prospective-Longitudinal-Study-of-Internet-Sports-Gambling-Behavior.pdf>`_, using data from `the transparency project <http://www.thetransparencyproject.org/download_index.php>`_. 

Note: the data we need is *Raw Dataset 2 (text version)* under the title 'Actual Internet Sports Gambling Activity: February 2005 through September 2005' towards the bottom of the page. We will also need the analytic data set named *AnalyticDataInternetGambling*, which is the text version of the analytic data set in the same section of that page.

The first step is to import the gamba library, granting access to all the methods we need;

.. code-block:: Python

	import gamba as gb

Next, read in the CSV file downloaded from the link above, and prepare the data using gamba's parsing method so it's in the right format for the rest of the library's methods.This splitting to the individual level will prove useful when exploring the data later on, as individual's transactions can be loaded as required without re-searching the data;

.. code-block:: Python

	daily_data = gb.read_csv('RawDataIIUserDailyAggregation.txt')
	daily_data[daily_data['ProductID'] == 1].to_csv('fixed_odds_daily.csv', index=False)
	daily_data[daily_data['ProductID'] == 2].to_csv('live_action_daily.csv', index=False)

	gb.prepare_labrie_data('fixed_odds_daily.csv', savedir='fo_labrie_individuals/', year=2007)
	gb.prepare_labrie_data('live_action_daily.csv', savedir='la_labrie_individuals/', year=2007)


With individual's transactions each saved to CSV files in their own directories (and now in the right format), we can now load them back in and calculate the behavioural measures described in the paper...

.. code-block:: Python

	gb.calculate_labrie_measures("fo_labrie_individuals/", filename='fo_labrie_measures.csv', loud=True)
	gb.calculate_labrie_measures("la_labrie_individuals/", filename='la_labrie_measures.csv', loud=True)

Next, for this replication we can take the user id's from the original analytic data set and take those from the measures dataset calculated above;

.. code-block:: Python
	
	fo_gamba_measures = gb.read_csv('fo_labrie_measures.csv')
	la_gamba_measures = gb.read_csv('la_labrie_measures.csv')
	original = gb.read_csv('AnalyticDataInternetGambling.txt')

	fo_bettors = original[original['FOTotalBets'] > 0]
	la_bettors = original[original['LATotalBets'] > 0]

	gamba_fo = fo_gamba_measures[fo_gamba_measures['player'].isin(fo_bettors['USERID'].values)]
	gamba_la = la_gamba_measures[la_gamba_measures['player'].isin(la_bettors['USERID'].values)]

We can describe these measures using the descriptive_table method from the :any:`gamba.tests` module as follows, plus compute spearmans r's between each of the behavioural measures in both the fixed odds and live action bettors;

.. code-block:: Python

	t1a = gb.descriptive_table(gamba_fo)
	t1b = gb.descriptive_table(gamba_la)
	display(t1a.round())
	display(t1b.round())
	    
	fo_spearmans = gb.spearmans_r(gamba_fo)
	la_spearmans = gb.spearmans_r(gamba_la)
	display(fo_spearmans)
	display(la_spearmans)

With both the descriptive and inter-measure correlation tables complete, the sample of measures can be labelled according to the presence of a player in the top 1% of their cohort by a given measure. In this case the measures include the **net loss**, **total amount wagered**, and **number of bets**. This is done for both the fixed odds (fo) and live action (la) data...

.. code-block:: Python
	
	fo_labelled = gb.top_split(gamba_fo, 'net_loss', percentile=99)
	fo_labelled = gb.top_split(fo_labelled, 'total_wagered', percentile=99)
	fo_labelled = gb.top_split(fo_labelled, 'num_bets', percentile=99)

	t3a = gb.descriptive_table(fo_labelled[fo_labelled['top_net_loss'] == 1])
	t3b = gb.descriptive_table(fo_labelled[fo_labelled['top_total_wagered'] == 1])
	t3c = gb.descriptive_table(fo_labelled[fo_labelled['top_num_bets'] == 1])

	la_labelled = gb.top_split(gamba_la, 'net_loss', percentile=99)
	la_labelled = gb.top_split(la_labelled, 'total_wagered', percentile=99)
	la_labelled = gb.top_split(la_labelled, 'num_bets', percentile=99)

	t3d = gb.descriptive_table(la_labelled[la_labelled['top_net_loss'] == 1])
	t3e = gb.descriptive_table(la_labelled[la_labelled['top_total_wagered'] == 1])
	t3f = gb.descriptive_table(la_labelled[la_labelled['top_num_bets'] == 1])

	t3_top = gb.concat([t3a, t3b, t3c], axis=1).reindex(t3a.index)
	t3_bottom = gb.concat([t3d, t3e, t3f], axis=1).reindex(t3d.index)
	t3_top.drop(t3_top.tail(3).index,inplace=True)
	t3_bottom.drop(t3_bottom.tail(3).index,inplace=True)

	display(t3_top)
	display(t3_bottom)

Finally, we need to present the overlap in terms of membership between the three different top 1%'s described above.
To calculate this, we can used the label_overlap_table function;

.. code-block:: Python

	fo_table = gb.label_overlap_table(fo_labelled, ['top_net_loss','top_total_wagered','top_num_bets'])
	la_table = gb.label_overlap_table(la_labelled, ['top_net_loss','top_total_wagered','top_num_bets'])
	display(fo_table)
	display(la_table)


That's it! Performing this replication is a little longer than the earlier papers, but it all follows a logical order nonetheless.
An important final note is that some of the figures (see fixed odds bettors frequency measures) differ slightly from those in the original paper, even though the players were taken from the analytic data set above.
This is currently an open issue believed to be caused by a minor (1) difference in the number of players in the data sets.
We can still be sure that the implementations of the methods are accurate as the live action bettors figures are replicated exactly.
