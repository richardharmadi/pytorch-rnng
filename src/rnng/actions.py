import abc

from rnng.typing import NTLabel, Word


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def from_string(cls, line: str):
        pass

    @abc.abstractmethod
    def __eq__(self, other) -> bool:
        pass

    @abc.abstractmethod
    def __hash__(self) -> int:
        pass

    def __repr__(self) -> str:
        return str(self)


class ShiftAction(Action):
    def __str__(self) -> str:
        return 'SHIFT'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(str(self))

    @classmethod
    def from_string(cls, line: str) -> 'ShiftAction':
        if line != 'SHIFT':
            raise ValueError('invalid string value for SHIFT action')
        else:
            return cls()


class ReduceAction(Action):
    def __str__(self) -> str:
        return 'REDUCE'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(str(self))

    @classmethod
    def from_string(cls, line: str) -> 'ReduceAction':
        if line != 'REDUCE':
            raise ValueError('invalid string value for REDUCE action')
        else:
            return cls()


class NTAction(Action):
    def __init__(self, label: NTLabel) -> None:
        self.label = label

    def __str__(self) -> str:
        return f'NT({self.label})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.label == other.label  # type: ignore

    def __hash__(self) -> int:
        return hash(str(self))

    @classmethod
    def from_string(cls, line: str) -> 'NTAction':
        if not line.startswith('NT(') or not line.endswith(')'):
            raise ValueError('invalid string value for NT(X) action')
        else:
            start = line.find('(') + 1
            return cls(line[start:-1])


class GenAction(Action):
    def __init__(self, word: Word) -> None:
        self.word = word

    def __str__(self) -> str:
        return f'GEN({self.word})'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.word == other.word  # type: ignore

    def __hash__(self) -> int:
        return hash(str(self))

    @classmethod
    def from_string(cls, line: str) -> 'GenAction':
        if not line.startswith('GEN(') or not line.endswith(')'):
            raise ValueError('invalid string value for GEN(w) action')
        else:
            start = line.find('(') + 1
            return cls(line[start:-1])
