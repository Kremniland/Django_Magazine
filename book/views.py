from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from .models import books
from .forms import BookAddForm

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


def template_book_list(request):
    book_list = books.objects.order_by('name')
    context = {
        'title': 'Список книг',
        'book_list': book_list
    }
    return render(request, 'book/books/books-list.html', context)


def template_book_detail(request, book_id):
    # book_one = books.objects.get(pk=book_id)
    book_one = get_object_or_404(books, pk=book_id)
    context = {
        # 'title': 'Книга: ' + book_one.name,
        # 'title': book_one.name,
        'book': book_one,
    }
    return render(request, 'book/books/books-detail.html', context)


def template_book_add(request):
    if request.method == "POST":
        # Создания записи о книге и сохранения в базу данных
        # book_db = books.objects.create(
        #     name=request.POST['name'],
        #     count_pages=request.POST['count_pages'],
        #     price=request.POST['price'],
        # )
        # print(book_db)
        # print(book_db.name)
        # print(book_db.price)
        # print(book_db.count_pages)
        # ==
        # Сначала создаём объект книги (создаём запись (в приложении))
        # book_obj = books(name=request.POST['name'], price=request.POST['price'])
        # print(book_obj)
        # print(book_obj.name)
        # print(book_obj.price)
        # print(book_obj.count_pages)
        # # Сохранение объекта в базу данных
        # book_obj.save()

        # Forms
        bookform_post = BookAddForm(request.POST)
        
        # Если полученные со страницы данные валидируются:
        if bookform_post.is_valid():
            print(bookform_post.cleaned_data) # cleaned_data хранит данные прописанные на форме

            books.objects.create(
                name=bookform_post.cleaned_data['name'],
                count_pages=bookform_post.cleaned_data['count_pages'],
                price=bookform_post.cleaned_data['price'],
                description=bookform_post.cleaned_data['description'],
            )

            return HttpResponseRedirect('/book/books/list/all/')
        
        # Если не валидируются просто вернем страницу:
        else:
            context = {
                'title': 'Добавление новой книги',
                'custom_form': bookform_post,
            }
            return render(request, 'book/books/books-add.html', context)

    bookForm = BookAddForm()
    context = {
        'title': 'Добавление новой книги',
        'custom_form': bookForm,
    }
    return render(request, 'book/books/books-add.html', context)

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
