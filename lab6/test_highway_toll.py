"""
Highway Toll Test Suite
Lab 6: Code and Branch Coverage Analysis

Student Details:
- Name: Ananthakrishna M A
- SRN: PES1UG24AM036
- GitHub: anantha-bit
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ==========================================
# Example Starter Test Cases
# ==========================================

def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# ==========================================
# Code Coverage Test Cases (>90% Line Coverage)
# ==========================================

def test_invalid_axle_count_raises_value_error():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_axles_not_in_base_toll():
    assert toll_for(5, False, False) == 400


def test_peak_hour_surcharge():
    assert toll_for(2, True, False) == 125.0


def test_fastag_discount_two_axles():
    assert toll_for(2, False, True) == 90.0


def test_fastag_discount_multi_axles():
    assert toll_for(3, False, True) == 142.5


def test_toll_charge_non_exempt_vehicle():
    assert toll_charge("car", 2, False, False) == 100


def test_pass_advice_buy_pass():
    trips = [(False, False), (False, False)]
    assert pass_advice(trips, 2, 150) == "buy_pass"


def test_pass_advice_either():
    trips = [(False, False)]
    assert pass_advice(trips, 2, 100) == "either"


def test_pass_advice_pay_per_trip():
    trips = [(False, False)]
    assert pass_advice(trips, 2, 150) == "pay_per_trip"
