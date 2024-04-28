from scouterx.common.constants.valueconstant.valueconstants import BLOB


class BlobValue:
    def __init__(self, value=None):
        if value is None:
            self.value = bytearray()
        else:
            self.value = bytearray(value)

    @staticmethod
    def new_blob_value(value):
        """Factory method to create a new BlobValue with the provided bytes."""
        return BlobValue(value)

    @staticmethod
    def new_blob_empty_value():
        """Factory method to create a new BlobValue with no initial bytes."""
        return BlobValue()

    def read(self, inp):
        """Reads a blob from the given DataInputX object."""
        try:
            self.value = inp.read_blob()
        except Exception as e:
            raise IOError(f"Error reading blob: {e}")
        return self

    def write(self, out):
        """Writes the blob to the given DataOutputX object."""
        try:
            out.write_blob(self.value)
        except Exception as e:
            raise IOError(f"Error writing blob: {e}")

    @classmethod
    def get_value_type(cls):
        """Returns the value type, typically the constant for a blob type."""
        return BLOB

    def __str__(self):
        """Returns a string representation of the blob, showing its length."""
        return f"byte[{len(self.value)}]"
