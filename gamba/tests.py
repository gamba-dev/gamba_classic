# statistical tests/decsriptions module

import pandas as pd, numpy as np, math
from scipy import stats


def descriptive_table(measures_table, loud=False, extended=False):
    """
	Creates the first table found in LaBrie et al's 2008 paper, which presents descriptive statistics for each of the behavioural measures they calculated.
	These include the mean, standard deviation, and median, of each behavioural measure.

	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
	
	Returns:
		Dataframe describing the behavioural measures provided.
	"""
    # first pull all of the data out of the dictionary for more readable use
    # later on
    measure_names = list(measures_table.columns)[1:]

    means = []
    stds = []
    medians = []
    stats.iqrs = []
    for measure in measure_names:
        means.append(measures_table[measure].mean())
        stds.append(measures_table[measure].std())
        medians.append(measures_table[measure].median())
        stats.iqrs.append(stats.iqr(measures_table[measure].values))

    if loud:
        print("calculating descriptive statistics for LaBrie measures")

    descriptive_df = pd.DataFrame(columns=["measure", "mean", "std", "median"])

    descriptive_df["measure"] = measure_names
    descriptive_df["mean"] = means
    descriptive_df["std"] = stds
    descriptive_df["median"] = medians
    if extended:
        descriptive_df["iqr"] = stats.iqrs

    descriptive_df.set_index("measure", inplace=True)
    descriptive_df = descriptive_df.rename_axis(None)

    return descriptive_df


def ks_test(measures_table):
    """
	Performs a one sample Kolmogorov-Smirnov test.
	This approximately indicates whether or not a collection of calculated behavioural measures are normally distributed.

	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
	
	Returns:
		Dataframe containing the K-S test scores and p-values of the behavioural measures provided.

	"""

    measure_names = list(measures_table.columns)[1:]

    scores = []
    pvals = []
    for measure in measure_names:
        result = stats.kstest(measures_table[measure], "norm")
        scores.append(result[0])
        pvals.append(result[1])

    ks_table = pd.DataFrame(columns=["Measure", "K-S Score", "p"])

    ks_table["Measure"] = measure_names
    ks_table["K-S Score"] = scores
    ks_table["p"] = pvals

    ks_table.set_index("Measure", inplace=True)
    ks_table.rename_axis(None, inplace=True)

    return ks_table


def cohens_d(measures_table, label):
    """
	Calculates Cohen's d value between the behavioural measures of two groups of players. 
	Groups are distinguished using a label column which is either 1 (in group) or 0 (not in group).
	For example, the column 'in_top5' may represent whether or not a player is in the top 5 % of players by total amount wagered, and would be 1 or 0 for the top 5 and remaining 95 percent respectively.

	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
		label (String): The name of the column representing the group's label, e.g. 'in_top5'.
	
	Returns:
		Dataframe containing Cohen's d values between each of the labelled groups for each of the behavioural measures provided.
	"""

    control_group = measures_table[measures_table[label] == 0]

    experimental_group = measures_table[measures_table[label] == 1]

    measure_names = list(measures_table.columns)[1:]

    # remove the label column (no point doing cohens d on it)
    measure_names.remove(label)

    d_results = []
    # do cohens d for each measure
    for measure in measure_names:
        control_measure = control_group[measure]
        experimental_measure = experimental_group[measure]

        control_mean = control_measure.mean()
        experimental_mean = experimental_measure.mean()

        control_sd = control_measure.std()
        experimental_sd = experimental_measure.std()

        control_n = len(control_measure)
        experimental_n = len(experimental_measure)

        top_line = ((control_n - 1) * control_sd ** 2) + (
            (experimental_n - 1) * experimental_sd ** 2
        )

        pooled_sd = math.sqrt(top_line / (control_n + experimental_n - 2))

        d = (control_mean - experimental_mean) / pooled_sd

        d_results.append(d)

    # make a nice dataframe to present the results
    d_table = pd.DataFrame(columns=["Measure", "Cohen's d"])
    d_table["Measure"] = measure_names
    d_table["Cohen's d"] = d_results

    d_table.set_index("Measure", inplace=True)
    d_table.rename_axis(None, inplace=True)

    return d_table


def spearmans_r(measures_table, loud=False):
    """
	Calculates the coefficients (nonparametric Spearman's r) between a collection of behavioural measures.
	The upper-right diagonal of the resulting matrix is discarded (symmetric).
	
	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
	
	Returns:
		Dataframe containing each of the coefficients marked by their p-values (** = p < 0.01, * = p < 0.05).
	"""

    measure_names = list(measures_table.columns)[1:]

    data = []
    for column in measure_names:
        data.append(measures_table[column].values)

    labels = measure_names

    coefs = []
    p_values = []
    for toprow in data:
        for siderow in data:
            coef, p = stats.spearmanr(toprow, siderow)
            coefs.append(coef)
            p_values.append(p)

    coefs = np.array(coefs)
    # reshape as matrix
    coef_as_matrix = coefs.reshape(len(data), len(data))
    # cut off top-diagonal elements
    coef_as_matrix = np.tril(coef_as_matrix, -1)

    p_values = np.array(p_values)
    p_as_matrix = np.array(p_values).reshape(len(data), len(data))
    p_as_matrix = np.tril(p_as_matrix, -1)

    coef_df = pd.DataFrame(coef_as_matrix, columns=labels, index=labels)
    p_df = pd.DataFrame(p_as_matrix, columns=labels, index=labels)

    # now for string manipulation (get the dataframe in a more readable format)
    coef_df.replace(0, "", inplace=True)
    np.fill_diagonal(coef_df.values, "-")

    p_values = p_df.values
    results_size = len(coef_df.columns)
    clean_results = np.empty((results_size, results_size), dtype=object)
    for r, row in enumerate(coef_df.values):
        for e, element in enumerate(row):
            if element == "-":
                clean_results[r, e] = "-"
                continue
            if element == "":
                clean_results[r, e] = ""
                continue

            p = float(p_values[r, e])

            if p < 0.01:
                clean_results[r, e] = str(round(element, 2)) + "**"
            elif p < 0.05:
                clean_results[r, e] = str(round(element, 2)) + "*"
            else:
                clean_results[r, e] = round(element, 2)

    correlation_df = pd.DataFrame(
        clean_results, columns=coef_df.columns, index=coef_df.index
    )

    return correlation_df


def calculate_walker_matrix(measures_tables, labels, measure="frequency", loud=False):
    """
	Performs a two sample Kolmogorov-Smirnov test between collections of measure from different games.

	Args:
		game_measures (List of Dataframes): Measures table for each of the games between which K-S II tests will be performed.
		labels (List of Strings): The name of the games' measures provided, to be used as the column and row names in the output matrix.
		measure (String): The measure (column name) to be used in the calculations.
		loud (Boolean): Whether or not to output status updates as the function progresses, default is False.
		
	Returns:
		Dataframe containing the results of the two sample K-S tests between each of the games for the measure provided.
	"""

    data = []
    for measures_table in measures_tables:
        data.append(measures_table[measure].values)

    coefs = []
    p_values = []
    if loud:
        print("num tests:", len(data) * len(data))
    for toprow in data:
        for siderow in data:
            coef, p = stats.ks_2samp(toprow, siderow)
            coefs.append(coef)
            p_values.append(p)

    coefs = np.array(coefs)
    # reshape as matrixEOS
    coef_as_matrix = coefs.reshape(len(data), len(data))
    # cut off top-diagonal elements
    coef_as_matrix = np.tril(coef_as_matrix, -1)

    p_values = np.array(p_values)
    p_as_matrix = np.array(p_values).reshape(len(data), len(data))
    p_as_matrix = np.tril(p_as_matrix, -1)

    coef_df = pd.DataFrame(coef_as_matrix, columns=labels, index=labels)
    p_df = pd.DataFrame(p_as_matrix, columns=labels, index=labels)

    # now for string manipulation to get the dataframe in a more readable format
    coef_df.replace(0, "", inplace=True)
    np.fill_diagonal(coef_df.values, "-")

    p_values = p_df.values
    clean_results = np.empty((len(coef_df.columns), len(coef_df.columns)), dtype=object)
    for r, row in enumerate(coef_df.values):
        for e, element in enumerate(row):
            if element == "-":
                clean_results[r, e] = "-"
                continue
            if element == "":
                clean_results[r, e] = ""
                continue

            p = float(p_values[r, e])

            if p < 0.01:
                clean_results[r, e] = str(round(element, 2)) + "**"
            elif p < 0.05:
                clean_results[r, e] = str(round(element, 2)) + "*"
            else:
                clean_results[r, e] = round(element, 2)

    clean_df = pd.DataFrame(clean_results, columns=coef_df.columns, index=coef_df.index)
    return clean_df


# the following tests require labelled measures;


def label_overlap_table(measures_table, labels):
    """
	Calculates the number of players under a collection of labels (exclusively), and on each pair of labels (again exclusively) in the list provided.
	This method can be used to reproduce the final table in LaBrie et al's 2007 paper.

	Args:
		measures_table (Dataframe): Collection of behavioural measures for a cohort of players.
		labels (List of Strings): The names of the column representing the group's labels, e.g. ['top_num_bets','top_total_wagered'].
	
	Returns:
		Dataframe containing the number of overlaps, both exclusively and pairwise exclusively.

	"""
    first_diagonal_values = []
    for label in labels:
        other_labels = labels.copy()
        other_labels.remove(label)

        records_with_label = measures_table[measures_table[label] == 1]

        records_with_only_label = records_with_label.copy()
        for other_label in other_labels:
            records_with_only_label = records_with_only_label[
                records_with_only_label[other_label] == 0
            ]

        percentage = len(records_with_only_label) / len(records_with_label) * 100

        table_entry = (
            str(len(records_with_only_label)) + " (" + str(round(percentage)) + ")"
        )
        first_diagonal_values.append(table_entry)

    left_side = np.zeros((len(first_diagonal_values), len(first_diagonal_values)))
    left_side = (pd.DataFrame(left_side)).applymap(str)

    np.fill_diagonal(left_side.values, first_diagonal_values)
    left_side.index = labels
    left_side.replace("0.0", "-", inplace=True)

    only = [label + "_only" for label in labels]
    left_side.columns = only

    # end of left side (exclusive labels)

    # get pairwise combinations of labels (both indexes and label names)
    label_combinations = []
    index_combinations = []
    for index, label in enumerate(labels[:-1]):
        for inner_index, remaining_label in enumerate(labels[index + 1 :]):
            label_combinations.append([label, remaining_label])
            index_combinations.append(
                [
                    labels.index(label),
                    labels.index(label) + labels.index(remaining_label) - 1,
                ]
            )

    # get number of exclusive labels for each pairwise combination
    combination_values = []
    percentage_values = []
    for index, combination in enumerate(label_combinations):
        records_with_first = measures_table[measures_table[combination[0]] == 1]
        records_with_both = measures_table[
            (measures_table[combination[0]] == 1)
            & (measures_table[combination[1]] == 1)
        ]

        records_with_only_both = records_with_both.copy()
        other_labels = labels.copy()
        other_labels.remove(combination[0])
        other_labels.remove(combination[1])
        for other_label in other_labels:
            records_with_only_both = records_with_only_both[
                records_with_only_both[other_label] == 0
            ]

        combination_values.append(len(records_with_only_both))
        percentage_values.append(
            len(records_with_only_both) / len(records_with_first) * 100
        )

    # create and populate a matrix (to be made into a dataframe) to hold the overlap combination results
    combination_matrix = np.zeros((len(label_combinations), len(label_combinations)))
    for index, value in enumerate(combination_values):
        combination_matrix[
            index_combinations[index][0], index_combinations[index][1]
        ] = value

    # make combination matrix a dataframe and rename columns
    combination_df = pd.DataFrame(combination_matrix)
    combination_columns = []
    for label_combination in label_combinations:
        combination_columns.append(" and ".join(label_combination) + " only")

    # get the number of records which have all labels (members of all groups)
    records_meeting_all_labels = measures_table[
        measures_table[labels[0]] == 1
    ]  # get those meeting the first label
    for label in labels[1:]:
        records_meeting_all_labels = records_meeting_all_labels[
            records_meeting_all_labels[label] == 1
        ]

    combination_df = combination_df.applymap(str)
    combination_df.replace("0.0", "-", inplace=True)

    combination_df.columns = combination_columns

    # add percentage values to exclusive columns (right side)
    for index, label_combination in enumerate(index_combinations):
        value = combination_df.iloc[label_combination[0], label_combination[1]]
        try:
            combination_df.iloc[label_combination[0], label_combination[1]] = (
                str(round(float(value)))
                + " ("
                + str(round(percentage_values[index]))
                + ")"
            )
        except:
            continue

    combination_df.index = labels

    combination_df["all labels"] = (
        str(round(len(records_meeting_all_labels)))
        + " ("
        + str(
            round(
                len(records_meeting_all_labels)
                / len(measures_table[measures_table[labels[0]] == 1])
                * 100
            )
        )
        + ")"
    )

    complete_table = pd.concat([left_side, combination_df], axis=1)

    return complete_table


def add_tables(t1, t2, same_columns=False):
    """
	Joins two tables (the second to the right hand side of the first), adding '_2' to column names if same_columns parameter is True.

	Args:
		t1 (Dataframe): The left side of the desired output table.
		t2 (Dataframae): The rigfht side of the desired output table (needs to have the same index as t1).
		same_columns (Boolean): Whether or not the column names of the two tables are the same (do they need renaming?).

	Returns:
		Dataframe containing the two tables stitched together.
	"""
    if same_columns:
        t2.columns = [name + "_2" for name in t2.columns]
    combined = pd.concat([t1, t2.reindex(t1.index)], axis=1)
    return combined





# =========================================================
# Plotting Functions for the Tests Module
# =========================================================

import matplotlib.cm as cm

def color_matrix(matrix, cmap):
    """
    Creates a shaded matrix based on a color map.

    Better docs needed.
    
    """

    results_size = len(correlations.columns)
    values = np.empty((results_size, results_size), dtype=object)
    for r, row in enumerate(correlations.values):
        for e, element in enumerate(row):
            if element == "-":
                values[r, e] = 100
                continue
            if element == "":
                values[r, e] = np.nan
                continue
            if "*" in str(element):
                value = element.replace("*", "")
                values[r, e] = float(value) * 100
            else:
                values[r, e] = element * 100

    current_cmap = cm.get_cmap(cmap)
    current_cmap.set_bad(color="white")
    plt.imshow(np.array(values).astype(np.float), cmap=current_cmap)
    plt.yticks(range(len(correlations.columns)), list(correlations.columns))
    plt.xticks(range(len(correlations.columns)), list(correlations.columns))
    plt.xticks(rotation=90)
    cbar = plt.colorbar()
    cbar.set_ticks([-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100])
    cbar.set_ticklabels([-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1])
    plt.ylabel("test")
    return plt


