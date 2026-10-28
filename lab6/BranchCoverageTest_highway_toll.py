"""
Branch Coverage Test Suite for Highway Toll Application
Lab 6: Code and Branch Coverage Analysis

Student Details:
- Name: Ananthakrishna M A
- SRN: PES1UG24AM036
- GitHub: anantha-bit
- Repository: L6_L7_36_highway_toll

This test suite evaluates all control structures (if/else/for) to evaluate both True and False,
covering all execution pathways, edge cases, and decision branches to achieve 100% branch coverage.
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice, BASE_TOLL, EXEMPT


# ==========================================
# 1. Branch Tests for `toll_for(axles, is_peak, has_fastag)`
# ==========================================

class TestTollForBranchCoverage:
    """Tests covering all branches of the toll_for function."""

    def test_axles_less_than_two_branch_true(self):
        """Branch: if axles < 2 evaluates to TRUE (raises ValueError)."""
        # Test boundary values: 1, 0, and negative
        for invalid_axle in (1, 0, -1, -5):
            with pytest.raises(ValueError, match="invalid axle count"):
                toll_for(invalid_axle, False, False)

    def test_axles_less_than_two_branch_false(self):
        """Branch: if axles < 2 evaluates to FALSE (proceeds to calculate toll)."""
        # 2 is the valid boundary
        assert toll_for(2, False, False) == 100

    def test_axles_in_base_toll_branch_true(self):
        """Branch: if axles in BASE_TOLL evaluates to TRUE (2, 3, 4)."""
        # Test all keys defined in BASE_TOLL
        assert toll_for(2, False, False) == BASE_TOLL[2]  # 100
        assert toll_for(3, False, False) == BASE_TOLL[3]  # 150
        assert toll_for(4, False, False) == BASE_TOLL[4]  # 250

    def test_axles_in_base_toll_branch_false(self):
        """Branch: if axles in BASE_TOLL evaluates to FALSE (axles >= 5, base = 400)."""
        assert toll_for(5, False, False) == 400
        assert toll_for(6, False, False) == 400
        assert toll_for(10, False, False) == 400

    def test_is_peak_branch_true_and_false(self):
        """Branch: if is_peak evaluates to TRUE vs FALSE."""
        # axles = 2, fastag = False
        assert toll_for(2, is_peak=False, has_fastag=False) == 100.0  # 100
        assert toll_for(2, is_peak=True, has_fastag=False) == 125.0   # 100 * 1.25

    def test_has_fastag_branch_false(self):
        """Branch: if has_fastag evaluates to FALSE (no discount)."""
        assert toll_for(2, is_peak=False, has_fastag=False) == 100
        assert toll_for(3, is_peak=False, has_fastag=False) == 150

    def test_has_fastag_branch_true_axles_two(self):
        """Branch: if has_fastag is TRUE AND if axles == 2 is TRUE (10% discount)."""
        # Non-peak: 100 * 0.9 = 90.0
        assert toll_for(2, is_peak=False, has_fastag=True) == 90.0
        # Peak: 100 * 1.25 * 0.9 = 112.5
        assert toll_for(2, is_peak=True, has_fastag=True) == 112.5

    def test_has_fastag_branch_true_axles_not_two(self):
        """Branch: if has_fastag is TRUE AND if axles == 2 is FALSE (5% discount)."""
        # 3 axles: 150 * 0.95 = 142.5
        assert toll_for(3, is_peak=False, has_fastag=True) == 142.5
        # 3 axles peak: round(150 * 1.25 * 0.95, 2) = round(178.125, 2) = 178.12
        assert toll_for(3, is_peak=True, has_fastag=True) == 178.12
        # 4 axles peak: round(250 * 1.25 * 0.95, 2) = round(296.875, 2) = 296.88
        assert toll_for(4, is_peak=True, has_fastag=True) == 296.88
        # 5 axles peak: round(400 * 1.25 * 0.95, 2) = 475.0
        assert toll_for(5, is_peak=True, has_fastag=True) == 475.0


# ==========================================
# 2. Branch Tests for `toll_charge(vehicle, axles, is_peak, has_fastag)`
# ==========================================

class TestTollChargeBranchCoverage:
    """Tests covering all branches of toll_charge."""

    def test_vehicle_in_exempt_branch_true(self):
        """Branch: if vehicle in EXEMPT evaluates to TRUE (returns 0)."""
        # Test all vehicles in EXEMPT tuple ("ambulance", "fire_engine")
        assert toll_charge("ambulance", 2, False, False) == 0
        assert toll_charge("ambulance", 4, True, True) == 0
        assert toll_charge("fire_engine", 3, False, True) == 0
        assert toll_charge("fire_engine", 5, True, False) == 0

    def test_vehicle_in_exempt_branch_false(self):
        """Branch: if vehicle in EXEMPT evaluates to FALSE (charges toll)."""
        assert toll_charge("car", 2, False, False) == 100
        assert toll_charge("bus", 3, True, True) == 178.12
        assert toll_charge("truck", 4, True, True) == 296.88
        assert toll_charge("heavy_vehicle", 5, False, False) == 400


# ==========================================
# 3. Branch Tests for `pass_advice(trips, axles, pass_price)`
# ==========================================

class TestPassAdviceBranchCoverage:
    """Tests covering all branches of pass_advice."""

    def test_pass_advice_buy_pass_branch_true(self):
        """Branch: if cost > pass_price evaluates to TRUE -> 'buy_pass'."""
        # 2 trips of 2-axle base (100 + 100 = 200) vs pass_price 150
        trips = [(False, False), (False, False)]
        assert pass_advice(trips, 2, 150) == "buy_pass"

    def test_pass_advice_either_branch_true(self):
        """Branch: if cost == pass_price evaluates to TRUE -> 'either'."""
        # 1 trip of 2-axle base (100) vs pass_price 100
        trips = [(False, False)]
        assert pass_advice(trips, 2, 100) == "either"

    def test_pass_advice_pay_per_trip_branch_true(self):
        """Branch: cost < pass_price evaluates to TRUE -> 'pay_per_trip'."""
        # 1 trip of 2-axle base (100) vs pass_price 150
        trips = [(False, False)]
        assert pass_advice(trips, 2, 150) == "pay_per_trip"

    def test_pass_advice_empty_trips_loop_zero_iterations(self):
        """Branch edge case: empty trips list (loop does not execute, cost = 0)."""
        assert pass_advice([], 2, 50) == "pay_per_trip"
        assert pass_advice([], 2, 0) == "either"
