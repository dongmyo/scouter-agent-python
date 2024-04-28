from abc import ABC, abstractmethod


class Value(ABC):
    @abstractmethod
    def write(self, data_output_x):
        """ Serialize this value using the provided DataOutputX instance. """
        pass

    @abstractmethod
    def read(self, data_input_x):
        """ Deserialize data using the provided DataInputX instance and return a Value object. """
        pass

    @abstractmethod
    def get_value_type(self):
        """ Return a byte that uniquely identifies the type of this Value. """
        pass

    @abstractmethod
    def to_string(self):
        """ Return a string representation of this Value. """
        pass
