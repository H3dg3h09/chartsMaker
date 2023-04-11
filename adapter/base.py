from typing import TypeVar

GenericData = TypeVar("GenericData")


class AdapterBase:
    def __init__(self: "AdapterBase", data: GenericData) -> None:
        self.data: GenericData = data

    def to_df(self):
        raise NotImplementedError
