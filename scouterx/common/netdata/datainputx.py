import io
import socket
import struct
from typing import Any, Optional, Tuple, Union

from scouterx.common.netdata.packcreator import create_pack
from scouterx.common.netdata.valuecreator import create_value


class DataInputX:
    def __init__(self, data: Any):
        if isinstance(data, bytes):
            self.reader = io.BytesIO(data)
        elif isinstance(data, io.IOBase):
            self.reader = data
        elif isinstance(data, socket.socket):
            self.reader = data.makefile('rwb', buffering=0)
        elif hasattr(data, 'read'):
            self.reader = data
        else:
            self.reader = None

        self.offset = 0

    def read_int8(self) -> Tuple[int, Optional[Exception]]:
        try:
            value = struct.unpack('>b', self.reader.read(1))[0]
            self.offset += 1
            return value, None
        except Exception as e:
            return 0, e

    def read_uint8(self) -> Tuple[int, Optional[Exception]]:
        try:
            value = struct.unpack('>B', self.reader.read(1))[0]
            self.offset += 1
            return value, None
        except Exception as e:
            return 0, e

    def read_int16(self) -> Tuple[int, Optional[Exception]]:
        try:
            value = struct.unpack('>h', self.reader.read(2))[0]
            self.offset += 2
            return value, None
        except Exception as e:
            return 0, e

    def read_int32(self) -> Tuple[int, Optional[Exception]]:
        try:
            value = struct.unpack('>i', self.reader.read(4))[0]
            self.offset += 4
            return value, None
        except Exception as e:
            return 0, e

    def read_int64(self) -> Tuple[int, Optional[Exception]]:
        try:
            value = struct.unpack('>q', self.reader.read(8))[0]
            self.offset += 8
            return value, None
        except Exception as e:
            return 0, e

    def read_float32(self) -> Tuple[float, Optional[Exception]]:
        try:
            value = struct.unpack('>f', self.reader.read(4))[0]
            self.offset += 4
            return value, None
        except Exception as e:
            return 0.0, e

    def read_float64(self) -> Tuple[float, Optional[Exception]]:
        try:
            value = struct.unpack('>d', self.reader.read(8))[0]
            self.offset += 8
            return value, None
        except Exception as e:
            return 0.0, e

    def read_decimal(self) -> Tuple[int, Optional[Exception]]:
        length, err = self.read_uint8()
        if err:
            return 0, err

        if length == 0:
            return 0, None
        elif length == 1:
            return self.read_int8()
        elif length == 2:
            return self.read_int16()
        elif length == 4:
            return self.read_int32()
        elif length == 8:
            return self.read_int64()
        else:
            return 0, ValueError(f"Unsupported length for decimal: {length}")

    def read_string(self) -> Tuple[str, Optional[Exception]]:
        try:
            length = self.read_uint8()[0]
            if length == 255:
                length = struct.unpack('>h', self.reader.read(2))[0]
            elif length == 254:
                length = struct.unpack('>i', self.reader.read(4))[0]
            elif length == 0:
                return "", None
            data = self.reader.read(length)
            self.offset += length
            return data.decode('utf-8'), None
        except Exception as e:
            return "", e

    def read_blob(self) -> Tuple[bytes, Optional[Exception]]:
        try:
            length = self.read_uint8()[0]
            if length == 255:
                length = struct.unpack('>h', self.reader.read(2))[0]
            elif length == 254:
                length = struct.unpack('>i', self.reader.read(4))[0]
            elif length == 0:
                return b'', None
            self.offset += length
            return self.reader.read(length), None
        except Exception as e:
            return b'', e

    def read_boolean(self) -> Tuple[bool, Optional[Exception]]:
        try:
            value, err = self.read_int8()
            return (value != 0), err
        except Exception as e:
            return False, e

    def read_value(self):
        try:
            value_type, _ = self.read_int8()
            value = create_value(value_type)
            if value is None:
                raise ValueError(f"Not defined value type: {value_type}")
            return value.read(self)
        except Exception as e:
            return None, e

    def read_int_bytes(self):
        length, err = self.read_int32()
        if err:
            return None, err
        return self.read(length)

    def read(self, length):
        try:
            data = self.reader.read(length)
            if len(data) < length:
                raise ValueError(f"Failed to read {length} bytes from input stream")
            self.offset += length
            return data, None
        except Exception as e:
            return None, e

    def read_pack(self):
        pack_type, err = self.read_int8()
        if err:
            return None, err

        pack = create_pack(pack_type)
        if pack:
            pack.read(self)
            return pack, err
        else:
            return None, ValueError("Invalid pack type")
