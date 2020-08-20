# machine learning module

import numpy as np, pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
import statistics
import matplotlib.pyplot as plt

import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier

# statsquest on youtube is useful


def k_means(measures_table, clusters=4, data_only=False, plot=False, loud=False):
	"""
	Applies the k-means clustering algorithm to a measures table.
	The resulting clustering is then reported in terms of its inertia (sum of squared distances of samples to their closest cluster center) and its silhouette score (how distinct clusters are within the sample 
	[see the skikit learn docs for details]).
	The measures passed as the first parameter can be returned with an added column reporting the cluster each player belongs to using the data_only parameter.

	Parameters
	----------
	measures_table : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		Behavioural measures for a collection of players.
	clusters : int
		Number of clusters to compute, default is 4.
	data_only : bool
		Whether or not to only return the clustered measures and not the goodness of fit measures, default is False (return only the inertia and silhouette scores).
	plot : bool
		Whether or not to plot the distribution of players within the clusters as a bar chart, default is False.
	loud : bool
		Whether or not to output status updates as the function progresses, default is False.
	
	Returns
	----------
	item : tuple 
		(Inertia, Silhouette, Clustered measures table) OR just the dataframe.

	Examples 
	----------
	>>> # this doesn't work yet but put code here
	

	"""

	# get variable names from the behavioural measures
	variables = list(measures_table.columns)[1:]

	Kmean = KMeans(n_clusters=clusters)

	data = np.array(measures_table[variables].values)
	Kmean.fit(data)

	silhouette = metrics.silhouette_score(data, Kmean.labels_, metric="euclidean")

	cluster_centers = Kmean.cluster_centers_

	clustered_data = measures_table.copy()
	clustered_data["cluster"] = Kmean.labels_

	if loud:
		print("variables:", variables)
		print("centers:", Kmean.cluster_centers_)
		print("inertia:", Kmean.inertia_)
		print("silhouette:", silhouette)

	if plot:
		bars = []
		heights = []
		for label in set(sorted(Kmean.labels_)):
			bars.append(label)
			heights.append(list(Kmean.labels_).count(label))

		colors = ["C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
		plt.bar(bars, heights, color=colors[: len(bars)])
		plt.title(
			"\nClusters: "
			+ str(len(bars))
			+ "\nInertia: "
			+ str(round(Kmean.inertia_))
			+ "\nIterations: "  # Kmean.inertia_ is the sum of squared distances of samples to their closest cluster center
			+ str(Kmean.n_iter_),
			x=1.01,
			y=0.5,
			ha="left",
		)
		plt.xlabel("Cluster ID")
		plt.ylabel("Number of Members")
		plt.show()

	if data_only:
		return clustered_data

	return clustered_data, Kmean.inertia_, silhouette


def k_means_range(measures_table, min_clusters=2, max_clusters=13):
	"""
	Computes the k_means calculation above across a range of cluster counts, returning their goodness of fit measures (inertia and silhouette).

	Parameters
	----------
	measures_table : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		Behavioural measures for a collection of players.
	min_clusters : int
		The minimum number of clusters to compute, default is 2.
	max_clusters : int
		The maximum (inclusive) number of clusters to compute, default is 13.

	Returns
	----------
		Two arrays, the inertias for each of the cluster counts, and the silhouette scores for each of the cluster counts.

	"""

	# print('calculating k means in range', min_clusters, max_clusters)

	inertias = []
	silhouettes = []

	for x in range(min_clusters, max_clusters + 1):
		k_means_result = k_means(measures_table, clusters=x)
		inertias.append(k_means_result[1])
		silhouettes.append(k_means_result[2])

	return inertias, silhouettes


def k_means_ensemble(measures_table, ensemble_size=100, min_clusters=2, max_clusters=13):
	"""
	Computes the k_means clustering algorithm across a range of cluster counts, a number of times.
	This is useful for determining clusters in a more robust way but can be slow on large data sets.

	Parameters
	----------
	measures_table : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		Behavioural measures for a collection of players.
	ensemble_size : int
		The number of times to repeat the clustering computations, default is 100.
	min_clusters : int
		The minimum number of clusters to compute, default is 2.
	max_clusters : int
		The maximum (inclusive) number of clusters to compute, default is 13.

	Returns
	----------
		Two arrays, the mean inertias for each of the cluster counts, and the mean silhouette scores for each of the cluster counts.

	"""

	all_inertias = []
	all_silhouettes = []

	# call the k_means_range function n times, storing scores in the above arrays
	for x in range(ensemble_size):
		k_means_range_result = k_means_range(
			measures_table, min_clusters=min_clusters, max_clusters=max_clusters
		)
		all_inertias.append(k_means_range_result[0])
		all_silhouettes.append(k_means_range_result[1])

	# now average each of the elements in the score lists
	ensemble_inertias = []
	ensemble_silhouettes = []
	for cluster_num in range(len(all_inertias[0])):
		inertia_scores = [all_inertias[x][cluster_num] for x in range(ensemble_size)]
		ensemble_inertias.append(statistics.mean(inertia_scores))

		silhouette_scores = [
			all_silhouettes[x][cluster_num] for x in range(ensemble_size)
		]
		ensemble_silhouettes.append(statistics.mean(silhouette_scores))

	return ensemble_inertias, ensemble_silhouettes


def agglomerative_cluster(measures_table, distance_threshold=0, n_clusters=None):
	"""
	Performs sklearn's agglomerative clustering algorithm on a dataframe of behavioural measures.
	See their documentation for details.
	Note: Either the distance threshold or the n_cluster parameter must be None.

	Parameters
	----------
	measures_table : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		Behavioural measures for a collection of players.
	distance_threshold : int
		The maximum distance threshold to perform the clustering to.
	n_clusters : int
		The number of clusters to perform the clustering to.

	Returns
	----------
	model : sklearn.AgglomerativClustering
		A fit agglomerative clustering model.

	"""
	variables = list(measures_table.columns)[1:]
	X = measures_table[variables].values

	model = AgglomerativeClustering(
		distance_threshold=distance_threshold, n_clusters=n_clusters
	)
	model = model.fit(X)
	return model


def describe_clusters(clustered_measures_table, cluster_col="cluster"):
	"""
	Describes cluster centroids (mean values of each measure) for each cluster in a clustered measures table.

	Parameters
	----------
	clustered_measures_table : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		A measures table with a cluster column (e.g. output of k_means() function).

	Returns
	--------
	dataframe
		A table describing each cluster as a pandas dataframe.

	"""
	unique_clusters = list(set(clustered_measures_table["cluster"].values))

	descriptive_table = pd.DataFrame()
	descriptive_table["cluster_centroid"] = clustered_measures_table.columns[1:]

	for value in unique_clusters:
		members = clustered_measures_table[
			clustered_measures_table[cluster_col] == value
		]
		centroid = [members[col].mean() for col in members.columns[1:]]
		descriptive_table["n=" + str(len(members))] = centroid

	descriptive_table.set_index("cluster_centroid", inplace=True)
	return descriptive_table


def logistic_regression(train_measures, test_measures, label):
	"""
	Performs a logistic regression using the `statsmodels library <https://www.statsmodels.org/stable/index.html>`_, returning the predicted labels rounded to the nearest integer.

	Note: this method is currently hard-coded to only function on Philander 2014's data set. Abstracted logistic regression function coming soon tm.

	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	"""


	# defines the R style formula to fit
	formula = str(label) + " ~ gender+age+total_wagered+num_bets+frequency+duration+bets_per_day+net_loss+intensity+variability+frequency_1m+trajectory+z_intensity+z_variability+z_frequency+z_trajectory"
	model = sm.formula.glm(formula=formula, family=sm.families.Binomial(), data=train_measures)
	
	# this is where the stepwise bit could happen - see original code
	fit_model = model.fit()

	raw_prediction = fit_model.predict(test_measures)
	predicted_labels = [value for value in np.where(raw_prediction >= 0.5, 1, 0)]

	#print(fit_model.summary())
	return predicted_labels

def lasso_logistic_regression(train_measures, test_measures, label):
	"""
	Performs a 'lasso' (optimizes a least-square problem with L1 penalty) logistic regression using `sklearn's linear_model <https://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model>`_.
	This `stackoverflow post <https://stackoverflow.com/questions/41639557/how-to-perform-logistic-lasso-in-python>`_ contains a useful discussion on this type of function-estimation regression pair.

	
	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.
	

	"""
	
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = LogisticRegression(penalty='l1', solver='liblinear')
	
	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)
	
	return predicted_labels


def svm_eps_regression(train_measures, test_measures, label):
	"""
	Creates and trains a support vector machine for epsilon-support vector regression using the sklearn library's implementation.
	

	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	"""
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = svm.SVR(kernel='rbf')

	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)

	# convert probabilities to binary labels for comparison
	regression_cutoff = 0.5
	predicted_labels = np.where(predicted_labels < regression_cutoff, 0, 1)
	
	return predicted_labels

def svm_c_classification(train_measures, test_measures, label):
	"""

	
	
	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	"""
	
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = svm.SVC(kernel='rbf')

	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)
	
	return predicted_labels

def svm_one_classification(train_measures, test_measures, label):
	"""

	
	
	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	"""
	
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = svm.OneClassSVM(kernel='rbf')

	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)

	# need to add a correction step for the labels here as OneClassSVM returns -1 for outliers and 1 for inliers
	predicted_labels = np.where(predicted_labels < 0, 1, 0)
	
	return predicted_labels


def rf_regression(train_measures, test_measures, label):

	"""
	Creates and fits a random forest regressor using `sklearn's ensemble module <https://scikit-learn.org/stable/modules/ensemble.html#forest>`_, returning the predicted labels rounded to the nearest integer.
	
	
	
	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	
	"""
	
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = RandomForestRegressor()

	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)

	# convert probabilities to binary labels for comparison
	regression_cutoff = 0.5
	predicted_labels = np.where(predicted_labels < regression_cutoff, 0, 1)

	return predicted_labels

def rf_classification(train_measures, test_measures, label):
	"""

	
	
	Parameters
	------------
	train_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The training portion of a measures table returned by the `split_measures_table` function in the measures module.
	test_measures : `dataframe <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html>`_
		The (smaller) test portion of a measures table returned by the `split_measures_table` function in the measures module.
	label : string
		The column name of the dependent variable in the train and test measures tables, e.g. 'self_exclude'.

	Returns
	--------
	list
		A list corresponding to the predicted values for the label column in the test measures table. These can be used with the actual values to compute performance metrics.

	"""
	
	train_data = train_measures.drop(['player_id', label], axis=1)
	train_labels = train_measures[label]
	test_data = test_measures.drop(['player_id', label], axis=1)
	
	model = RandomForestClassifier(n_estimators=100)

	model.fit(train_data, train_labels)

	predicted_labels = model.predict(test_data)

	return predicted_labels



def compute_performance(method_name, actual, predicted):
	"""
	Computes performance metrics including sensitivity, specificity, accuracy, confusion matrix values, odds ratio, and area under curve, for a given classification/regression using its actual and predicted values.

	Parameters
	-----------
	method_name : string
		The name of the method which has been applied (for labelling the final performance table), e.g. 'random forest classification'.
	actual : list
		The actual values of the test measures table.
	predicted : list
		The values predicted by the method for the test measures table.

	"""
	# resources:
	# describes odds ratio and precision equations
	# https://cran.r-project.org/web/packages/ROCR/ROCR.pdf
	# describes sklearn's confusion matrix
	# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html#sklearn-metrics-confusion-matrix

	result = metrics.classification_report(actual, y_pred=predicted, output_dict=True)
	sensitivity = result['1']['recall']
	specificity = result['0']['recall']
	accuracy = result['accuracy']
	fpr, tpr, thresholds = metrics.roc_curve(actual, predicted)
	auc = metrics.auc(fpr, tpr)
	confusion_matrix = metrics.confusion_matrix(actual, predicted)
	tn, fp, fn, tp = confusion_matrix.ravel()
	
	# odds ratio is (tp x tn)/(fp x fn)
	odds_ratio = 0
	if fp != 0 and fn != 0:
		odds_ratio = (tp * tn)/(fp * fn)
		
	# precision is tp / (tp + fp)
	precision = tp / (tp + fp)

	metrics_df = pd.DataFrame()
	metrics_df['sensitivity'] = [round(sensitivity, 3)]
	metrics_df['specificity'] = [round(specificity, 3)]
	metrics_df['accuracy'] = [round(accuracy, 3)]
	metrics_df['precision'] = [round(precision, 3)]
	metrics_df['auc'] = [round(auc, 3)]
	metrics_df['odds_ratio'] = [round(odds_ratio, 3)]
	metrics_df.index = [method_name]
	return metrics_df




# =========================================================
# Plotting Functions for the Machine Learning Module
# =========================================================


import scipy.cluster.hierarchy as sch
import scipy.ndimage.filters as snf


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
	plt.bar(
		cluster_ids,
		cluster_sizes,
		color=plt.rcParams["axes.prop_cycle"].by_key()["color"],
	)
	locs, labels = plt.xticks()
	plt.xticks(range(len(cluster_ids)), cluster_ids)
	plt.xlabel("Cluster ID")
	plt.ylabel("Number of Players per Cluster")
	plt.grid(axis="x")
	return plt

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

	linkage_matrix = np.column_stack(
		[model.children_, model.distances_, counts]
	).astype(float)

	# Plot the corresponding dendrogram
	plt.figure(figsize=(12, 4))
	plt.title("Hierarchical Clustering dendrogram")
	sch.dendrogram(linkage_matrix, truncate_mode="level", p=3)
	if dt_cutoff != None:
		plt.plot(list(plt.xlim()), [dt_cutoff, dt_cutoff], linestyle="--", color="grey")
	plt.xlabel("Number of points in node (or index of point if no parenthesis).")
	plt.ylabel("Distance threshold")
	plt.grid(False)
	return plt

