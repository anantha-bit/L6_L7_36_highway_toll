from hypothesis import given, settings, strategies as st
from highway_toll import parse_plate, trip_cost, axle_class

UNEXPECTED_TYPES = (
    st.integers()
    | st.floats(allow_nan=True, allow_infinity=True)
    | st.booleans()
    | st.lists(st.integers())
    | st.dictionaries(st.text(), st.integers())
)


# ---------------------------------------------------------------------------
# 1. Core Hypothesis Crash-Resistance Fuzz Tests (from starter template)
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
@settings(max_examples=200)
def test_parse_plate_no_crash(s):
    """Fuzz parse_plate with arbitrary Unicode text and None."""
    try:
        result = parse_plate(s)
    except Exception as e:
        assert False, f"parse_plate crashed with: {e}"
    if result is not None:
        assert isinstance(result, tuple) and len(result) == 3
        state, district, number = result
        assert isinstance(state, str) and state.isascii() and state.isalpha() and state.isupper()
        assert isinstance(district, int) and not isinstance(district, bool) and district >= 0
        assert isinstance(number, int) and not isinstance(number, bool) and number >= 0


@given(st.text() | st.none())
@settings(max_examples=200)
def test_trip_cost_no_crash(s):
    """Fuzz trip_cost with arbitrary Unicode text and None."""
    try:
        result = trip_cost(s)
    except Exception as e:
        assert False, f"trip_cost crashed with: {e}"
    if result is not None:
        assert isinstance(result, int) and not isinstance(result, bool) and result >= 0


@given(st.text() | st.none())
@settings(max_examples=200)
def test_axle_class_no_crash(s):
    """Fuzz axle_class with arbitrary Unicode text and None."""
    try:
        result = axle_class(s)
    except Exception as e:
        assert False, f"axle_class crashed with: {e}"
    assert result in (None, "car", "truck", "heavy")


# ---------------------------------------------------------------------------
# 2. Unexpected Type Fuzzing (integers, floats, booleans, lists, dicts)
# ---------------------------------------------------------------------------

@given(UNEXPECTED_TYPES)
def test_parse_plate_unexpected_types_no_crash(val):
    """Non-string inputs to parse_plate must return None without crashing."""
    try:
        result = parse_plate(val)
    except Exception as e:
        assert False, f"parse_plate crashed on {type(val).__name__}: {e}"
    assert result is None


@given(UNEXPECTED_TYPES)
def test_trip_cost_unexpected_types_no_crash(val):
    """Non-string inputs to trip_cost must return None without crashing."""
    try:
        result = trip_cost(val)
    except Exception as e:
        assert False, f"trip_cost crashed on {type(val).__name__}: {e}"
    assert result is None


@given(UNEXPECTED_TYPES)
def test_axle_class_unexpected_types_no_crash(val):
    """Unexpected types to axle_class must not crash; only valid ints >= 2 classify."""
    try:
        result = axle_class(val)
    except Exception as e:
        assert False, f"axle_class crashed on {type(val).__name__}: {e}"
    if isinstance(val, int) and not isinstance(val, bool) and val >= 2:
        assert result in ("car", "truck", "heavy")
    else:
        assert result is None


# ---------------------------------------------------------------------------
# 3. Domain Property & Edge-Case Fuzz Tests
# ---------------------------------------------------------------------------

@given(
    state=st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    district=st.integers(min_value=1, max_value=99),
    series=st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=3),
    number=st.integers(min_value=1, max_value=9999),
)
def test_parse_plate_valid_roundtrip(state, district, series, number):
    """Valid plates normalize state to uppercase and parse district/number as ints."""
    plate = f"{state}-{district:02d}-{series}-{number:04d}"
    assert parse_plate(plate) == (state.upper(), district, number)


@given(st.lists(st.text(alphabet="abcdef0123456789 ", min_size=0, max_size=5), min_size=0, max_size=6))
def test_parse_plate_malformed_segments(parts):
    """Malformed hyphen-delimited plates must not crash or return empty/invalid fields."""
    if len(parts) == 4:
        # Ensure at least one segment violates valid plate constraints
        parts = ["", parts[1], parts[2], parts[3]]
    plate = "-".join(parts)
    try:
        result = parse_plate(plate)
    except Exception as e:
        assert False, f"parse_plate crashed on malformed plate {plate!r}: {e}"
    assert result is None


@given(
    count=st.integers(min_value=0, max_value=10000),
    rate=st.integers(min_value=0, max_value=10000),
    sep=st.sampled_from(["x", "X"]),
)
def test_trip_cost_valid_multiplication(count, rate, sep):
    """Valid non-negative trips and rates compute count * rate regardless of x/X case."""
    assert trip_cost(f"{count}{sep}{rate}") == count * rate


@given(
    count=st.integers(min_value=1, max_value=1000),
    rate=st.integers(min_value=1, max_value=1000),
)
def test_trip_cost_rejects_negative_values(count, rate):
    """Negative trip counts or rates must be rejected as None, never negative/flipped totals."""
    assert trip_cost(f"-{count}x{rate}") is None
    assert trip_cost(f"{count}x-{rate}") is None
    assert trip_cost(f"-{count}x-{rate}") is None


@given(n=st.integers(min_value=2, max_value=100))
def test_axle_class_valid_classification(n):
    """Valid axle counts >= 2 map to car (2), truck (3-4), or heavy (>4)."""
    expected = "car" if n == 2 else ("truck" if n <= 4 else "heavy")
    assert axle_class(str(n)) == expected
    assert axle_class(n) == expected


@given(n=st.integers(min_value=-1000, max_value=1))
def test_axle_class_rejects_below_two(n):
    """Axle counts below 2 (negative, 0, or 1) are invalid and must return None."""
    assert axle_class(str(n)) is None
    assert axle_class(n) is None


def test_security_and_unicode_edge_cases():
    """Verify protection against 4300-digit int DoS, Unicode digits, underscores, and bools."""
    huge_digits = "9" * 5000
    assert parse_plate(f"KA-05-AB-{huge_digits}") is None
    assert trip_cost(f"{huge_digits}x10") is None
    assert axle_class(huge_digits) is None

    # Unicode digits and Python underscore numeric literals must be rejected
    assert parse_plate("KA-\u0660\u0665-AB-\u0661\u0662\u0663\u0664") is None
    assert parse_plate("KA-0_5-AB-1_2") is None
    assert trip_cost("\u0663x\u0661\u0665\u0660") is None
    assert trip_cost("1_0x2_0") is None
    assert axle_class("\u0662") is None
    assert axle_class("2_0") is None

    # Booleans are ints in Python (True == 1, False == 0) and must be rejected
    assert axle_class(True) is None
    assert axle_class(False) is None
