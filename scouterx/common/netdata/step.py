from abc import ABC, abstractmethod

METHOD: int = 1
METHOD2: int = 10
SPAN: int = 51
SQL: int = 2
SQL2: int = 8
SQL3: int = 16
MESSAGE: int = 3
SOCKET: int = 5
APICALL: int = 6
APICALL2: int = 15
SPANCALL: int = 52
THREAD_SUBMIT: int = 7
HASHED_MESSAGE: int = 9
PARAMETERIZED_MESSAGE: int = 17
DUMP: int = 12
DISPATCH: int = 13
THREAD_CALL_POSSIBLE: int = 14
METHOD_SUM: int = 11
SQL_SUM: int = 21
MESSAGE_SUM: int = 31
SOCKET_SUM: int = 42
APICALL_SUM: int = 43
CONTROL: int = 99


class Step(ABC):
    @abstractmethod
    def get_order(self) -> int:
        pass

    @abstractmethod
    def get_step_type(self) -> int:
        pass

    @abstractmethod
    def write(self, out) -> None:
        pass

    @abstractmethod
    def read(self, inp) -> 'Step':
        pass

    @abstractmethod
    def set_index(self, index: int) -> None:
        pass

    @abstractmethod
    def set_parent(self, parent: int) -> None:
        pass

    @abstractmethod
    def get_parent(self) -> int:
        pass


class SingleStep(Step):
    def __init__(self, parent: int = 0, index: int = 0, start_time: int = 0):
        self.parent = parent
        self.index = index
        self.start_time = start_time

    def get_order(self) -> int:
        return self.index

    def get_step_type(self) -> int:
        # TODO: SingleStep.GetStepType()
        return 0

    def set_index(self, index: int) -> None:
        self.index = index

    def set_parent(self, parent: int) -> None:
        self.parent = parent

    def get_parent(self) -> int:
        return self.parent

    def write(self, out) -> None:
        try:
            out.write_decimal32(self.parent)
            out.write_decimal32(self.index)
            out.write_decimal32(self.start_time)
            out.write_decimal32(0)
        except Exception as e:
            raise IOError(f"Error writing data: {e}")

    def read(self, inp) -> 'Step':
        # TODO: SingleStep.Read()
        return self
