from django.urls import path

import book.views as v

urlpatterns = [
    path('index/', v.template_index),
    # path('list/', v.template_list),
    path('books/list/all/', v.template_book_list, name='book_list'),
    path('books/<int:book_id>/', v.template_book_detail, name='book_detail'),
    path('books/add/', v.template_book_add, name='book_add'),

    # path('index/list/', v.template_list),

    # path('req/', v.req),
    # path('html/', v.tag),
    # path('booklist/', v.html_page),
    # path('META/', v.req_META),
]
