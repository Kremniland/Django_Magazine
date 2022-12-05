from book.utils import NDS
from django.test import TestCase

class TestUtils(TestCase):
    def test_nds(self):
        result = NDS(100)
        return self.assertEqual(10, result)

def test_foo(x,y):
    return x+y

assert test_foo(2,2)==4

assert NDS(100)==10