# behavioural measures module

# dependencies
import datetime, pandas as pd, numpy as np
from sklearn.linear_model import LinearRegression
from scipy.stats import zscore
# data checking


def check_measure_data(player_bets, required_columns):
	"""
	Compares the columns found in a dataframe of player bets to a supplied list of column names.
	If any of the required_column names are not found, an exception is raised reporting the error.

	:param required_columns: The names of columns needed for further calculations.
	:type required_columns: List of strings
	"""
	for column in required_columns:
		if column not in player_bets.columns:
			exception_string = 'Column \'' + column + '\' missing from provided dataframe.'
			raise Exception(exception_string)


def standardise_measures_table(measures_table):
	"""
	Standardises all measures columns in a measures table by applying the scipy.stats.zscore function to each column.
	This is useful for column-wise comparisons and some clustering methods.

	Args:
		measures_table(Dataframe): An unlabelled and unclustered measures table.

	Returns:
		A standardised measures table.
	"""
	colnames = list(measures_table.columns)[1:]

	standardised_table = pd.DataFrame()
	standardised_table['player_id'] = measures_table['player_id'].values
	for col in colnames:
		standardised_table[col] = zscore(measures_table[col].values)

	return standardised_table

# transaction level measures

def duration(player_bets):
	"""
	The number of days between the first bet and the last.
	"""
	check_measure_data(player_bets, ['bet_time'])
	player_bets.sort_values('bet_time', inplace=True)
	player_bets.reset_index(drop=True, inplace=True)

	first_day = player_bets.iloc[0]['bet_time']
	last_day = player_bets.iloc[len(player_bets) - 1]['bet_time']
	# add one to make it interpret as 'days where betting has occurred'
	age_in_days = (last_day.date() - first_day.date()).days + 1
	return age_in_days


def frequency(player_bets):
	"""
	The percentage of days within the :meth:`duration` that included at least one bet.
	"""
	check_measure_data(player_bets, ['bet_time'])
	player_bets.sort_values('bet_time', inplace=True)
	player_bets.reset_index(drop=True, inplace=True)
	age_in_days = duration(player_bets)

	player_bets['bet_date'] = player_bets['bet_time'].dt.date
	first_day = player_bets.iloc[0]['bet_time']

	betting_days = 0
	for day in range(age_in_days):
		current_date = (first_day + datetime.timedelta(days=day)).date()
		bets_today = player_bets.iloc[player_bets['bet_date'].values == current_date]
		if len(bets_today) != 0:
			betting_days += 1

	frequency_percentage = (betting_days / age_in_days) * 100
	return frequency_percentage


def number_of_bets(player_bets):
	"""
	The total number of bets made.
	"""

	return len(player_bets)


def average_bets_per_day(player_bets):
	"""
	The average (mean) number of bets made on days where betting took place.
	"""
	age_in_days = duration(player_bets)
	frequency_percentage = frequency(player_bets)

	betting_days = (frequency_percentage / 100)  * age_in_days

	average_bets_per_day = len(player_bets) / \
		betting_days  # taken from LaBrie 2008
	return average_bets_per_day


def average_bet_size(player_bets):
	"""
	The average (mean) size of bets.
	"""
	check_measure_data(player_bets, ['bet_size'])
	average_bet_size = player_bets['bet_size'].sum() / len(player_bets)
	return average_bet_size


def total_wagered(player_bets):
	"""
	The total amount wagered (sum of bet sizes).
	"""
	check_measure_data(player_bets, ['bet_size'])
	return player_bets['bet_size'].sum()


def net_loss(player_bets):
	"""
	The net amount lost (sum of bet sizes minus sum of payout sizes).
	"""
	check_measure_data(player_bets, ['bet_size', 'payout_size'])
	net_loss_value = player_bets['bet_size'].sum(
	) - player_bets['payout_size'].sum()
	return net_loss_value


def percent_loss(player_bets):
	"""
	The :meth:`net_loss` as a percentage of :meth:`total_wagered`.
	"""
	net_loss_value = net_loss(player_bets)
	total_wagered_value = total_wagered(player_bets)
	percent_loss_value = (net_loss_value / total_wagered_value) * 100
	return percent_loss_value


# daily aggregate measures

def number_of_bets_daily(player_bets):
	"""
	The total number of bets made if data set contains daily aggregate data.
	"""
	check_measure_data(player_bets, ['bet_count'])
	return player_bets['bet_count'].sum()


def average_bets_per_day_daily(player_bets):
	"""
	The average (mean) number of bets made on days where betting took place to be used on daily aggregate data.
	"""
	age_in_days = duration(player_bets)
	frequency_percentage = frequency(player_bets)

	betting_days = (frequency_percentage / 100) * age_in_days

	average_bets_per_day = number_of_bets_daily(
		player_bets) / betting_days  # taken from LaBrie 2008
	return average_bets_per_day


def average_bet_size_daily(player_bets):
	"""
	The average (mean) size of bets to be used on daily aggregate data.
	"""
	check_measure_data(player_bets, ['bet_size'])
	average_bet_size = player_bets['bet_size'].sum(
	) / number_of_bets_daily(player_bets)
	return average_bet_size


# braverman measures

def intensity_daily(player_bets):
	"""
	Mean number of bets per active betting day in first month, if data set contains daily aggregate data.
	"""
	first_day = player_bets.iloc[0]['bet_time']
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets['bet_time'] <= one_month_later]
	result = first_month_bets['bet_count'].mean()
	return result


def frequency_daily(player_bets):
	"""
	Number of active betting days in first month, if data set contains daily aggregate data.
	"""
	first_day = player_bets.iloc[0]['bet_time']
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets['bet_time'] <= one_month_later]

	return len(first_month_bets)


def variability_daily(player_bets):
	"""
	Standard deviation of stake size in first month, if data set contains daily aggregate data.
	"""
	first_day = player_bets.iloc[0]['bet_time']
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets['bet_time'] <= one_month_later]

	return first_month_bets['bet_size'].std()


def trajectory_daily(player_bets, plot=False):
	"""
	Gradient of a linear regression fitted to the sequence of daily aggredated bet sizes.
	"""

	first_day = player_bets.iloc[0]['bet_time']
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets['bet_time'] <= one_month_later]
	
	# first_month_bets['mean_bet_size'] = first_month_bets['bet_size'] / first_month_bets['bet_count']
	
	x = np.array(range(len(first_month_bets))).reshape((-1, 1)) + 1
	y = first_month_bets['bet_size'].values

	model = LinearRegression().fit(x, y)
	r_sq = model.score(x, y)

	model_x = x
	model_y = model.coef_ * x + model.intercept_

	if plot:
		plt.figure()
		plt.scatter(x, y)
		plt.plot(model_x, model_y, color='r')
		plt.show()

	trajectory = model.coef_[0]
	return model.coef_[0]

