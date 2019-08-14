class Element:
    __slots__ = ('value', 'next')

    def __init__(self, value):
        self.value = value
        self.next = None


class Iterator:
    def __init__(self, linked_list):
        self.cursor = linked_list.head

    def __iter__(self):
        return self

    def __next__(self):
        if self.cursor is None:
            raise StopIteration

        value = self.cursor.value
        self.cursor = self.cursor.next
        return value


class ReverseIterator(Iterator):
    def __init__(self, linked_list):
        self.cursor = None
        for value in linked_list:
            element = Element(value)
            if self.cursor is not None:
                element.next = self.cursor
            self.cursor = element


class List:
    def __init__(self, *args):
        self.head = None
        self.tail = None

        for value in args:
            self.append(value)

    def append(self, value):
        element = Element(value)

        if self.head is None:
            self.head = element

        if self.tail is not None:
            self.tail.next = element

        self.tail = element

    def __iter__(self):
        return Iterator(self)

    def __reversed__(self):
        return ReverseIterator(self)

    def __iadd__(self, other):
        for value in other:
            self.append(value)
        return self

    def __str__(self):
        values = ', '.join(map(str, self))
        return f'<{values}>'

    def print(self):
        return ' '.join(map(str, self))

    def print_reversed(self):
        return ' '.join(map(str, reversed(self)))
