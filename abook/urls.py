from django.urls import path
import abook.views as v

urlpatterns = [
    path('', v.get_index, name='home'),
]