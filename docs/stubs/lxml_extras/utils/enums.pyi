from enum import Enum
from lxml_extras.utils.exceptions import InvalidOnErrorValueError as InvalidOnErrorValueError

class OnError(Enum):
    RAISE: int
    IGNORE: int
    @classmethod
    def from_str(cls, value: str) -> OnError: ...
    def to_str(self) -> str: ...
    @classmethod
    def from_any(cls, value: str | OnError) -> OnError: ...
