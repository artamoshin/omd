from unittest import TestCase

from .linked_list import List


class TestList(TestCase):
    def test_samples(self):
        list_ = List(1, 2, 3)
        self.assertEqual(list_.print(), '1 2 3')

        list_.append(4)
        self.assertEqual(list_.print(), '1 2 3 4')

        tail = List(5, 6)
        list_ += tail  # shallow copy, see examples below
        self.assertEqual(list_.print(), '1 2 3 4 5 6')

        tail.head.value = 0
        self.assertEqual(tail.print(), '0 6')  # element 5 in tail is changed
        self.assertEqual(list_.print(), '1 2 3 4 5 6')  # element 5 in list_ is NOT changed

        list_ += [7, 8]
        self.assertEqual(list_.print(), '1 2 3 4 5 6 7 8')
        list_ += ()
        self.assertEqual(list_.print(), '1 2 3 4 5 6 7 8')

    def test_iteration(self):
        list_ = List(*range(1, 9))
        self.assertEqual([2 ** elem for elem in list_], [2, 4, 8, 16, 32, 64, 128, 256])

    def test_multiple_iterators(self):
        list_ = List(1, 2, 3)
        iterator1 = iter(list_)
        iterator2 = iter(list_)

        self.assertEqual(next(iterator1), 1)
        self.assertEqual(next(iterator1), 2)
        self.assertEqual(next(iterator2), 1)
        self.assertEqual(next(iterator1), 3)

    def test_print_reversed(self):
        list_ = List(*range(1, 9))
        self.assertEqual(list_.print_reversed(), '8 7 6 5 4 3 2 1')

    def test_empty_list(self):
        empty_list = List()
        self.assertEqual(empty_list.print(), '')

    def test_none_value(self):
        list_with_single_none_element = List(None)
        self.assertEqual(list_with_single_none_element.print(), 'None')
