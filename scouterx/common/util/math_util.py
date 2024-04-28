import math


def round_up(input, places):
    """Rounds up a float to a given number of decimal places."""
    pow = 10 ** places
    digit = pow * input
    rounded = math.ceil(digit)
    new_val = rounded / pow
    return new_val


if __name__ == '__main__':
    value = 3.14159
    rounded_value = round_up(value, 2)
    print("Rounded up value:", rounded_value)
