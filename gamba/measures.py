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
			exception_string = (
				"Column '" + column + "' missing from provided dataframe."
			)
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
	standardised_table["player_id"] = measures_table["player_id"].values
	for col in colnames:
		standardised_table[col] = zscore(measures_table[col].values)

	return standardised_table


def split_measures_table(measures_table, frac=0.7, loud=False):
	"""
	Splits a measures table into two randomly selected groups. This is useful for machine learning methods where a train-test split is needed, and uses the Pandas library's sample method.

	
	Args:
		measures_table(Dataframe): A measures table.
		frac(Float): The fraction, represented as a decimal number, to split the measures table by, e.g. 0.7 would result in a 70-30 split.
		loud(Boolean): Whether or not to print out the size of the two resulting groups.

	"""
	measures_table.drop(['player_id'], axis=1)
	train_table = measures_table.sample(frac=frac) 
	test_table = measures_table.drop(train_table.index)

	if loud:
		print('train:test\n', len(train_table),':',len(test_table), 'ready')
	
	return train_table, test_table


# transaction level measures


def duration(player_bets):
	"""
	The number of days between the first bet and the last.
	"""
	check_measure_data(player_bets, ["bet_time"])
	player_bets.sort_values("bet_time", inplace=True)
	player_bets.reset_index(drop=True, inplace=True)

	first_day = player_bets.iloc[0]["bet_time"]
	last_day = player_bets.iloc[len(player_bets) - 1]["bet_time"]
	# add one to make it interpret as 'days where betting has occurred'
	age_in_days = (last_day.date() - first_day.date()).days + 1
	return age_in_days


def frequency(player_bets):
	"""
	The percentage of days within the :meth:`duration` that included at least one bet.
	"""
	check_measure_data(player_bets, ["bet_time"])
	player_bets.sort_values("bet_time", inplace=True)
	player_bets.reset_index(drop=True, inplace=True)
	age_in_days = duration(player_bets)

	player_bets["bet_date"] = player_bets["bet_time"].dt.date
	first_day = player_bets.iloc[0]["bet_time"]

	betting_days = 0
	for day in range(age_in_days):
		current_date = (first_day + datetime.timedelta(days=day)).date()
		bets_today = player_bets.iloc[player_bets["bet_date"].values == current_date]
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

	betting_days = (frequency_percentage / 100) * age_in_days

	average_bets_per_day = len(player_bets) / betting_days  # taken from LaBrie 2008
	return average_bets_per_day


def average_bet_size(player_bets):
	"""
	The average (mean) size of bets.
	"""
	check_measure_data(player_bets, ["bet_size"])
	average_bet_size = player_bets["bet_size"].sum() / len(player_bets)
	return average_bet_size


def total_wagered(player_bets):
	"""
	The total amount wagered (sum of bet sizes).
	"""
	check_measure_data(player_bets, ["bet_size"])
	return player_bets["bet_size"].sum()


def net_loss(player_bets):
	"""
	The net amount lost (sum of bet sizes minus sum of payout sizes).
	"""
	check_measure_data(player_bets, ["bet_size", "payout_size"])
	net_loss_value = player_bets["bet_size"].sum() - player_bets["payout_size"].sum()
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

	check_measure_data(player_bets, ["bet_count"])
	return player_bets["bet_count"].sum()


def average_bets_per_day_daily(player_bets):
	"""
	The average (mean) number of bets made on days where betting took place to be used on daily aggregate data.
	"""

	age_in_days = duration(player_bets)
	frequency_percentage = frequency(player_bets)

	betting_days = (frequency_percentage / 100) * age_in_days

	average_bets_per_day = (
		number_of_bets_daily(player_bets) / betting_days  # taken from LaBrie 2008
	)
	return average_bets_per_day


def average_bet_size_daily(player_bets):
	"""
	The average (mean) size of bets to be used on daily aggregate data.
	"""

	check_measure_data(player_bets, ["bet_size"])
	average_bet_size = player_bets["bet_size"].sum() / number_of_bets_daily(player_bets)
	return average_bet_size


# braverman measures


def intensity_daily(player_bets):
	"""
	Mean number of bets per active betting day in first month, if data set contains daily aggregate data.
	"""

	first_day = player_bets.iloc[0]["bet_time"]
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets["bet_time"] <= one_month_later]
	result = first_month_bets["bet_count"].mean()
	return result


def frequency_daily(player_bets):
	"""
	Number of active betting days in first month, if data set contains daily aggregate data.
	"""

	first_day = player_bets.iloc[0]["bet_time"]
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets["bet_time"] <= one_month_later]

	return len(first_month_bets)


def variability_daily(player_bets):
	"""
	Standard deviation of stake size in first month, if data set contains daily aggregate data.
	"""

	first_day = player_bets.iloc[0]["bet_time"]
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets["bet_time"] <= one_month_later]

	return first_month_bets["bet_size"].std()


def trajectory_daily(player_bets, plot=False):
	"""
	Gradient of a linear regression fitted to the sequence of daily aggredated bet sizes.
	"""

	first_day = player_bets.iloc[0]["bet_time"]
	one_month_later = first_day + datetime.timedelta(days=+30)
	first_month_bets = player_bets[player_bets["bet_time"] <= one_month_later]

	# first_month_bets['mean_bet_size'] = first_month_bets['bet_size'] / first_month_bets['bet_count']

	x = np.array(range(len(first_month_bets))).reshape((-1, 1)) + 1
	y = first_month_bets["bet_size"].values

	model = LinearRegression().fit(x, y)
	r_sq = model.score(x, y)

	model_x = x
	model_y = model.coef_ * x + model.intercept_

	if plot:
		plt.figure()
		plt.scatter(x, y)
		plt.plot(model_x, model_y, color="r")
		plt.show()

	trajectory = model.coef_[0]
	return model.coef_[0]





def calculate_labrie_measures(
    all_player_bets,
    savedir="",
    filename="gamba_labrie_measures.csv",
    loud=False,
    daily=True,
):
    """
	Calculates the set of measures described in LaBrie et al's work in 2008 on casino gamblers.
	These measures include the durations, frequencies, number of bets, bets per day, value per bet (eth), total amount wagered, net loss, and percent loss for each player.
	As this method sits in the studies module, it accepts a list of dataframes representing each player's bets as input.
	By default, this method saves the resulting dataframe of each player's measures to 'gamba_labrie_measures.csv'.
	Be advised: this method can take some time for large numbers of players, the 'loud' parameter can be set to True to print out updates every 200 players.

	Args:
		all_player_bets (Dataframe): All of the bets made by all of the players in the data set.
		savedir (String): The directory in which to save the resulting labrie measures dataframe, default is ''.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.

	"""

    # load in all files (can take some time)

    player_id = []
    duration = []
    frequency = []
    number_of_bets = []
    average_bets_per_day = []
    average_bet_size = []
    total_wagered = []
    net_loss = []
    percent_loss = []

    unique_players = list(set(all_player_bets["player_id"]))

    print(
        "calculating LaBrie measures for",
        len(unique_players),
        "players, this may take some time...",
    )

    for i in tqdm(range(len(unique_players))):
        player_bets = all_player_bets[all_player_bets["player_id"] == unique_players[i]]
        player_id.append(player_bets.iloc[0]["player_id"])
        duration.append(duration(player_bets))
        frequency.append(frequency(player_bets))
        if daily:
            number_of_bets.append(number_of_bets_daily(player_bets))
            average_bets_per_day.append(average_bets_per_day_daily(player_bets))
            average_bet_size.append(average_bet_size_daily(player_bets))
        else:
            number_of_bets.append(number_of_bets(player_bets))
            average_bets_per_day.append(average_bets_per_day(player_bets))
            average_bet_size.append(average_bet_size(player_bets))
        total_wagered.append(total_wagered(player_bets))
        net_loss.append(net_loss(player_bets))
        percent_loss.append(percent_loss(player_bets))

    labrie_dict = {
        "player_id": player_id,
        "duration": duration,
        "frequency": frequency,
        "num_bets": number_of_bets,
        "average_bets_per_day": average_bets_per_day,
        "average_bet_size": average_bet_size,
        "total_wagered": total_wagered,
        "net_loss": net_loss,
        "percent_loss": percent_loss,
    }

    labrie_measures = pd.DataFrame.from_dict(labrie_dict)
    labrie_measures.to_csv(savedir + filename, index=False)

    if loud:
        print("LaBrie measures saved")

    return labrie_measures


def calculate_braverman_measures(all_player_bets, savedir="", loud=False):
    """
	Calculates the set of measures described in Braverman and Shaffer's work in 2010 on high risk internet gamblers.
	These measures include the frequency, intensity, variability, and trajectories of each player.
	As this method sits in the studies module, it accepts a list of dataframes representing each player's bets as input.
	By default, this method saves the resulting dataframe of each player's measures to 'gamba_braverman_measures.csv'.

	Args:
		all_player_bets (Dataframe): All of the bets made by all of the players in the data set.
		savedir (String): The directory in which to save the resulting Braverman measures dataframe, default is ''.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.

	"""
    player_id = []

    intensity = []
    variability = []
    frequency = []
    trajectory = []

    sum_of_stakes = []
    total_num_bets = []
    average_bet_size = []
    duration = []
    net_loss = []

    unique_players = list(set(all_player_bets["player_id"]))

    for i in tqdm(range(len(unique_players))):
        player_bets = all_player_bets[all_player_bets["player_id"] == unique_players[i]]

        player_id.append(player_bets.iloc[0]["player_id"])
        intensity.append(intensity_daily(player_bets))
        frequency.append(frequency_daily(player_bets))
        variability.append(variability_daily(player_bets))
        trajectory.append(trajectory_daily(player_bets))

        sum_of_stakes.append(player_bets["bet_size"].sum())
        total_num_bets.append(player_bets["bet_count"].sum())
        average_bet_size.append(
            player_bets["bet_size"].sum() / player_bets["bet_count"].sum()
        )
        duration.append(duration(player_bets))
        net_loss.append(net_loss(player_bets))

    braverman_dict = {
        "player_id": player_id,
        "intensity": intensity,
        "frequency": frequency,
        "variability": variability,
        "trajectory": trajectory,
        "sum_of_stakes": sum_of_stakes,
        "total_num_bets": total_num_bets,
        "average_bet_size": average_bet_size,
        "duration": duration,
        "net_loss": net_loss,
    }

    braverman_measures = pd.DataFrame.from_dict(braverman_dict)
    braverman_measures.to_csv(savedir + "gamba_braverman_measures.csv", index=False)

    return braverman_measures