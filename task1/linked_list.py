class Element:
    __slots__ = ('value', 'next')

    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.last = None

    def push(self, value):
        element = Element(value)

        if self.last is not None:
            element.next = self.last

        self.last = element

    def pop(self):
        if self.last is None:
            raise IndexError("pop from empty stack")

        value = self.last.value
        self.last = self.last.next
        return value

    def pop_all(self):
        while self.last is not None:
            yield self.pop()


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
        self.cursor = self.head
        return self

    def __next__(self):
        if self.cursor is None:
            raise StopIteration

        value = self.cursor.value
        self.cursor = self.cursor.next
        return value

    def print(self):
        return ' '.join(map(str, self))

    def __str__(self):
        values = ', '.join(map(str, self))
        return f'<{values}>'

    def __iadd__(self, other):
        for value in other:
            self.append(value)
        return self

    def print_reversed(self):
        stack = Stack()
        for value in self:
            stack.push(value)

        return ' '.join(map(str, stack.pop_all()))
