from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import books, publishing_house, category, order, pos_order, passport_book
from .forms import BookAddForm, BookForm, PublishingHouseForm, CategoryForm, OrderForm  # BookAddForm - Form, BookForm - ModelForm

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator

def template_index(request):
    return render(request, 'book/index.html')


def template_list(request):
    # print(request.GET.get('name'))
    # var = request.GET['name']
    context = dict()
    if request.method == 'GET':
        print(request.GET['name'])
        print(request.GET['count'])

        context = {
            'title': 'Список книг',
            'name_book': request.GET['name'],
            'count_book': request.GET['count'],
        }
    elif request.method == 'POST':
        context = {
            'title': 'Список книг',
            'name_book': request.POST['name'],
            'count_book': request.POST['count'],
        }
    return render(request, 'book/list.html', context)

# С пагинацией страниц
def template_book_list(request):
    book_list = books.objects.order_by('name')
    paginator = Paginator(book_list, 2)
    print(paginator)
    print(paginator.count)
    print(paginator.object_list)
    print(paginator.page(2).object_list)
    print(paginator.page_range)
    print(paginator.num_pages)

    page_num = request.GET.get('page',1) # Получаем значение страницы
    page_obj = paginator.get_page(page_num) # Получаем саму страницу по значению (часть из нашего множества)
    context = {
        'title': 'Список книг',
        'book_list': book_list,
        'page_obj': page_obj,
    }
    return render(request, 'book/books/books-list.html', context)


def template_book_detail(request, book_id):
    # book_one = books.objects.get(pk=book_id)
    book_one = get_object_or_404(books, pk=book_id)
    context = {
        # 'title': 'Книга: ' + book_one.name,
        # 'title': book_one.name,
        'book': book_one,
        'categories': book_one.category_set.all()
    }
    return render(request, 'book/books/books-detail.html', context)


# Добавление новой книги в ручную и через Forms
# def template_book_add(request):
#     if request.method == "POST":
#         # Создания записи о книге и сохранения в базу данных
#         # book_db = books.objects.create(
#         #     name=request.POST['name'],
#         #     count_pages=request.POST['count_pages'],
#         #     price=request.POST['price'],
#         # )
#         # print(book_db)
#         # print(book_db.name)
#         # print(book_db.price)
#         # print(book_db.count_pages)
#         # ==
#         # Сначала создаём объект книги (создаём запись (в приложении))
#         # book_obj = books(name=request.POST['name'], price=request.POST['price'])
#         # print(book_obj)
#         # print(book_obj.name)
#         # print(book_obj.price)
#         # print(book_obj.count_pages)
#         # # Сохранение объекта в базу данных
#         # book_obj.save()

#         # Forms
#         bookform_post = BookAddForm(request.POST)
        
#         # Если полученные со страницы данные валидируются:
#         if bookform_post.is_valid():
#             print(bookform_post.cleaned_data) # cleaned_data хранит данные прописанные на форме

#             books.objects.create(
#                 name=bookform_post.cleaned_data['name'],
#                 count_pages=bookform_post.cleaned_data['count_pages'],
#                 price=bookform_post.cleaned_data['price'],
#                 description=bookform_post.cleaned_data['description'],
#             )
            # Сохранения выбранных категорий в книгу
            # for categ in bookForm.cleaned_data['category']:
            #     book_one.category_set.add(categ)

#             return HttpResponseRedirect('/book/books/list/all/')
        
#         # Если не валидируются просто вернем страницу:
#         else:
#             context = {
#                 'title': 'Добавление новой книги',
#                 'custom_form': bookform_post,
#             }
#             return render(request, 'book/books/books-add.html', context)

#     bookForm = BookAddForm()
#     context = {
#         'title': 'Добавление новой книги',
#         'custom_form': bookForm,
#     }
#     return render(request, 'book/books/books-add.html', context)

# Добавление новой книги через ModelForm:
def template_book_add(request):
    if request.method == "POST":
        bookForm = BookForm(request.POST)
        if bookForm.is_valid():
            print(bookForm.cleaned_data)  # cleaned_data хранит данные прописанные на форме
            books.objects.create(
                name=bookForm.cleaned_data['name'],
                count_pages=bookForm.cleaned_data['count_pages'],
                price=bookForm.cleaned_data['price'],
                description=bookForm.cleaned_data['description'],
                publisher=bookForm.cleaned_data['publisher'],
            )
            # ==
            # books.objects.create(
            #     **bookForm.cleaned_data
            # )
            return HttpResponseRedirect('/book/books/list/all/')
    else:
        bookForm = BookForm()
    context = {
        'title': 'Добавление новой книги',
        'custom_form': bookForm,
    }
    return render(request, 'book/books/books-add.html', context)

# class
# ListView

class ListBooks(ListView):  # Возврат листа объектов (книг)
    model = books  # Определяем модель для получения данных
    template_name = 'book/books/books-list.html'  # Установка шаблона
    context_object_name = 'book_list'  # Изменение ключа для передачи данных (object_list)
    extra_context = {  # Доп значения (вторичные/статичные данные)
        'title': 'Список книг из класса'
    }

    def get_context_data(self, *, object_list=None, **kwargs): # Переопределение метода для добавления доп. данных
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список книг из класса (полученные внутри метода get_context_data)'
        context['count_pub'] = publishing_house.objects.all().count()
        return context

    def get_queryset(self): # Переопределение запроса
        return books.objects.filter(exists=True).order_by('release_date')
# ==
# def template_book_list(request):
#     book_list = books.objects.order_by('name')
#     context = {
#         'title': 'Список книг',
#         'book_list': book_list,
#         'count_pub': publishing_house.objects.all().count()
#     }
#     return render(request, 'book/books/books-list.html', context)

# DetailView

class DetailBook(DetailView):
    model = books
    template_name = 'book/books/books-detail.html'
    context_object_name = 'book' # По умолчанию object
    pk_url_kwarg = 'book_id'  # Переопределение получаемого параметра
    
    def get_context_data(self, *, object_list=None, **kwargs):  # Переопределение метода для добавления доп. данных
        context = super().get_context_data(**kwargs)
        # Получение категорий из объекта книги
        context['categories'] = context['book'].category_set.all()

        # Добавление связи книги и категории
        # book_one = books.objects.get(pk=1)
        # categ = category.objects.get(pk=2)
        #
        # book_one.category_set.add(categ)
        #
        # # Создание категории из книги
        # book_one.category_set.create(name='Детектив', description='')
        return context
# ==
# def template_book_detail(request, book_id):
#     # book_one = books.objects.get(pk=book_id)
#     book_one = get_object_or_404(books, pk=book_id)
#     context = {
#         # 'title': 'Книга: ' + book_one.name,
#         # 'title': book_one.name,
#         'book': book_one,
#     }
#     return render(request, 'book/books/books-detail.html', context)    

def template_publishing_house_add(request):
    if request.method == 'POST':
        publishing_house_form = PublishingHouseForm(request.POST)
        if publishing_house_form.is_valid():
            publishing_house.objects.create(
                **publishing_house_form.cleaned_data
            )
            return HttpResponseRedirect('/book/publishing/list/all/')
        else:
            context = {
                'title': 'Добавление издательства',
                'publishing_form': publishing_house_form,
            }
            return render(request, 'book/books/publishing-add.html', context)                    
    publishing_house_form = PublishingHouseForm()
    context = {
        'title': 'Заполнение анкеты издательства',
        'publishing_form': publishing_house_form,
    }
    return render(request, 'book/publishing/publishing-add.html', context)

class ListPublishing(ListView):
    model = publishing_house
    template_name = 'book/publishing/publishing-list.html'
    context_object_name = 'publishing_list'
    
    def get_context_data(self, *, object_list=None, **kwargs): # Переопределение метода для добавления доп. данных
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список издательств'
        return context

class DetailPublishing(DetailView):
    model = publishing_house
    template_name = 'book/publishing/publishing-detail.html'
    pk_url_kwarg = 'publishing_id'  # Переопределение получаемого параметра
    context_object_name = 'publishing'

def template_category_add(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category.objects.create(
                title=category_form.cleaned_data['title'],
                description=category_form.cleaned_data['description'],
                # books=category_form.changed_data['books'],
            )
            return HttpResponseRedirect('/book/category/list/all/')
    else:
        category_form = CategoryForm()
    context = {
        'title': 'Заполнение категорий',
        'category_form': category_form,
    }
    return render(request, 'book/category/category-add.html', context)
        
class ListCategory(ListView):
    model = category
    template_name = 'book/category/category-list.html'
    context_object_name = 'category_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список жанров'
        return context

def template_order_add(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order.objects.create(
                date_finish=order_form.cleaned_data['date_finish'],
                price=order_form.cleaned_data['price'],
                address_delivery=order_form.cleaned_data['address_delivery'],
                # books=order_form.cleaned_data['books']
                # **order_form.cleaned_data
            )
            return HttpResponseRedirect('/book/order/list/all/')
    else:
        order_form = OrderForm()
    context = {
        'title': 'Заполнение заказа',
        'order_form': order_form,
    }
    return render(request, 'book/order/order-add.html', context)

class CreateBook(CreateView):
    model = books
    form_class = BookForm  # Форма, которая будет использоваться
    template_name = 'book/books/books-add.html'
    # context_object_name = 'custom_form'
    success_url = reverse_lazy('book_list_class')  # Путь переадресации при успешном добавлении


# HttpResponseRedirect('/book/books/index/') -> Переадресация по пути
# reverse('book_list_class') -> book/books/class/list/all/ - возврат пути указанного имени

# redirect('book_list_detail') -> Переадресация по названию пути == HttpResponseRedirect(reverse('book_list_detail'))

class UpdateBook(UpdateView):
    model = books
    form_class = BookForm
    template_name = 'book/books/books-update.html'
    pk_url_kwarg = 'book_id'

class DeleteBook(DeleteView):
    model = books
    template_name = 'book/books/books-delete.html'
    success_url = reverse_lazy('book_list_class')


# --------------------------------------------------
def req(request):
    print(request)
    return HttpResponse('request in print')


def tag(request):
    print(request.META)
    return HttpResponse('<h1>Hello HTML</h1>')


def html_page(request):
    book_list = ['Муму', '1984', '451 градус по Фаренгейту']
    res = ''
    for item in book_list:
        res += f'<h1>{item}</h1>'
    return HttpResponse(res)


def req_META(request):
    meta_output = ''
    for key, value in request.META.items():
        meta_output += f'{key}: {value}<br>'

    return HttpResponse(f"""
    <h2>Запрос пользователя</h2>
    <p>Схема запроса: {request.scheme}</p>
    <p>Тело запроса: {request.body}</p>
    <p>Путь запроса: {request.path}</p>
    <p>Метод запроса: {request.method}</p>
    <p>Параметры GET: {request.GET}</p>
    <p>Параметры POST: {request.POST}</p>
    <p>Параметры COOKIES: {request.COOKIES}</p>
    <p>Параметры FILES: {request.FILES}</p>
    <br>
    <div>{meta_output}</div>
    """)
