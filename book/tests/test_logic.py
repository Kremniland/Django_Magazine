from django.test import TestCase
from book.utils import *


class NDSTestCase(TestCase):
    def test_NDS(self):
        result = NDS(100)
        self.assertEqual(10, result)

    def test_NDS_proc(self):
        result = NDS(200, 0.35)
        self.assertEqual(70, result)

    def test_NDS_full(self):
        result = NDS_full(50)
        self.assertEqual(55, result)

    def test_NDS_full_proc(self):
        result = NDS_full(50, 0.20)
        self.assertEqual(60, result)


class DefaultValueTestCase(TestCase, DefaultValue):
    def test_DefaultValue_pass(self):
        context = {}
        context = self.template_title_value(context)
        self.assertTrue(context == {'title': 'Страница книг'})

    def test_DefaultValue_fail(self):
        context = {'name': 'Название'}
        context = self.template_title_value(context)
        self.assertFalse(context == {'title': 'Страница книг'})
