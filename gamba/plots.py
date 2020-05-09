# plotting and data visualisation module
import matplotlib.pyplot as plt, numpy as np, math
import scipy.cluster.hierarchy as sch
import matplotlib.cm as cm
import scipy.ndimage.filters as snf
import matplotlib.ticker as mplt


def plot_measure_hist(measures, name):
	"""
	Plots a histogram for a named measure from a dataframe of measures.

	Args:
		measures (Dataframe): Collection of behavioural measures for a cohort of players.
		name (String): The name of the measure to plot, e.g. 'duration'.

	Returns:
		Matplotlib.pyplot plot object.

	"""

	plt.figure()
	data = measures[name].values
	n, bins, patches = plt.hist(data, bins=50, alpha=.5, label='data')
	xmin, xmax, ymin, ymax = plt.axis()
	plt.plot([data.mean(), data.mean()], [ymin, ymax * 0.95], label='mean')
	plt.plot([np.median(data), np.median(data)], [ymin, ymax * 0.95], label='median', color='green')
	plt.legend()
	plt.xlim(min(data), max(data))
	plt.xlabel(name)
	plt.ylim(min(n), max(n))
	return plt

def plot_measure_centile(measures, name, top_heavy=False):
    """
    Plots centiles of a single named measure from a dataframe of measures.

    Args:
        measures (Dataframe): Collection of behavioural measures for a cohort of players.
        name (String): The name of the measure to plot, e.g. 'duration'.
        top_heavy (Boolean): Whether to plot each centile (100), or to plot every 5 up to 95 followed by 96-100 as individual percentiles (discontinuous x axis). Default is False (plot 100 bars).

    Returns:
        Matplotlib.pyplot plot object.

    """

    plt.figure(figsize=(9,4))

    values = measures[name].values

    percentile_values = []

    percentiles = np.array(range(1, 101))

    if top_heavy:
        percentiles = list(range(5, 100, 5))
        percentiles.extend(list(range(96,101)))

    previous_cutoff = 0
    for percentile_group in percentiles:
        cutoff = np.percentile(values, percentile_group)

        this_group = [value for value in values if previous_cutoff <= value < cutoff]
        previous_cutoff = cutoff

        mean_value = 0
        if len(this_group) > 0:
            mean_value = np.mean(this_group)

        percentile_values.append(mean_value)

    # the +0.5 here shifts all bars down the x axis so that ticks line up with the start of the percentile
    if top_heavy:
        plt.bar(np.array(range(len(percentiles))[:19]) + 0.5, percentile_values[:19],
                alpha=0.5, edgecolor='black', linewidth=1, width=1, label='5% Group')
        plt.bar(np.array(range(len(percentiles))[19:]) + 0.5, percentile_values[19:],
                alpha=0.5, color='C1', edgecolor='black', linewidth=1, width=1, label='1% Group')
        plt.legend()

    else:
        plt.bar(np.array(range(len(percentiles))) + 0.5, percentile_values, alpha=0.5, edgecolor='black', linewidth=1, width=1)

    if top_heavy:
        plt.xticks(np.array(range(len(percentiles)))+1, percentiles)
        plt.xlim(0, len(percentiles))
        plt.grid(False)
    else:
        #plt.xticks(percentiles)
        plt.xlim(0, len(percentiles))

    plt.ylim(0, max(percentile_values) * 1.12)
    plt.ylabel('Mean ' + name.replace('_',' ').title())
    plt.xlabel('Percentile')

    return plt

def plot_measure_pair_plot(measures, label_override=None, thermal=False, figsize=(14,14)):

	"""
	Plots centiles of a single named measure from a dataframe of measures.

	Args:
		measures (Dataframe): Collection of behavioural measures for a cohort of players.
		label_override (List of Strings): List of axis labels, if None, the column names directly from the measures dataframe will be used.
		thermal (Boolean): Show 2D histograms instead of scatter plots (better for perceiving density).
		figsize (Tuple of Integers (2)): Size of the resulting plot, (14,14) is good for large numbers of measures (5+).

	Returns:
		Matplotlib.pyplot plot object.

	"""
	colnames = list(measures.columns)[1:]
	plt.rcParams["figure.figsize"] = figsize

	num_measures = len(colnames)

	fig, ax = plt.subplots(nrows=num_measures, ncols=num_measures)

	for y, row in enumerate(ax):
		for x, col in enumerate(row):	   

			if x != y:
				col.scatter(measures[colnames[x]].values, measures[colnames[y]].values)
			
				if thermal:					
					xlim = col.get_xlim()
					ylim = col.get_ylim()
					x_increment = (xlim[1]-xlim[0])/25.0
					y_increment = (ylim[1]-ylim[0])/25.0
					xrange = np.arange(xlim[0], xlim[1] + x_increment, x_increment)
					yrange = np.arange(ylim[0], ylim[1] + y_increment, y_increment)
					heatmap_raw, xedges, yedges = np.histogram2d(measures[colnames[x]].values, measures[colnames[y]].values, bins=(xrange, yrange))
					heatmap = snf.gaussian_filter(heatmap_raw, sigma=2)
					img = heatmap.T
					X, Y = np.meshgrid(xedges, yedges)
					col.pcolormesh(X, Y, img, cmap=cm.jet)
					col.set_xlim(xlim)
					col.set_ylim(ylim)
			else:
				col.hist(measures[colnames[x]], color='C2', bins=25)

			if y != len(colnames) - 1:
				col.axes.xaxis.set_ticklabels([])
				col.xaxis.set_ticks_position('none')
			if x != 0:
				col.axes.yaxis.set_ticklabels([])
				col.yaxis.set_ticks_position('none')
			
			if x == 0:
				if label_override == None:
					col.set_ylabel(colnames[y])
				else:
					col.set_ylabel(label_override[y])
			if y == len(colnames) - 1:
				if label_override == None:
					col.set_xlabel(colnames[x])
				else:
					col.set_xlabel(label_override[x])

	fig.subplots_adjust(wspace=0.1, hspace=0.1)
	return plt


# individual player transaction plots

def plot_player_career(player_df, savename=None):
	"""
		Creates a candlestick-style plot of a players betting activity over the course of their career.
		This works best on regularly-spaced sequential data but can also provide insight into intra-session win/loss patterns.

	Args:
		player_df (Dataframe): Collection of player bets, must include columns 'bet_size','payout_size','bet_time', and 'payout_time'.
		savename (String): If given, saves the resulting plot to the name supplied, e.g. 'player_bets.png'.

	Returns:
		Matplotlib.pyplot plot object.

	"""
	plt.figure(figsize=[5,3])
	previous_y_end = 0
	for i, bet in player_df.iterrows():
		bet_size = bet['bet_size']
		payout_size = bet['payout_size']
		bet_time = bet['bet_time']
		payout_time = bet['payout_time']

		start_y = previous_y_end
		end_y = 0

		# if bet loses
		if payout_size < bet_size:
			end_y = start_y - bet_size
			#plt.plot([2*i, 2*i + 1], [bet_size, payout_size], marker='o', color='red')
			plt.plot([i,i], [start_y, end_y], marker='o', color='#d30505', markersize=12)
		else:
			end_y = start_y + payout_size
			#plt.plot([2*i, 2*i + 1], [bet_size, payout_size], marker='o', color='green')
			plt.plot([i,i], [start_y, end_y], marker='o', color='#00B007', markersize=12)

		previous_y_end = end_y

	plt.xlabel(None)
	if savename != None:
		plt.savefig(savename, dpi=200, transparent=True)
	
	return plt

def plot_player_career_split(player_df):
	"""
	Plot a player's betting and payout trajectory on a single plot, with green indicating payouts (top) and red indicating bets (bottom).
	A cumulative value line is also plotted between the two.

	Args:
		player_df (Dataframe): Collection of player bets, must include columns 'bet_size','payout_size','bet_time', and 'payout_time'.
		
	Returns:
		Matplotlib.pyplot plot object.

	"""
	plt.figure()
	
	previous_y_end = 0
	for i, bet in player_df.iterrows():
		bet_size = bet['bet_size']
		payout_size = bet['payout_size']
		bet_time = bet['bet_time']
		payout_time = bet['payout_time']

		start_y = previous_y_end	
		end_y = 0

		# if bet loses
		if payout_size < bet_size:
			end_y = start_y - bet_size
			#plt.plot([2*i, 2*i + 1], [bet_size, payout_size], marker='o', color='red')
			plt.plot([i,i], [start_y, end_y], marker='o', color='red')
		else:
			end_y = start_y + payout_size
			#plt.plot([2*i, 2*i + 1], [bet_size, payout_size], marker='o', color='green')
			plt.plot([i,i], [start_y, end_y], marker='o', color='green')

		previous_y_end = end_y
		
	bets = player_df['bet_size'].values
	payouts = player_df['payout_size'].values
	plt.plot(range(len(bets)), np.cumsum(-bets), marker='o', color='red', label='Cumulative Bets')
	plt.plot(range(len(payouts)), np.cumsum(payouts), marker='o', color='green', label='Cumulative Payouts')
	plt.legend()
	plt.xlim(0, len(bets) * 1.02)
	plt.ylim(-max([sum(bets),sum(payouts)]), max([sum(bets),sum(payouts)]))
	return plt

def plot_player_radar(values, lims=(-1,1), loud=False):
	"""
	Creates a radar chart from a list of values, this is useful for visualising differences between 'typical' players in clusters or cohorts. 
	Values should be normalised (zscore). 
	[bug: first axis is not always at 12 o'clock]

	Args:
		values (List of Floats): The values to be plotted on the radar chart, values start at 12 o'clock on the radar and are plotted in clockwise order.
		lims (Tuple of Integers (2)): The inner and outer limits of the radar axes (all axes are the same as values shoud be normalised.).
	
	Returns:
		Matplotlib.pyplot plot object.

	"""

	values.append(values[0])
	N = len(values) - 1
	pi = math.pi
	# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
	
	angle = 2*pi/float(N)
	angles = [angle * n for n in reversed(range(N))]
	# rotate everything round 1/4 turn to put 0 at the top
	angles = [angle + (3/8 * 2 * pi) for angle in angles]
	
	for i, angle in enumerate(angles):
		if angle > 2 * pi:
			angles[i] = angles[i] - 2 * pi
	
	angles += angles[:1]

	# Initialise the spider plot
	fig = plt.figure()
	fig.patch.set_facecolor('white')
	ax = plt.subplot(111, polar=True)
	#plt.yticks([.25, .5, .75], [".25", ".5", ".75"], color="grey", size=7)
	plt.ylim(lims)

	# Draw one axis per variable + add labels labels yet
	tick_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)']
	plt.xticks(angles[:-1], tick_labels[:len(variable_names)], color='grey', size=8)

	ax.tick_params(pad=5)  # move the axis labels out a bit
	for label in (ax.get_xticklabels() + ax.get_yticklabels()):
		label.set_fontsize(13)

	# Draw ylabels
	ax.set_rlabel_position(0)  # degrees from horisontal to mark the ticks
	# Plot data
	ax.plot(angles, values, linewidth=1, linestyle='solid', color='blue')
	# Fill area
	ax.fill(angles, values, 'b', alpha=0.1)

	return plt


# clustering related plots

def plot_agglomeration_dendrogram(model, dt_cutoff=None, **kwargs):
	"""
	Create a dendrogram visualising a heirarchical clustering method (agglomerative clustering).
	A horisontal line can be added using the dt_cutoff parameter to visualise the number of clusters at a given distance threshold.

	Args:
		model (sklearn.cluster model): A trained sklearn clustering model, e.g. sklearn.cluster.AgglomerativeClustering.
		dt_cutoff (Integer): The distance threshold value at which to mark a grey dashed horisontal line.
	
	Returns:
		Matplotlib.pyplot plot object.

	"""
	# Create linkage matrix and then plot the sch.dendrogram
	# create the counts of samples under each node
	counts = np.zeros(model.children_.shape[0])
	n_samples = len(model.labels_)
	for i, merge in enumerate(model.children_):
		current_count = 0
		for child_idx in merge:
			if child_idx < n_samples:
				current_count += 1  # leaf node
			else:
				current_count += counts[child_idx - n_samples]
		counts[i] = current_count

	linkage_matrix = np.column_stack([model.children_, model.distances_,
									  counts]).astype(float)

	# Plot the corresponding dendrogram
	plt.figure(figsize=(12,4))
	plt.title('Hierarchical Clustering dendrogram')
	sch.dendrogram(linkage_matrix, truncate_mode='level', p=3)
	if dt_cutoff != None:
		plt.plot(list(plt.xlim()), [dt_cutoff, dt_cutoff], linestyle='--', color='grey')
	plt.xlabel("Number of points in node (or index of point if no parenthesis).")
	plt.ylabel('Distance threshold')
	plt.grid(False)
	return plt

def plot_cluster_sizes(model):
	"""
	Create a bar chart using a previously computed clustering model.
	Each bar represents a single cluster, with the height of the bars representing the number of members (players) in each cluster.

	Args:
		model (sklearn.cluster model): A trained sklearn clustering model, e.g. sklearn.cluster.AgglomerativeClustering.

	Returns:
		Matplotlib.pyplot plot object.

	"""
	plt.figure()
	cluster_ids = list(set(list(model.labels_)))
	cluster_sizes = [list(model.labels_).count(x) for x in cluster_ids]
	plt.bar(cluster_ids, cluster_sizes, color=plt.rcParams['axes.prop_cycle'].by_key()['color'])
	locs, labels = plt.xticks()
	plt.xticks(range(len(cluster_ids)), cluster_ids)
	plt.xlabel('Cluster ID')
	plt.ylabel('Number of Players per Cluster')
	plt.grid(axis='x')
	return plt


# correlation plots

def color_matrix(matrix, cmap):
	"""
	
	
	"""

	results_size = len(correlations.columns)
	values = np.empty((results_size, results_size), dtype=object)
	for r, row in enumerate(correlations.values):
		for e, element in enumerate(row):
			if element == '-':
				values[r, e] = 100
				continue
			if element == '':
				values[r, e] = np.nan
				continue
			if '*' in str(element):
				value = element.replace('*', '')
				values[r, e] = float(value)*100
			else:
				values[r, e] = element*100

	current_cmap = matplotlib.cm.get_cmap(cmap)
	current_cmap.set_bad(color='white')
	plt.imshow(np.array(values).astype(np.float), cmap=current_cmap);
	plt.yticks(range(len(correlations.columns)), list(correlations.columns))
	plt.xticks(range(len(correlations.columns)), list(correlations.columns))
	plt.xticks(rotation=90)
	cbar=plt.colorbar()
	cbar.set_ticks([-100,-80,-60,-40,-20,0,20,40,60,80,100])
	cbar.set_ticklabels([-1, -0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1])
	plt.ylabel('test')
	return plt
