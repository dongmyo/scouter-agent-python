import socket

from scouterx.common.constants.valueconstant.valueconstants import IP4ADDR


class Ip4Value:
    def __init__(self, value=None):
        if value is None:
            self.value = bytearray(4)
        else:
            self.value = value

    @classmethod
    def new_ip4_value(cls, ip):
        return cls(socket.inet_aton(ip))

    @classmethod
    def new_ip4_empty_value(cls):
        return cls()

    def read(self, data_input_x):
        try:
            self.value = data_input_x.read(4)
            return self, None
        except Exception as e:
            return None, e

    def write(self, out):
        out.write(self.value)

    @classmethod
    def get_value_type(cls):
        return IP4ADDR

    def __str__(self):
        return f"ip[{self.value.decode()}]"
