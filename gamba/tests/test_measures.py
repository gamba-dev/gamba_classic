import pytest

import pandas as pd
import datetime

import gamba.measures as gb


# create some example data to compute measures on for testing
example_transactions = pd.DataFrame()
example_transactions["player_id"] = ["test_player"] * 4
example_transactions["bet_time"] = [
    datetime.datetime.now() + datetime.timedelta(days=x) for x in range(4)
]
example_transactions["bet_size"] = [2, 2, 3, 4]
example_transactions["payout_size"] = [0, 4, 0, 8]


def test_duration():
    value = gb.duration(example_transactions)
    assert value == 4


def test_frequency():
    value = gb.frequency(example_transactions)
    assert value == 100


def test_number_of_bets():
    value = gb.number_of_bets(example_transactions)
    assert value == 4


def test_average_bets_per_day():
    value = gb.average_bets_per_day(example_transactions)
    assert value == 1


def test_average_bet_size():
    value = gb.average_bet_size(example_transactions)
    assert value == 2.75


def test_total_wagered():
    value = gb.total_wagered(example_transactions)
    assert value == 11


def test_net_loss():
    value = gb.net_loss(example_transactions)
    assert value == -1


def test_percent_loss():
    value = gb.percent_loss(example_transactions)
    # floating point value so the approx method comes in handy
    assert value == pytest.approx(-9.1, 0.1)


# more to do, this is the rough flavour for now...
