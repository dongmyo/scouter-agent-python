import time
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
    time_delta = to_time - from_time
    return int(time_delta * 1000)


def millis_to_now(from_time):
    return millis_between(from_time, time.time())


if __name__ == '__main__':
    now_dt = datetime.now()
    past_dt = now_dt - timedelta(days=1, hours=3, minutes=46)

    now = now_dt.timestamp()
    past = past_dt.timestamp()

    print(f"past={past}, now={now}")

    print(get_duration((now - past)))
    print(millis_between(past, now))
    print(millis_to_now(past))
