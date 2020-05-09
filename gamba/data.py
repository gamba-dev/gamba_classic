# data loading and storage module

# dependencies
import pandas as pd, os, glob, numpy as np, datetime, warnings
from tqdm import tqdm


def help(advanced=False):
	"""
	Prints help to the console describing the columns required by other functions in the library.

	Args:
		advanced(Boolean): Show the more detailed column names and descriptors.
	
	"""

	if advanced:
		print()
		print('=== Advanced Data Module Help ===')
		print('payout_time: the time a payout is made (datetime)')
		print('success_probability: the probability of success (decimal between 0 and 1)')
		print('bet_count: to be used for daily aggregate data')
		return

	core_column_names = ['player_id','bet_time','bet_size','payout_size']
	extra_column_names = ['payout_time','bet_count','success_probability']
	print()
	print('=== Data Module Help ===')
	print('Read in your data using the gb.read_csv() method.')
	print()
	print('If it doesn\'t already, use the following column names so that the\nrest of the library knows which values to use;')
	print(core_column_names)
	print()
	print('If you\'re using more detailed data, the following column names can\nbe used, see the gamba.data documentation page for descriptors;')
	print(extra_column_names)

def prepare_labrie_data(filename, savedir='labrie_individuals/', loud=False, year=2008):
	"""
	Splits the original labrie data into CSV files for each individual's transactions and renames the columns to be compatable with the rest of the gamba library.
	
	Args:
		filename (String): The name of the file downloaded from the transparency project's website, e.g. 'home/data/DailyData.txt'.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
		year (Integer): The year of the publication the data was used in (this method works for either the 2007 or 2008 paper's data).
	
	"""

	labrie_data = None

	if year == 2008:
		labrie_data = pd.read_csv(
			filename, delimiter='\t', parse_dates=['Date'])
	elif year == 2007:
		labrie_data = pd.read_csv(filename, parse_dates=['Date'])

	# rename columns to make them compatable with gamba.measures
	if loud:
		print('original columns:', list(labrie_data.columns))

	if year == 2008:
		labrie_data.columns = ['player_id', 'bet_time',
							   'bet_size', 'payout_size', 'bet_count']
		labrie_data.to_csv('gamba_ready_labrie_data_2008.csv', index=False)
	elif year == 2007:
		labrie_data.columns = ['player_id', 'bet_time',
							   'product_id', 'bet_size', 'payout_size', 'bet_count']
		labrie_data.to_csv('gamba_ready_labrie_data_2007.csv', index=False)

	if loud:
		print('better columns:', list(labrie_data.columns))

	#split_individual_transactions(labrie_data, savedir)

	if loud:
		print('LaBrie data ready to use!')

	return labrie_data


def prepare_braverman_data(filename, loud=False):
	"""
	Splits the original Braverman and Shaffer data into CSV files for each indivdiual's transactions, and renames the columns to be compatable with the rest of the gamba library.

	Args:
		filename (String): The name of the file downloaded from the transparency project's website, e.g. 'home/data/DailyData.txt'.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
	
	"""
	braverman_data = pd.read_csv(filename, parse_dates=['TimeDATE'], delimiter='\t')

	braverman_data.columns = ['player_id', 'bet_time',
						'bet_size', 'payout_size', 'bet_count']

	# split_individual_transactions(raw_data, 'braverman_individuals/')

	if loud:
		print('Braverman data ready to use!')

	braverman_data.to_csv('gamba_ready_braverman_data.csv', index=False)
	return braverman_data


def split_individual_transactions(matched_df, savedir):
	"""
	Seperates all transactions from each unique player from the matched bet-payout dataframe of a single application.
	A CSV file is created in a new directory 'individuals/' containing each player's bets.

	Args:
		matched_df_csv (Dataframe): A collection of matched bet-payout transactions.
		savedir (Dataframe): The directory to save each individual's transaction dataframes.

	"""
	unique_players = list(set(matched_df['player_id']))

	if not os.path.exists(savedir):
		os.makedirs(savedir)
		print("Directory ", savedir, " Created ")
	else:
		print("Directory ", savedir, " already exists, clearing files...")
		files = glob.glob(savedir + '*')
		for f in files:
			os.remove(f)
		print("Directory ", savedir, " cleared.")

	print('extracting individual transactions for',
		  len(unique_players), 'players...')

	for i in tqdm(range(len(unique_players))):
		player_bets = matched_df[matched_df['player_id'] == unique_players[i]]
		player_bets.to_csv(savedir + str(unique_players[i]) + '.csv',
						   index=None, header=True)
		
	print('all individual transaction files saved.')




# pandas wrapper methods (for convenience)

def read_csv(file, parse_dates=[], index_col=None, delimiter=',', dummy_data=False):
	"""
	This method is a simple wrapper of pandas' **read_csv** function which only includes its date parsing, index_col, and delimiter functionality.
	Feel free to use pd.read_csv in place of this method if more specific paremeters are required.
	See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html for details.
	It can also be used to generate dummy transaction data for examples or to test new functionality.

	Args:
		file (String): The file to be loaded, e.g. 'data/transactions.csv'
		parse_dates (List of Strings): The names of the columns containing datetime data types, e.g. ['bet_time','payout_time']
		index_col (String): Which column to be used as the index, default is None.
		delimiter (String): The delimiter used in the file being read, default is ',' (CSV format).
		dummy_data (Boolean): Whether or not to ignore the other parameters and return dummy data.
	"""

	if dummy_data:
		print('todo: add dummy data gen code')

		df = pd.DataFrame({'USERID':['2345345','2153674','2364565'],
							'DATETIME':['this','is','unfinished'], # todo
							'ROUL_STAKE':[10,22,15],
							'RETURN':[0,44,0]})




		return df

	df = pd.read_csv(file, parse_dates=parse_dates,
					 index_col=index_col, delimiter=delimiter)

	return df


def concat(dfs, axis=0):
	"""
	This method is a wrapper of pandas' **concat** function.
	See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.concat.html for details.

	Args:
		dfs (List of Dataframes): The dataframes to be concatenated.
		axis (Integer): The axis to concatenate along (0 is add underneath, 1 is add along as new columns)
	
	"""
	df = pd.concat(dfs, axis=axis)
	return df


def load_directory(directory):
	"""
	Loads a directory containing a collection of CSV files in as dataframes, returning a list of dataframes.
	This is useful for calculating behavioural measures on collections of players by iterating over the returned list.

	Args:
		directory (String): The directory containing player CSV files, e.g. 'fixed_odds_players/'.

	Returns:
		List of dataframes where each dataframe is one player's transaction data.

	"""
	all_filenames = glob.glob(directory + '*.csv')
	all_player_bets = [read_csv(f, parse_dates=['bet_time']) for f in all_filenames]
	return all_player_bets


def summarise_app(player_bets):
	"""
	Prints out some basic information about a gambling or gambling-like application given a collection of bets made through that application.
	Data displayedi includes the number of users, the number of game types provided, the number of bets placed, the total value of the bets and the payouts, the time of the first bet, and the time of the last.
	
	Args:
		player_bets (Dataframe): Dataframe containing bets to a gambling application.
	
	"""
	users = set(df['player_id'].values)
	games = set(df['game_type'].values)
	bets = df['bet_size'].sum()
	payouts = df['payout_size'].sum()
	start_block = df['block_number'].min()
	end_block = df['block_number'].max()
	start = df['bet_time'].min()
	end = df['bet_time'].max()

	print('users:', len(users))
	print('games:', len(games))
	print('num bets:', len(df))
	print('bet value:', bets)
	print('payout value:', payouts)
	print('start:', start, int(start_block))
	print('end:', end, int(end_block))
	print('')



def dummy_measures_table(size=100):
	"""
	Creates a dummy measures table for use in the user guide and to practice some of the analytical techniques.

	Args:
		size (Integer): The number of players to generate measures for.
	"""

	# create the table
	measures_table = pd.DataFrame()

	# generate some player ids
	player_ids = []
	for x in range(size):
	    player_ids.append('anon_'+str(x))
	measures_table['player_ids'] = player_ids

	# make some durations (exponentially distributed)
	measures_table['duration'] = [int(x) for x in np.random.exponential(scale=1,size=(size,10)).sum(axis=1)]

	# make some frequencies (normally distributed)
	measures_table['frequency'] = [int(sorted((10,x,100))[1]) for x in np.random.normal(scale=60,size=size)]

	# make some total_wagered (also exponential but not integer)
	measures_table['total_wagered'] = [round(x,2) for x in np.random.exponential(scale=200,size=(size,2)).sum(axis=1)]

	# finally some num_bets (uniform)
	measures_table['num_bets'] = [int(x) for x in np.random.uniform(low=10, high=200, size=size)]

	return measures_table







