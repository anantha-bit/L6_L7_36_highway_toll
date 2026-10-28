"""
Code Coverage Test Suite for Highway Toll Application
Lab 6: Code and Branch Coverage Analysis

Student Details:
- Name: Ananthakrishna M A
- SRN: PES1UG24AM036
- GitHub: anantha-bit
- Repository: L6_L7_36_highway_toll
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ==========================================
# 1. Initial Starter Test Cases
# ==========================================

def test_ambulance_is_exempt():
    """Verify that exempt vehicle 'ambulance' incurs zero toll charge."""
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    """Verify standard base toll for a 2-axle vehicle without peak or fastag."""
    assert toll_for(2, False, False) == 100


# ==========================================
# 2. Targeted Tests to Achieve 100% Code Coverage
# ==========================================

def test_invalid_axle_count_raises_value_error():
    """Test line 6-7: axles < 2 raises ValueError('invalid axle count')."""
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_axles_not_in_base_toll():
    """Test line 10-11: axles > 4 defaults to base = 400."""
    assert toll_for(5, False, False) == 400


def test_peak_hour_surcharge():
    """Test line 12-13: is_peak adds 25% surcharge."""
    # 2 axles base 100 * 1.25 = 125.0
    assert toll_for(2, True, False) == 125.0


def test_fastag_discount_two_axles():
    """Test line 14-16: has_fastag with 2 axles gets 10% discount."""
    # 2 axles base 100 * 0.9 = 90.0
    assert toll_for(2, False, True) == 90.0


def test_fastag_discount_multi_axles():
    """Test line 17-18: has_fastag with axles != 2 gets 5% discount."""
    # 3 axles base 150 * 0.95 = 142.5
    assert toll_for(3, False, True) == 142.5


def test_toll_charge_non_exempt_vehicle():
    """Test line 25: non-exempt vehicle calculates toll via toll_for."""
    assert toll_charge("car", 2, False, False) == 100


def test_pass_advice_buy_pass():
    """Test line 32-33: when total trip cost > pass_price, advise 'buy_pass'."""
    trips = [(False, False), (False, False)]  # 100 + 100 = 200
    assert pass_advice(trips, 2, 150) == "buy_pass"


def test_pass_advice_either():
    """Test line 34-35: when total trip cost == pass_price, advise 'either'."""
    trips = [(False, False)]  # 100 == 100
    assert pass_advice(trips, 2, 100) == "either"


def test_pass_advice_pay_per_trip():
    """Test line 36: when total trip cost < pass_price, advise 'pay_per_trip'."""
    trips = [(False, False)]  # 100 < 150
    assert pass_advice(trips, 2, 150) == "pay_per_trip"
