from abc import ABC, abstractmethod

class ComponentIterator:
    def __init__(self, children):
        self._children = children
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._children):
            item = self._children[self._index]
            self._index += 1
            return item
        raise StopIteration


class CakeComponent(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    def is_composite(self) -> bool:
        return False


class CakeItem(CakeComponent):
    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name


class CakeCategory(CakeComponent):
    def __init__(self, name: str):
        self.name = name
        self.children = []

    def add(self, component: CakeComponent):
        self.children.append(component)

    def get_name(self) -> str:
        return self.name

    def is_composite(self) -> bool:
        return True

    def __iter__(self):
        return ComponentIterator(self.children)