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
    path('category/<int:pk>/', v.DetailCategory.as_view(), name='category_detail_class'),

# CreateView
    path('books/class/add/', v.CreateBook.as_view(), name='book_add_class'),

# UpdateView
    path('books/class/update/<int:book_id>', v.UpdateBook.as_view(), name='book_update_class'),
 
# DeleteView
    path('books/class/delete/<int:pk>', v.DeleteBook.as_view(), name='book_delete_class'),

 # Регистрация и авторизация
    path('registration/', v.user_registration, name='regis'),
    path('login/', v.user_login, name='log in'),
    path('logout/', v.user_logout, name='log out'),

# Проверка регистрации
    path('is_login_user/', v.is_login_user),
    path('is_login_required/', v.is_login_required),

# Проверка прав доступа
    path('is_permission/', v.is_permission),

    path('is_add/', v.is_perm_add),
    path('is_change/', v.is_perm_change),
    path('is_add_and_change/', v.is_perm_add_and_change),

# EMAIL
    path('contact/', v.contact_email, name='contact_email'),

# API
    path('api/books/', v.book_api_list, name='book_list_api'),
    path('api/books/<int:pk>', v.book_api_detail, name='book_detail_api'),

    
    # path('index/list/', v.template_list),

    # path('req/', v.req),
    # path('html/', v.tag),
    # path('booklist/', v.html_page),
    # path('META/', v.req_META),
]
