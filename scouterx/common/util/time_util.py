from datetime import datetime, timedelta

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 60 * SECONDS_PER_MINUTE
SECONDS_PER_DAY = 24 * SECONDS_PER_HOUR


def get_duration(seconds):
    """Convert seconds to a formatted string showing days, hours, minutes, and seconds."""
    day = seconds // SECONDS_PER_DAY
    hour = (seconds - (day * SECONDS_PER_DAY)) // SECONDS_PER_HOUR
    minute = (seconds - (day * SECONDS_PER_DAY) - (hour * SECONDS_PER_HOUR)) // SECONDS_PER_MINUTE
    secs = (seconds - (day * SECONDS_PER_DAY) - (hour * SECONDS_PER_HOUR) - (minute * SECONDS_PER_MINUTE))
    return f"{day}D {hour}H {minute}M {secs}S"


def millis_between(from_time, to_time):
    """Return the difference in milliseconds between two datetime objects."""
    time_delta = to_time - from_time
    return int(time_delta.total_seconds() * 1000)


def millis_to_now(from_time):
    """Return the difference in milliseconds from a given datetime to now."""
    return millis_between(from_time, datetime.now())


def time_to_millis(time_obj):
    """Convert a datetime object to the number of milliseconds since Unix epoch."""
    epoch = datetime.utcfromtimestamp(0)
    time_delta = time_obj - epoch
    return int(time_delta.total_seconds() * 1000)


if __name__ == '__main__':
    now = datetime.now()
    past = now - timedelta(days=1, hours=3, minutes=46)
    print(get_duration((now - past).total_seconds()))  # 1D 3H 46M 0S
    print(millis_between(past, now))  # Expected: ~97360000 milliseconds
    print(millis_to_now(past))  # Milliseconds from past date to now
    print(time_to_millis(now))  # Milliseconds since Unix epoch to now
