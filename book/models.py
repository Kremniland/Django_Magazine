from django.db import models


class books(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название книги')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    count_pages = models.IntegerField(null=True, verbose_name='Количество страниц')
    price = models.FloatField(verbose_name='Цена')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата издания')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления записи')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, verbose_name='Фотография книги')
    exists = models.BooleanField(default=True, verbose_name='Существует ли?')

    publisher = models.ForeignKey('publishing_house', on_delete=models.PROTECT, null=True, verbose_name='Издатель')

    def __str__(self):
        return self.name
        # + " - " + str(self.price)

    class Meta:  # Класс для атрибутов относящихся к модели (вывод админки)
        verbose_name = 'Книга'  # Псевдоним таблицы в ед. числе
        verbose_name_plural = 'Книги'  # Псевдоним таблицы во мн. числе
        ordering = ['name', '-price']  # Сортировка полей


# Books
#   name
#   description
#   count_pages
#   price
#   release_date
#   create_date
#   update_date
#   photo
#   exists

# Таблица для связи один ко многим
class publishing_house(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    agent_firstname = models.CharField(max_length=50, verbose_name='Фамилия представителя')
    agent_name = models.CharField(max_length=50, verbose_name='Имя представителя')
    agent_patronymic = models.CharField(max_length=50, null=True, verbose_name='Отчество представителя')
    agent_telephone = models.CharField(max_length=50, null=True, verbose_name='Телефон представителя')

    def __str__(self):
        return self.title + " " + self.agent_firstname + ":" + self.agent_telephone

    class Meta:
        verbose_name = 'Издатель'
        verbose_name_plural = 'Издатели'


# Связь многие ко многим
class category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    books = models.ManyToManyField(books)  # through='category_book')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Связь многие ко многим (через ручную техническую таблицу)
class order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, blank=True, verbose_name='Дата завершения заказа')  # ( ,"")
    price = models.FloatField(null=True, blank=True, verbose_name='Цена заказа')
    address_delivery = models.CharField(max_length=255, verbose_name='Адрес доставки')

    books = models.ManyToManyField(books, through='pos_order')

    def __str__(self):
        return str(self.date_create) + " " + str(self.price) + " " + self.address_delivery

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date_create']


# (Промежуточная (техническая) таблица для связи многие ко многим (Order, Books))
class pos_order(models.Model):
    book = models.ForeignKey(books, on_delete=models.CASCADE, verbose_name='Книга')
    order = models.ForeignKey(order, on_delete=models.CASCADE, verbose_name='Заказ')
    count_books = models.IntegerField(verbose_name='Количество книг')

    def __str__(self):
        return self.order.__str__() + " " + self.book.__str__() + "|" + str(self.count_books)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        ordering = ['order']


# Связь один ко одному
class passport_book(models.Model):
    article = models.IntegerField(verbose_name='Артикль')
    features = models.CharField(max_length=255, verbose_name='Свойства книги')

    book = models.OneToOneField(books, on_delete=models.PROTECT, primary_key=True, verbose_name='Книга')

    # id integer PRIMARY KEY                            параметр - primary_key=False
    # article integer
    # features varchar
    # book integer FOREIGN KEY books(id) UNIQUE

    # book integer FOREIGN KEY books(id) PRIMARY KEY    параметр - primary_key=True
    # article integer
    # features varchar

    def __str__(self):
        return str(self.article) + " | " + self.book.__str__()

    class Meta:
        verbose_name = 'Паспорт книги'
        verbose_name_plural = 'Паспорт книги'

# Команда для запуска консоли - python manage.py shell

# Сохранение записи

# book_one = books(name='451 градус по Фаренгейту',price=160)
# book_one.save()

# book_two = books()
# book_two.name = 'Евгений Онегин'
# book_two.price = 215
# book_two.save()

# books.objects.create(name='Басни',price=90)
# book_three = books.objects.create(name='Басни',price=90)

# Вывод записей

# books.objects.all()
# list_books = books.objects.all()
# list_books[1].name

# book_from_db = books.objects.get(pk=3)

# Изменения данных

# book_from_db = books.objects.get(pk=3)
# book_from_db.name
# book_from_db.price = 190
# book_from_db.save()

# Удаление данных

# book_from_db = books.objects.get(pk=4)
# book_from_db.delete()

# Сортировка данных

# books.objects.order_by('name') # ASC
# books.objects.order_by('-name') # DESC

# books.objects.order_by('name').first() # Вывод первой записи
# books.objects.all().first()

# books.objects.order_by('name').last() # Вывод последней записи
# books.objects.all().last()

# books.objects.earliest('create_date') # Ранняя дата
# books.objects.latest('create_date') # Поздняя дата
