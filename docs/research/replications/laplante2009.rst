LaPlante et al's 2009 Study
=========================================


This study used many of the same techniques in :doc:`labrie2008` to exlore the spending of 3445 internet poker players.
As with other replications, it follows the data parsing -> measures calculations -> testing format as follows, starting with data loading/parsing;

.. code-block:: Python

	import gamba as gb

	raw_data = gb.read_csv('DS4_Raw2_Aggregate_txt.txt', delimiter='\t')
	analytic_data = gb.read_csv('DS4_Analytic_txt.txt', delimiter='\t')
	print('raw data loaded:', len(raw_data))
	print('analytic data loaded:', len(analytic_data))

Next, taking only the analytic data forward (for now), we can prepare the three subsets described in the paper (full set, most involved, not most involved);

.. code-block:: Python

	useful_columns = ['UserID','Duration','Total_sessions','Sessions_Per_Day','Euros_Per_Session','Total_wagered','Net_Loss','Percent_Lost']
	all_study_data = analytic_data[useful_columns] # get only columns that are used in the analysis, then rename them to be compatable with gamba
	all_study_data.columns = ['player_id','duration','total_sessions','sessions_per_day','euros_per_session','total_wagered','net_loss','percent_loss']

	# now do the same for the 5-95 split of players performed in the study (using the 'Most_Involved_Group' column)
	most_involved = analytic_data[analytic_data['Most_Involved_Group'] == 1]
	most_involved = most_involved[useful_columns]
	most_involved.columns = ['player_id','duration','total_sessions','sessions_per_day','euros_per_session','total_wagered','net_loss','percent_loss']

	not_most_involved = analytic_data[analytic_data['Most_Involved_Group'] == 0]
	not_most_involved = not_most_involved[useful_columns]
	not_most_involved.columns = ['player_id','duration','total_sessions','sessions_per_day','euros_per_session','total_wagered','net_loss','percent_loss']

	print('all players:', len(all_study_data))
	print('most involved:', len(most_involved))
	print('others 95 percent:', len(not_most_involved))

These numbers are identical to those found in the paper, so at this stage we can be reasonably sure that the data extracted above is the same as that used in the original analysis. We can then reproduce each of the tables with the `descriptive_table` function, plus the `cohens_d` and `ks_test` functions...

.. code-block:: Python

	descriptive_df = gb.descriptive_table(all_study_data)
	ks_table = gb.ks_test(all_study_data)
	combined = gb.concat([descriptive_df, ks_table], axis=1)
	display(combined)

	majority_table = gb.descriptive_table(not_most_involved)
	minority_table = gb.descriptive_table(most_involved)
	display(majority_table, minority_table)

	most_involved['most_involved'] = 1
	not_most_involved['most_involved'] = 0
	all_labelled_data = gb.concat([most_involved, not_most_involved])
	cohens = gb.cohens_d(all_labelled_data, 'most_involved')
	most_involved.drop(['most_involved'], axis=1, inplace=True)
	display(cohens)

	spearmans = gb.spearmans_r(all_study_data)
	second_spearmans = gb.spearmans_r(most_involved)
	display(spearmans)
	display(second_spearmans)


That's it! The tables found in the paper can be recreated from those above - minus a *df*, *t*, *p*, and *p(2-tailed)* column which are not described in the text.

This replication contains some problems, most notably that the paper contains undocumented results, plus a data transformation appears to be discussed but not explicitly described (causing differences in statistical tests).
This does not invalidate any replication attempt overall, but does provide an example of where ambiguity can be introduced in the analysis if the paper does not carefully describe each step of the process!
See the :download:`jupyter notebook <LaPlante_2009/laplante_2009.ipynb>` for this project to see how the outputs differ!
