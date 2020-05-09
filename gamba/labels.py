# data labelling module

# this module provides methods for labelling existing dataframes of
# behavioural measures

import numpy as np


def top_split(measures_table, split_by, percentile=95, loud=False):
	"""
	Labels player's behavioural measures according to their presence in the top percentile of a given measure (split_by).
	Label column will be 1 if in the top percentile, 0 if not.
	E.g. if split_by is 'total_wagered' and percentile is 95, players in the top 5% by total wagered will be labelled 1, and all others 0.


	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
		split_by (String): The measure to split players by, e.g. 'total_wagered'.
		percentile (Integer): The percentile at which to split players, default is 95 meaning a 5-95 split.
		loud (Boolean): Wherer or not to print out some information about the labelling.
	
	Returns:
		A copy of the measures table provided, with an added column containing the 'top' split labels.
	
	"""

	cutoff = np.percentile(measures_table[split_by].values, percentile)

	column_name = 'top_' + split_by

	labelled_measures_table = measures_table.copy()

	labelled_measures_table[column_name] = 0
	labelled_measures_table.loc[labelled_measures_table[split_by] > cutoff,
						  column_name] = 1

	if loud:
		print('top count:', len(labelled_measures_table[labelled_measures_table['top_'+split_by] == 1]))
		print('other count:', len(labelled_measures_table[labelled_measures_table['top_'+split_by] == 0]))

	return labelled_measures_table


def get_labelled_groups(labelled_measures_table, labelname):
	"""
	Provides a simple way of splitting a labelled measures table into multiple tables each corresponding to a given label.

	Args:
		labelled_measures_table (Dataframe): A measures table with a column corresponding to a label.
		labelname (String): The name of the label to be split on.

	Returns:
		List of dataframes correspending to membership of a given label.

	"""
	
	# get the labels IN ASCENDING ORDER (important)
	labels = sorted(set(list(labelled_measures_table[labelname].values)))
	player_groups = []
	for label in labels:
		this_group = labelled_measures_table[labelled_measures_table[labelname] == label]
		player_groups.append(this_group)

	
	return player_groups


def spending_portions(measures_table):
	"""
	Computes the percentages of total amount wagered of groups of players by presence in the top percentages of the total amount wagered.
	E.g. how much does the top 5% of players by total amount wagered account for out of the total amount wagered by everyone.
	It currently computes this statement for the percentages {1,5,10,25,50}, and prints the statements to the console.

	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.


	"""

	percentages = [1,5, 10, 25, 50]

	for percentage in percentages:

		labelled_measures_table = gb.top_split(mt, 'total_wagered', percentile=100-percentage)
		groups = gb.get_labelled_groups(labelled_measures_table, 'top_total_wagered')
		label_members = groups[1]
		non_members = groups[0]

		total_amount = labelled_measures_table['total_wagered'].sum()

		top_one_amount = label_members['total_wagered'].sum()

		print('top',percentage,'% of players account for', str(round(top_one_amount,0)), '/', str(round(total_amount,0)), 
			'or', str(round(top_one_amount/total_amount * 100, 2)), 'of the amount wagered.')
