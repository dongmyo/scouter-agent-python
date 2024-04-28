def int_to_xlog_string32(num):
    """Converts an integer to a base-32 string with a prefix indicating the sign."""
    minus = num < 0
    if minus:
        return 'z' + to_base32(-num)
    else:
        return 'x' + to_base32(num)


def to_base32(num):
    """Converts an integer to a base-32 encoded string."""
    alphabet = '0123456789abcdefghijklmnopqrstuv'  # Base-32 alphabet
    if num == 0:
        return alphabet[0]
    result = ''
    negative = num < 0
    num = -num if negative else num
    while num:
        result = alphabet[num % 32] + result
        num = num // 32
    return result


if __name__ == '__main__':
    number_positive = 12345
    number_negative = -12345
    print(int_to_xlog_string32(number_positive))
    print(int_to_xlog_string32(number_negative))
