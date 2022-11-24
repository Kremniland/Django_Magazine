from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import books, publishing_house, category, order, pos_order, passport_book
from .forms import RegistrationForm, LoginForm, ContactForm, BookAddForm, BookForm, PublishingHouseForm, CategoryForm, OrderForm  # BookAddForm - Form, BookForm - ModelForm

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.urls import reverse, reverse_lazy

from django.core.paginator import Paginator

from book.utils import DefaultValue

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

from django.contrib import messages

# Registration Auth
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

# EMAIL
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings

# API
from django.http import JsonResponse
from .seializers import BooksSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    paginator = Paginator(book_list, 1)
    # print(paginator)
    # print(paginator.count)
    # print(paginator.object_list)
    # print(paginator.page(2).object_list)
    # print(paginator.page_range)
    # print(paginator.num_pages)

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
@permission_required('book.add_books')
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
        'form': bookForm,
    }
    return render(request, 'book/books/books-add.html', context)

# class
# ListView

# Используем Mixin(DefaultValue)
class ListBooks(ListView, DefaultValue):  # Возврат листа объектов (книг)
    model = books  # Определяем модель для получения данных
    template_name = 'book/books/books-list.html'  # Установка шаблона
    context_object_name = 'book_list'  # Изменение ключа для передачи данных (object_list)
    extra_context = {  # Доп значения (вторичные/статичные данные)
        'title': 'Список книг из класса'
    }

    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs): # Переопределение метода для добавления доп. данных
        context = super().get_context_data(**kwargs)
        
        # Добавляем из своего класса заголовок по умолчанию:
        context = self.template_title_value(context)
        
        context['title'] = 'Список книг из класса (полученные внутри метода get_context_data)'
        context['count_pub'] = publishing_house.objects.all().count()
        
        # Получение категорий
        context['categories'] = category.objects.all()
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

class DetailBook(DetailView, DefaultValue):
    model = books
    template_name = 'book/books/books-detail.html'
    context_object_name = 'book' # По умолчанию object
    pk_url_kwarg = 'book_id'  # Переопределение получаемого параметра
    
    def get_context_data(self, *, object_list=None, **kwargs):  # Переопределение метода для добавления доп. данных
        context = super().get_context_data(**kwargs)
        # Добавляем из своего класса заголовок по умолчанию:
        context = self.template_title_value(context)
        
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

class CreateBook(CreateView, DefaultValue):
    model = books
    form_class = BookForm  # Форма, которая будет использоваться
    template_name = 'book/books/books-add.html'
    # context_object_name = 'custom_form'
    success_url = reverse_lazy('book_list_class')  # Путь переадресации при успешном добавлении

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.template_title_value(context)
        return context

# Добавляем проверку на авторизированного пользователя:
    @method_decorator(login_required) # Вставляем login_required для проверки регистрации    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# HttpResponseRedirect('/book/books/index/') -> Переадресация по пути
# reverse('book_list_class') -> book/books/class/list/all/ - возврат пути указанного имени

# redirect('book_list_detail') -> Переадресация по названию пути == HttpResponseRedirect(reverse('book_list_detail'))

class UpdateBook(UpdateView):
    model = books
    form_class = BookForm
    template_name = 'book/books/books-update.html'
    pk_url_kwarg = 'book_id'

# Проверка прав доступа на изменение, при попытке изменить выведет 404
    @method_decorator(permission_required('book.change_books'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class DeleteBook(DeleteView):
    model = books
    template_name = 'book/books/books-delete.html'
    success_url = reverse_lazy('book_list_class')

# Проверка прав доступа на удаление, при попытке удалить выведет 404
    @method_decorator(permission_required('book.delete_books'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# Category
class DetailCategory(DetailView):
    model = category
    template_name = 'book/category/category-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
          # context['list_books'] = category.objects.get(pk=context['pk']).books.all()
        context['list_books'] = context['object'].books.all()
        return context

# Registration
def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        # form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            # Войдет сразу после регистрации
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('log in')
        messages.error(request, 'Что-то пошло не так')
    else:
        form = RegistrationForm()
        # form = UserCreationForm()
    return render(request, 'book/auth/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # form = AuthenticationForm(data=request.POST)
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('auth: ',request.user.is_authenticated)
            print('anon: ',request.user.is_anonymous)
            login(request, user)
            print('auth: ', request.user.is_authenticated)
            print('anon: ', request.user.is_anonymous)
            messages.success(request, 'Вы успешно авторизировались')
            return redirect('book_list_class')
        messages.error(request, 'Что-то пошло не так')
    else:
        # form = AuthenticationForm()
        form = LoginForm()
    return render(request, 'book/auth/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('log in')

# Метод проверки авторизации:
def is_login_user(request):
    if request.user.is_authenticated:
        return HttpResponse('Вы зарегистрированный пользователь')
    elif request.user.is_anonymous:
        return HttpResponse('Вы анонимны для сайта')

@login_required
def is_login_required(request): # Если не авторизован выдаст 404
    return HttpResponse('<h1>Вы авторизированный пользователь</h1>')

# Проверка прав доступа:
# request.user.has_perms проверяет список прав, hes_perm какое то одно право
# request.user.has_perm('book.view_category') - <приложение>.<право>_<модель>
def is_permission(request):
    text = ''
    if request.user.has_perm('book.change_books'):
        text += '<h1>У вас имеется право на изменение книг</h1>'
    if request.user.has_perm('book.view_category'):
        text += '<h1>У вас имеется право на просмотр категорий</h1>'
    if request.user.has_perm('book.add_books'):
        text += '<h1>У вас имеется право на добавление книг</h1>'
    if request.user.has_perm('book.delete_books'):
        text += '<h1>У вас имеется право на удаление книг</h1>'
    if text == '':
        text += '<h1>Вы не имеет никаких прав доступа</h1>'
    if request.user.is_anonymous:
        text += '<h1>Вы не авторизовались</h1>'
    if request.user.is_authenticated:
        text += '<h1>Вы авторизовались</h1>'

    if request.user.has_perms(['book.add_books', 'book.add_category']):
        text += '<h1>Вы имеет право на добавление информации на сайт</h1>'

    return HttpResponse(text)

# ('book.add_books') - <приложение>.<право>_<модель>
@permission_required('book.add_books')
def is_perm_add(request):
    return HttpResponse('<h1>Добавление книги</h1>')


@permission_required('book.change_books')
def is_perm_change(request):
    return HttpResponse('<h1>Изменение книги</h1>')


@permission_required(['book.add_books', 'book.change_books'])
def is_perm_add_and_change(request):
    return HttpResponse('<h1>Добавление и изменение книги</h1>')

# EMAIL

def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['kremnilandk@gmail.com'],
                fail_silently=False # При ошибке будет ее показывать, если True - то нет
            )
            if mail:
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('book_list_class')
            else:
                messages.error(request, 'Письмо не удалось отправить, попробуйте позже.')
        else:
            messages.warning(request, 'Письмо неверно заполнено, перепроверьте внесенные данные.')
    else:
        form = ContactForm()
    return render(request, 'book/email.html', {'form': form})

@api_view(['GET', 'POST'])
def book_api_list(request):
    if request.method == 'GET':  # Получение данных
        # book_list = books.objects.all()
        book_list = books.objects.filter(exists=True)
        serializer = BooksSerializer(book_list, many=True) # many=True для того что бы список принимался по отдельным объектам
        print(serializer.data)
        # return JsonResponse(serializer.data, safe=False)
        # return JsonResponse({'books': serializer.data})
        return Response({'books': serializer.data})
    elif request.method == 'POST':  # Добавляем объект в БД
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # при успешном добавлении
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Вывод изменение удаление смотря какой метод запроса
@api_view(['GET', 'PUT', 'DELETE'])
def book_api_detail(request, pk):
    book_obj = get_object_or_404(books, pk=pk)

    # Вывод
    if request.method == 'GET':
        serializer = BooksSerializer(book_obj)
        return Response(serializer.data)
    # Изменение
    elif request.method == 'PUT':
        serializer = BooksSerializer(book_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Данные успешно обновлены', 'book': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # Удаление
    elif request.method == 'DELETE':
        book_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

# ============================== МОИ ДОБАВЛЕНИЯ ===============================

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
