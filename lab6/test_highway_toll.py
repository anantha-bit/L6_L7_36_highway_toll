"""
Highway Toll Test Suite
Lab 6: Code and Branch Coverage Analysis

Student Details:
- Name: Ananthakrishna M A
- SRN: PES1UG24AM036
- GitHub: anantha-bit
- Repository: L6_L7_36_highway_toll
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice, BASE_TOLL, EXEMPT


# ==========================================
# 1. Starter Test Cases
# ==========================================

def test_ambulance_is_exempt():
    """Verify that exempt vehicle 'ambulance' incurs zero toll charge."""
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    """Verify standard base toll for a 2-axle vehicle without peak or fastag."""
    assert toll_for(2, False, False) == 100


# ==========================================
# 2. Comprehensive Code & Branch Coverage Tests
# ==========================================

def test_invalid_axle_count_less_than_two():
    """Test boundary values for axles < 2 raising ValueError."""
    for invalid_axle in (1, 0, -1, -5):
        with pytest.raises(ValueError, match="invalid axle count"):
            toll_for(invalid_axle, False, False)


def test_valid_axle_two_boundary():
    """Test lower boundary of valid axles (axles == 2)."""
    assert toll_for(2, False, False) == 100


def test_all_base_toll_axle_keys():
    """Test all valid axle keys in BASE_TOLL (2: 100, 3: 150, 4: 250)."""
    assert toll_for(2, False, False) == BASE_TOLL[2]
    assert toll_for(3, False, False) == BASE_TOLL[3]
    assert toll_for(4, False, False) == BASE_TOLL[4]


def test_axles_greater_than_four_default_base():
    """Test axles not in BASE_TOLL (axles >= 5 defaults to 400)."""
    assert toll_for(5, False, False) == 400
    assert toll_for(6, False, False) == 400
    assert toll_for(10, False, False) == 400


def test_peak_hour_surcharges():
    """Test peak surcharge (1.25x) vs non-peak."""
    # 2 axles non-peak vs peak
    assert toll_for(2, is_peak=False, has_fastag=False) == 100.0
    assert toll_for(2, is_peak=True, has_fastag=False) == 125.0


def test_fastag_discounts():
    """Test fastag discounts: 10% for axles==2, 5% for axles!=2."""
    # axles == 2: 10% discount
    assert toll_for(2, is_peak=False, has_fastag=True) == 90.0
    assert toll_for(2, is_peak=True, has_fastag=True) == 112.5

    # axles == 3: 5% discount
    assert toll_for(3, is_peak=False, has_fastag=True) == 142.5
    assert toll_for(3, is_peak=True, has_fastag=True) == 178.12

    # axles == 4: 5% discount
    assert toll_for(4, is_peak=True, has_fastag=True) == 296.88

    # axles == 5: 5% discount on base 400
    assert toll_for(5, is_peak=True, has_fastag=True) == 475.0


def test_toll_charge_all_exempt_vehicles():
    """Test that all vehicles in EXEMPT tuple incur zero toll."""
    assert toll_charge("ambulance", 2, False, False) == 0
    assert toll_charge("ambulance", 4, True, True) == 0
    assert toll_charge("fire_engine", 3, False, True) == 0
    assert toll_charge("fire_engine", 5, True, False) == 0


def test_toll_charge_non_exempt_vehicles():
    """Test toll charges for non-exempt vehicles."""
    assert toll_charge("car", 2, False, False) == 100
    assert toll_charge("bus", 3, True, True) == 178.12
    assert toll_charge("truck", 4, True, True) == 296.88
    assert toll_charge("heavy_truck", 5, False, False) == 400


def test_pass_advice_all_branches():
    """Test all branches of monthly pass advice."""
    # Branch 1: cost > pass_price -> 'buy_pass'
    trips_buy = [(False, False), (False, False)]  # 100 + 100 = 200
    assert pass_advice(trips_buy, 2, 150) == "buy_pass"

    # Branch 2: cost == pass_price -> 'either'
    trips_either = [(False, False)]  # 100 == 100
    assert pass_advice(trips_either, 2, 100) == "either"

    # Branch 3: cost < pass_price -> 'pay_per_trip'
    trips_pay = [(False, False)]  # 100 < 150
    assert pass_advice(trips_pay, 2, 150) == "pay_per_trip"

    # Branch 4: empty trips edge case
    assert pass_advice([], 2, 50) == "pay_per_trip"
    assert pass_advice([], 2, 0) == "either"
