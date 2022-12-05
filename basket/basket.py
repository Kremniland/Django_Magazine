from django.conf import settings
from book.models import books

class Basket:
    # Инициализация корзины
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def save(self):
        # Обновление ключа basket в сессии
        self.session[settings.BASKET_SESSION_ID] = self.basket
        # Отметка сеанса в роли "измененный", для сохранения данных
        self.session.modified = True

    def add(self, product, count_product=1, update_count=False):
        prod_pk = str(product.pk)  # Сохранение ID в переменную (в качестве ключа)

        # Проверка наличия продукта в корзине (если нет, то добавляем)
        # if not prod_pk not in self.basket: if not 5 in not self.basket[4] - True
        # if not prod_pk not in self.basket: if not 5 in not self.basket[5] - False
        if prod_pk not in self.basket:
            self.basket[prod_pk] = {
                'count_prod': 0,
                'price_prod': str(product.price)
            }
        # Обновление количества продуктов
        # (update_count=True - перезадаем количество)
        # (update_count=False - дополняем количество)
        if update_count:
            self.basket[prod_pk]['count_prod'] = count_product
        else:
            self.basket[prod_pk]['count_prod'] += count_product

        # Сохранение корзины
        self.save()

    def remove(self, product):
        prod_pk = str(product.pk)
        # Если удаляемый товар лежит в корзине, то очищаем данное значение в сессии
        if prod_pk in self.basket:  # if 5 in basket[5] - True
            del self.basket[prod_pk]
            self.save()

    def get_total_price(self): # Считаем цену товара в корзине
        # sum_price = 0
        # for item in self.basket.values():
        #     sum_price += float(item['price_prod']) * int(item['count_prod'])
        # return sum_price
        # ==
        return sum(float(item['price_prod']) * int(item['count_prod']) for item in self.basket.values())

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.session.modified = True

    def __len__(self): # Колличество товара в корзине
        return sum(int(item['count_prod']) for item in self.basket.values())

    def __iter__(self):
        # Получение первичных ключей
        list_prod_pk = self.basket.keys()

        # Загрузка данных из БД
        list_prod_obj = books.objects.filter(pk__in=list_prod_pk)

        # Копирование корзины для дальнейшей работы
        basket = self.basket.copy()
        # Перебор и добавление объектов из бд в корзину
        for prod_obj in list_prod_obj:
            basket[str(prod_obj.pk)]['book'] = prod_obj

        # Перебор позиций и вывод общей суммы позиции
        for item in basket.values():
            item['total_price'] = float(item['price_prod']) * int(item['count_prod'])
            yield item
