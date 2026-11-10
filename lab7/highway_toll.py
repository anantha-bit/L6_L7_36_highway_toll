MAX_PLATE_LENGTH = 32
MAX_TRIP_TEXT_LENGTH = 64


def _parse_ascii_uint(value, max_digits):
    """Parse a bounded non-negative ASCII digit string, rejecting signs, underscores, and Unicode digits."""
    if not isinstance(value, str):
        return None
    if not value or len(value) > max_digits:
        return None
    if not (value.isascii() and value.isdigit()):
        return None
    return int(value)


def parse_plate(plate):
    """Parse a vehicle plate 'STATE-DISTRICT-SERIES-NUMBER' into (STATE, district, number), or None if invalid."""
    if not isinstance(plate, str):
        return None
    cleaned = plate.strip()
    if not cleaned or len(cleaned) > MAX_PLATE_LENGTH:
        return None

    parts = cleaned.split("-")
    if len(parts) != 4:
        return None

    state, district_str, series, number_str = parts
    if not (state.isascii() and state.isalpha() and 2 <= len(state) <= 3):
        return None
    if not (series.isascii() and series.isalpha() and 1 <= len(series) <= 3):
        return None

    district = _parse_ascii_uint(district_str, max_digits=3)
    number = _parse_ascii_uint(number_str, max_digits=6)
    if district is None or number is None:
        return None

    return state.upper(), district, number


def trip_cost(text):
    """Calculate non-negative trip cost from '<count>x<rate>', returning None on invalid input."""
    if not isinstance(text, str):
        return None
    cleaned = text.strip()
    if not cleaned or len(cleaned) > MAX_TRIP_TEXT_LENGTH:
        return None

    parts = cleaned.lower().split("x")
    if len(parts) != 2:
        return None

    count = _parse_ascii_uint(parts[0].strip(), max_digits=12)
    rate = _parse_ascii_uint(parts[1].strip(), max_digits=12)
    if count is None or rate is None:
        return None

    return count * rate


def axle_class(axles):
    """Classify a vehicle by axle count (>= 2) as 'car', 'truck', or 'heavy', or None if invalid."""
    if isinstance(axles, bool):
        return None
    if isinstance(axles, int):
        n = axles
    elif isinstance(axles, str):
        n = _parse_ascii_uint(axles.strip(), max_digits=6)
        if n is None:
            return None
    else:
        return None

    if n < 2:
        return None
    if n == 2:
        return "car"
    if n <= 4:
        return "truck"
    return "heavy"


def _safe_input(prompt):
    """Read a line from stdin, returning None on EOF or user interrupt."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main():
    """Run interactive demonstrations for plate parsing, trip costing, and axle classification."""
    print("==== Running parse_plate ====")
    user_input = _safe_input("Enter a plate (e.g. KA-05-AB-1234): ")
    result = parse_plate(user_input)
    if result is None:
        print("Invalid vehicle plate. Expected format: STATE-DISTRICT-SERIES-NUMBER (e.g. KA-05-AB-1234)")
    else:
        print("State, District and Number:", result)

    print("\n==== Running trip_cost ====")
    user_input = _safe_input("Enter trips x rate (e.g. 3x150): ")
    result = trip_cost(user_input)
    if result is None:
        print("Invalid trip cost input. Expected non-negative integers like 3x150")
    else:
        print("Trip Cost:", result)

    print("\n==== Running axle_class ====")
    user_input = _safe_input("Enter an axle count (e.g. 3): ")
    result = axle_class(user_input)
    if result is None:
        print("Invalid axle count. Expected an integer >= 2 (e.g. 3)")
    else:
        print("Vehicle Class:", result)


if __name__ == "__main__":
    main()
