
# welcome to the init file, this code makes the methods found in each of the gamba modules avaliable through the top level 'import gamba as gb' statement.
# e.g. this make gb.ks_test() work instead of having to use gb.tests.ks_test()

# when adding features to modules, remember to update this file to allow
# them to be accessed - also remember to check for name conflicts!


__version__ = "0.1b"


from gamba.data import (
    prepare_labrie_data,
    prepare_braverman_data,
    split_individual_transactions,
    load_directory,
    read_csv,
    concat,
    summarise_app
)

from gamba.measures import (
    duration,
    frequency,
    number_of_bets,
    average_bets_per_day,
    average_bet_size,
    total_wagered,
    net_loss,
    percent_loss,

    number_of_bets_daily,
    average_bets_per_day_daily,
    average_bet_size_daily,

    intensity_daily,
    frequency_daily,
    variability_daily,

    check_measure_data,
    standardise_measures_table
)

from gamba.labels import (
    top_split,
    get_labelled_groups
)

from gamba.tests import (
    descriptive_table,
    ks_test,
    cohens_d,
    spearmans_r,
    label_overlap_table,
    calculate_walker_matrix,
    add_tables
)

from gamba.clustering import (
    k_means,
    k_means_range,
    k_means_ensemble,
    agglomerative_cluster,

    describe_clusters
)

from gamba.plots import (
    plot_measure_hist,
    plot_measure_centile,
    plot_measure_pair_plot,

    plot_player_career,
    plot_player_career_split,
    plot_player_radar,
    
    plot_agglomeration_dendrogram,
    plot_cluster_sizes
)

from gamba.studies import (
    calculate_labrie_measures,
    calculate_braverman_measures
)


print('thank you for using gamba!')
