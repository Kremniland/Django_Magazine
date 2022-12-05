from rest_framework.test import APITestCase
from django.urls import reverse
from book.models import books
from book.seializers import BooksSerializer
from rest_framework import status


class BookAPITestCase(APITestCase):
    def test_get_list(self):
        book_1 = books.objects.create(name='Test1', price=194.5)
        book_2 = books.objects.create(name='Test2', price=223.78, description='Книга для тестирования')
        url = reverse('book_list_api')

        print(url)
        print(book_1)
        print(book_2)

        response = self.client.get(url)

        serial_data = BooksSerializer([book_1, book_2], many=True).data
        serial_data = {'books': serial_data}

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serial_data, response.data)

    def test_post_list(self):
        # Проверка со стороны тест-кейс
        book_1 = books(pk=3, name='Test1', price=374.12, exists=False)
        serial_data = BooksSerializer(book_1).data

        # Проверка со стороны проекта (views.book_api_list)
        url = reverse('book_list_api')
        response = self.client.post(url, data={
            'name': 'Test1',
            'price': 374.12
        })

        print(url)
        print(book_1)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(serial_data, response.data)
