from abc import ABC, abstractmethod


class Pack(ABC):
    @abstractmethod
    def write(self, out) -> None:
        """Serialize the pack to the provided DataOutputX instance."""
        pass

    @abstractmethod
    def read(self, inp) -> 'Pack':
        """Deserialize data from the DataInputX instance and return a Pack instance."""
        pass

    @abstractmethod
    def to_string(self) -> str:
        """Return a string representation of the pack."""
        pass

    @abstractmethod
    def get_pack_type(self) -> int:
        """Return the type of the pack as a byte (int in Python)."""
        pass
