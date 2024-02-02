from typing import Any


class ListOpr:
    @staticmethod
    def element_same_all(lst: list[Any]) -> bool:
        return all(element == lst[0] for element in lst)
