from django.contrib import admin
from .models import books, publishing_house, passport_book, order, pos_order, category


# Отображение списка в админке
class BooksAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'exists')  # Отображение полей
    list_display_links = ('name',)  # Установка ссылок на атрибуты
    search_fields = ('name', 'price')  # Поиск по полям
    list_editable = ('price', 'exists')  # Изменяемые поля
    list_filter = ('exists',)  # Фильтры полей


admin.site.register(books, BooksAdmin)

#  Название атрибутов прописывается в самих атрибутах (models)
#  Название записи прописывается в __str__ (models)
#  Название модели и сортировка её атрибутов прописывается в классе Meta (models)
#  Отображение списка записей в админке прописывается в модуле админки приложения (admin)
#  Название приложения прописывается в настройках приложения (apps)

admin.site.register(publishing_house)
admin.site.register(passport_book)
admin.site.register(order)
admin.site.register(pos_order)
admin.site.register(category)
