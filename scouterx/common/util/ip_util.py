def ip_to_bytes(ip):
    """Converts an IPv4 address from string to a byte array."""
    result = bytearray(4)
    parts = ip.split('.')
    if len(parts) != 4:
        return bytearray([0, 0, 0, 0])  # equivalent to emptyIp

    try:
        for i, part in enumerate(parts):
            v = int(part)
            if not 0 <= v <= 255:
                return bytearray([0, 0, 0, 0])
            result[i] = v
    except ValueError:
        return bytearray([0, 0, 0, 0])

    return bytes(result)


if __name__ == '__main__':
    ip_string = "192.168.1.1"
    print(ip_to_bytes(ip_string))
