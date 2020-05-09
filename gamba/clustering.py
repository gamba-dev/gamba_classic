# clustering module

import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.cluster import AgglomerativeClustering
from statistics import mean
import matplotlib.pyplot as plt

# statsquest on youtube is useful

def k_means(measures, clusters=4, data_only=False, plot=False, loud=False):
	"""
	Applies the k-means clustering algorithm to a measures table.
	The resulting clustering is then reported in terms of its inertia (sum of squared distances of samples to their closest cluster center) and its silhouette score (how distinct clusters are within the sample 
	[see the skikit learn docs for details]).
	The measures passed as the first parameter can be returned with an added column reporting the cluster each player belongs to using the data_only parameter.

	Args:
		measures (Dataframe): Behavioural measures for a collection of players.
		clusters (Integer): Number of clusters to compute, default is 4.
		data_only (Boolean): Whether or not to only return the clustered measures and not the goodness of fit measures, default is False (return only the inertia and silhouette scores).
		plot (Boolean): Whether or not to plot the distribution of players within the clusters as a bar chart, default is False.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
	
	Returns:
		Tuple (Inertia, Silhouette score, Dataframe of measures including 'cluster' column of integers) OR just the dataframe.

	"""

	# get variable names from the behavioural measures
	variables = list(measures.columns)[1:]	

	Kmean = KMeans(n_clusters=clusters)

	data = np.array(measures[variables].values)
	Kmean.fit(data)
	
	silhouette = metrics.silhouette_score(data, Kmean.labels_, metric='euclidean')

	cluster_centers = Kmean.cluster_centers_
	
	clustered_data = measures.copy()
	clustered_data['cluster'] = Kmean.labels_

	if loud:
		print('variables:', variables)
		print('centers:', Kmean.cluster_centers_)
		print('inertia:', Kmean.inertia_)
		print('silhouette:', silhouette)
	
	if plot:
		bars = []
		heights = []
		for label in set(sorted(Kmean.labels_)):
			bars.append(label)
			heights.append(list(Kmean.labels_).count(label))
		
		colors = ['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
		plt.bar(bars, heights, color=colors[:len(bars)])
		plt.title('\nClusters: ' + str(len(bars)) +	  
				  '\nInertia: ' + str(round(Kmean.inertia_)) + # Kmean.inertia_ is the sum of squared distances of samples to their closest cluster center
				  '\nIterations: ' + str(Kmean.n_iter_), x = 1.01, y = 0.5, ha='left')
		plt.xlabel('Cluster ID')
		plt.ylabel('Number of Members')
		plt.show()
		
	if data_only:
		return clustered_data
	
	return clustered_data, Kmean.inertia_, silhouette


def k_means_range(measures, min_clusters=2, max_clusters=13):
	"""
	Computes the k_means calculation above across a range of cluster counts, returning their goodness of fit measures (inertia and silhouette).

	Args:
		measures (Dataframe): A collection of measures calculated in the measures module.
		min_clusters (Integer): The minimum number of clusters to compute, default is 2.
		max_clusters (Integer): The maximum (inclusive) number of clusters to compute, default is 13.

	Returns:
		Two arrays, the inertias for each of the cluster counts, and the silhouette scores for each of the cluster counts.
	"""

	#print('calculating k means in range', min_clusters, max_clusters)
	
	inertias = []
	silhouettes = []
	
	for x in range(min_clusters, max_clusters + 1):
		k_means_result = k_means(measures, clusters = x)
		inertias.append(k_means_result[1])
		silhouettes.append(k_means_result[2])
	
	return inertias, silhouettes


def k_means_ensemble(measures, ensemble_size=100, min_clusters=2, max_clusters=13):
	"""
	Computes the k_means clustering algorithm across a range of cluster counts, a number of times.
	This is useful for determining clusters in a more robust way but can be slow on large data sets.

	Args:
		measures (Dataframe): A collection of measures calculated in the measures module.
		ensemble_size (Integer): The number of times to repeat the clustering computations, default is 100.
		min_clusters (Integer): The minimum number of clusters to compute, default is 2.
		max_clusters (Integer): The maximum (inclusive) number of clusters to compute, default is 13.

	Returns:
		Two arrays, the mean inertias for each of the cluster counts, and the mean silhouette scores for each of the cluster counts.

	"""

	all_inertias = []
	all_silhouettes = []

	# call the k_means_range function n times, storing scores in the above arrays
	for x in range(ensemble_size):
		k_means_range_result = k_means_range(measures, min_clusters=min_clusters, max_clusters=max_clusters)
		all_inertias.append(k_means_range_result[0])
		all_silhouettes.append(k_means_range_result[1])
	    
	# now average each of the elements in the score lists
	ensemble_inertias = []
	ensemble_silhouettes = []
	for cluster_num in range(len(all_inertias[0])):
		inertia_scores = [all_inertias[x][cluster_num] for x in range(ensemble_size)]
		ensemble_inertias.append(mean(inertia_scores))

		silhouette_scores = [all_silhouettes[x][cluster_num] for x in range(ensemble_size)]
		ensemble_silhouettes.append(mean(silhouette_scores))

	return ensemble_inertias, ensemble_silhouettes


def agglomerative_cluster(measures, distance_threshold=0, n_clusters=None):
	"""
	Performs sklearn's agglomerative clustering algorithm on a dataframe of behavioural measures.
	See their documentation for details.
	Note: Either the distance threshold or the n_cluster parameter must be None.

	Args:
		measures (Dataframe): A collection of measures calculated in the measures module.
		distance_threshold (Integer): The maximum distance threshold to perform the clustering to.
		n_clusters (Integer): The number of clusters to perform the clustering to.

	"""	
	variables = list(measures.columns)[1:]
	X = measures[variables].values
	
	model = AgglomerativeClustering(distance_threshold=distance_threshold, n_clusters=n_clusters)
	model = model.fit(X)
	return model



def describe_clusters(clustered_measures_table, cluster_col='cluster'):
	"""
	Describes cluster centroids (mean values of each measure) for each cluster in a clustered measures table.

	Args:
		clustered_measures_table (DataFrame): A measures table with a cluster column (e.g. output of k_means() function)

	"""
	unique_clusters = list(set(clustered_measures_table['cluster'].values))

	descriptive_table = pd.DataFrame()
	descriptive_table['cluster_centroid'] = clustered_measures_table.columns[1:]

	for value in unique_clusters:
		members = clustered_measures_table[clustered_measures_table[cluster_col] == value]
		centroid = [members[col].mean() for col in members.columns[1:]]
		descriptive_table['n='+str(len(members))] = centroid

	descriptive_table.set_index('cluster_centroid', inplace=True)
	display(descriptive_table)