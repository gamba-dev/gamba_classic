import pytest

import pandas as pd
import datetime

import gamba.measures as gb


# create some example data to compute measures on for testing
player_bets = pd.DataFrame()
player_bets["player_id"] = ["test_player"] * 4
player_bets["bet_time"] = [
    datetime.datetime.now() + datetime.timedelta(days=x) for x in range(4)
]
player_bets["bet_size"] = [2, 2, 3, 4]
player_bets["payout_size"] = [0, 4, 0, 8]


def test_duration():
    value = gb.duration(player_bets)
    assert value == 4


def test_frequency():
    value = gb.frequency(player_bets)
    assert value == 100


def test_number_of_bets():
    value = gb.number_of_bets(player_bets)
    assert value == 4


def test_average_bets_per_day():
    value = gb.average_bets_per_day(player_bets)
    assert value == 1


def test_average_bet_size():
    value = gb.average_bet_size(player_bets)
    assert value == 2.75


def test_total_wagered():
    value = gb.total_wagered(player_bets)
    assert value == 11


def test_net_loss():
    value = gb.net_loss(player_bets)
    assert value == -1


def test_percent_loss():
    value = gb.percent_loss(player_bets)
    # floating point value so the approx method comes in handy
    assert value == pytest.approx(-9.1, 0.1)


# ==========================================

# test measures for daily aggregate data

# ==========================================

player_bets_daily = player_bets.copy()
player_bets_daily["bet_count"] = [1, 4, 2, 4]


def test_number_of_bets_daily():
    value = gb.number_of_bets_daily(player_bets_daily)
    assert value == 11


def test_average_bets_per_day_daily():
    value = gb.average_bets_per_day_daily(player_bets_daily)
    assert value == 2.75


def test_average_bet_size_daily():
    value = gb.average_bet_size_daily(player_bets_daily)
    assert value == 1


def test_intensity_daily():
    value = gb.intensity_daily(player_bets_daily)
    assert value == 2.75


def test_frequency_daily():
    value = gb.frequency_daily(player_bets_daily)
    assert value == 4


def test_variability_daily():
    value = gb.variability_daily(player_bets_daily)
    assert value == pytest.approx(1, 0.1)


def test_trajectory_daily():
    value = gb.trajectory_daily(player_bets_daily)
    assert value == pytest.approx(0.7, 0.01)






