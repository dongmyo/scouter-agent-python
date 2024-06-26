import io
import socket
import struct

import numpy

from scouterx.common.netdata.nilvalue import NilValue
from scouterx.common.netdata.pack import Pack
from scouterx.common.netdata.step import Step


class DataOutputX:
    """A DataOutputX is a output stream which used write various kinds of data."""

    def __init__(self, writer=None):
        self.written = 0
        if writer is None:
            self.writer = io.BytesIO()
        elif isinstance(writer, io.IOBase):
            self.writer = writer
        elif isinstance(writer, socket.socket):
            self.writer = writer.makefile('rwb', buffering=0)
        elif hasattr(writer, 'write'):
            self.writer = writer
        else:
            self.writer = io.BytesIO()

    def write_int32_array(self, values):
        if values is None:
            self.write_int16(0)
        else:
            self.write_int16(numpy.int16(len(values)))
            for value in values:
                self.write_int32(value)

    def write_int32(self, value):
        self.writer.write(struct.pack('>i', value))
        self.written += 4

    def write_int16(self, value):
        self.writer.write(struct.pack('>h', value))
        self.written += 2

    def write_int64(self, value):
        self.writer.write(struct.pack('>q', value))
        self.written += 8

    def write_uint64(self, value):
        self.writer.write(struct.pack('>Q', value))
        self.written += 8

    def write_int8(self, value):
        self.writer.write(struct.pack('>b', value))
        self.written += 1

    def write_uint8(self, value):
        self.writer.write(struct.pack('>B', value))
        self.written += 1

    def write_float32(self, value):
        self.writer.write(struct.pack('>f', value))
        self.written += 4

    def write_float64(self, value):
        self.writer.write(struct.pack('>d', value))
        self.written += 8

    def write_decimal(self, value):
        if value == 0:
            self.write_int8(0)
        elif -128 <= value <= 127:
            self.write_int8(1)
            self.write_int8(numpy.int8(value))
        elif -32768 <= value <= 32767:
            self.write_int8(2)
            self.write_int16(numpy.int16(value))
        elif -2147483648 <= value <= 2147483647:
            self.write_int8(4)
            self.write_int32(numpy.int32(value))
        else:
            self.write_int8(8)
            self.write_int64(value)

    def write_decimal32(self, value):
        if value == 0:
            self.write_int8(0)
        elif -128 <= value <= 127:
            self.write_int8(1)
            self.write_int8(numpy.int8(value))
        elif -32768 <= value <= 32767:
            self.write_int8(2)
            self.write_int16(numpy.int16(value))
        elif -2147483648 <= value <= 2147483647:
            self.write_int8(4)
            self.write_int32(numpy.int32(value))

    def write_string(self, value):
        if len(value) == 0:
            self.write_int8(0)
        elif len(value) > 100000:
            self.write_blob(b"huge string omitted...")
        else:
            self.write_blob(value.encode('utf-8'))

    def write_int_bytes(self, value):
        """Write a byte array preceded by its length as an int32."""
        self.write_int32(numpy.int32(len(value)))  # write length of the array
        self.writer.write(value)  # write the actual byte array
        self.written += len(value)  # update the count of written bytes

    def write_blob(self, value):
        length = len(value)
        if length == 0:
            self.write_uint8(0)
        elif length <= 253:
            self.write_uint8(length)
            self.writer.write(value)
            self.written += length
        elif length <= 65535:
            self.write_uint8(255)
            self.write_int16(numpy.int16(length))
            self.writer.write(value)
            self.written += length
        else:
            self.write_uint8(254)
            self.write_int32(numpy.int32(length))
            self.writer.write(value)
            self.written += length

    def write(self, value):
        """Write raw bytes to the buffer and update the written count."""
        self.writer.write(value)
        self.written += len(value)

    def write_boolean(self, value):
        if value:
            self.write_int8(1)
        else:
            self.write_int8(0)

    def write_value(self, value):
        if value is None:
            value = NilValue()
        self.write_uint8(numpy.uint8(value.get_value_type()))
        value.write(self)

    def write_pack(self, pack: Pack):
        """Writes the type and content of the pack to the output buffer."""
        try:
            self.write_uint8(numpy.uint8(pack.get_pack_type()))  # Serialize the pack type
            pack.write(self)  # Serialize the pack content
        except Exception as e:
            raise IOError(f"Error writing pack: {e}")

    def write_step(self, step: Step):
        try:
            self.write_uint8(numpy.uint8(step.get_step_type()))
            step.write(self)
        except Exception as e:
            raise IOError(f"Error writing step: {e}")

    def get_bytes(self):
        return self.writer.getvalue()

    def size(self):
        return self.written

    def get_write_size(self):
        return self.written


if __name__ == '__main__':
    output = DataOutputX()
    output.write_int32(123456)
    output.write_string("Hello World")
    output.write_float64(3.141592653589793)
    output.write_boolean(True)
    print(output.get_bytes())
    print(output.size())
