from django.urls import path

import book.views as v

urlpatterns = [
    path('index/', v.template_index),
    # path('list/', v.template_list),
    path('books/list/all/', v.template_book_list, name='book_list'),
    path('books/<int:book_id>/', v.template_book_detail, name='book_detail'),
    path('books/add/', v.template_book_add, name='book_add'),
    path('publishing/add/', v.template_publishing_house_add, name='publishing_house_add'),
    path('category/add/', v.template_category_add, name='category_add'),
    path('order/add/', v.template_order_add, name='order_add'),

    # ListView
    path('books/class/list/all/', v.ListBooks.as_view(), name='book_list_class'),
    path('publishing/list/all/', v.ListPublishing.as_view(), name='publishing_list'),
    path('category/list/all/', v.ListCategory.as_view(), name='category_list'),

   # DetailView
    # path('books/class/<int:pk>', v.DetailBook.as_view(), name='book_detail_class'),
    path('books/class/<int:book_id>/', v.DetailBook.as_view(), name='book_detail_class'),
    path('publishing/<int:publishing_id>/', v.DetailPublishing.as_view(), name='publishing_detail'),

    # CreateView
    path('books/class/add/', v.CreateBook.as_view(), name='book_add_class'),

    # UpdateView
    path('books/class/update/<int:book_id>', v.UpdateBook.as_view(), name='book_update_class'),
 
    # DeleteView
    path('books/class/delete/<int:pk>', v.DeleteBook.as_view(), name='book_delete_class'),
 

    # path('index/list/', v.template_list),

    # path('req/', v.req),
    # path('html/', v.tag),
    # path('booklist/', v.html_page),
    # path('META/', v.req_META),
]
