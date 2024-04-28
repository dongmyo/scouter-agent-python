from scouterx.common.constants.valueconstant.valueconstants import *
from scouterx.common.netdata.blobvalue import BlobValue
from scouterx.common.netdata.booleanvalue import BooleanValue
from scouterx.common.netdata.decimalvalue import DecimalValue
from scouterx.common.netdata.doublevalue import DoubleValue
from scouterx.common.netdata.floatvalue import Float32Value
from scouterx.common.netdata.listvalue import ListValue
from scouterx.common.netdata.mapvalue import MapValue
from scouterx.common.netdata.nilvalue import NilValue
from scouterx.common.netdata.texthashvalue import TextHashValue
from scouterx.common.netdata.textvalue import TextValue


def create_value(value_type):
    if value_type == NULL:
        return NilValue.new_nil_value()
    elif value_type == BOOLEAN:
        return BooleanValue.new_boolean_empty_value()
    elif value_type == DECIMAL:
        return DecimalValue.new_decimal_empty_value()
    elif value_type == FLOAT:
        return Float32Value.new_float_empty_value()
    elif value_type == DOUBLE:
        return DoubleValue.new_double_empty_value()
    elif value_type == TEXT:
        return TextValue.new_text_empty_value()
    elif value_type == TEXT_HASH:
        return TextHashValue.new_text_hash_empty_value()
    elif value_type == BLOB:
        return BlobValue.new_blob_empty_value()
    elif value_type == IP4ADDR:
        return BlobValue.new_blob_empty_value()  # Assuming this is intentional, as in your Go code
    elif value_type == LIST:
        return ListValue.new_list_value()
    elif value_type == MAP:
        return MapValue.new_map_value()
    else:
        return None
