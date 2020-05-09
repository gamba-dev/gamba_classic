# study replication module

import numpy as np, glob, pandas as pd
from tqdm import tqdm
from scipy.stats import spearmanr

import gamba.measures as gb
import gamba.data as gd

import warnings
warnings.filterwarnings("ignore") # for SettingWithCopyWarning's from pandas

# starting with LaBrie 2007/8/9


def calculate_labrie_measures(all_player_bets, savedir='', filename='gamba_labrie_measures.csv', loud=False, daily=True):
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

	unique_players = list(set(all_player_bets['player_id']))

	print('calculating LaBrie measures for', len(unique_players), 'players, this may take some time...')

	for i in tqdm(range(len(unique_players))):
		player_bets = all_player_bets[all_player_bets['player_id'] == unique_players[i]]
		player_id.append(player_bets.iloc[0]['player_id'])
		duration.append(gb.duration(player_bets))
		frequency.append(gb.frequency(player_bets))
		if daily:
			number_of_bets.append(gb.number_of_bets_daily(player_bets))
			average_bets_per_day.append(gb.average_bets_per_day_daily(player_bets))
			average_bet_size.append(gb.average_bet_size_daily(player_bets))
		else:
			number_of_bets.append(gb.number_of_bets(player_bets))
			average_bets_per_day.append(gb.average_bets_per_day(player_bets))
			average_bet_size.append(gb.average_bet_size(player_bets))
		total_wagered.append(gb.total_wagered(player_bets))
		net_loss.append(gb.net_loss(player_bets))
		percent_loss.append(gb.percent_loss(player_bets))
	
	labrie_dict = {'player_id': player_id,
					'duration': duration,
					'frequency': frequency,
					'num_bets': number_of_bets,
					'average_bets_per_day': average_bets_per_day,
					'average_bet_size': average_bet_size,
					'total_wagered': total_wagered,
					'net_loss': net_loss,
					'percent_loss': percent_loss}

	labrie_measures = pd.DataFrame.from_dict(labrie_dict)
	labrie_measures.to_csv(savedir + filename, index=False)
	
	if loud:
		print('LaBrie measures saved')

	return labrie_measures


def calculate_braverman_measures(all_player_bets, savedir='', loud=False):
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
	
	unique_players = list(set(all_player_bets['player_id']))

	for i in tqdm(range(len(unique_players))):
		player_bets = all_player_bets[all_player_bets['player_id'] == unique_players[i]]

		player_id.append(player_bets.iloc[0]['player_id'])
		intensity.append(gb.intensity_daily(player_bets))
		frequency.append(gb.frequency_daily(player_bets))
		variability.append(gb.variability_daily(player_bets))
		trajectory.append(gb.trajectory_daily(player_bets))
		
		sum_of_stakes.append(player_bets['bet_size'].sum())
		total_num_bets.append(player_bets['bet_count'].sum())
		average_bet_size.append(player_bets['bet_size'].sum() / player_bets['bet_count'].sum())
		duration.append(gb.duration(player_bets))
		net_loss.append(gb.net_loss(player_bets))
		
	braverman_dict ={'player_id': player_id,
					'intensity':intensity, 
					'frequency':frequency, 
					'variability': variability, 
					'trajectory': trajectory, 
					'sum_of_stakes': sum_of_stakes, 
					'total_num_bets': total_num_bets, 
					'average_bet_size': average_bet_size, 
					'duration': duration, 
					'net_loss': net_loss}

	braverman_measures = pd.DataFrame.from_dict(braverman_dict)
	braverman_measures.to_csv(savedir + 'gamba_braverman_measures.csv', index=False)

	return braverman_measures

