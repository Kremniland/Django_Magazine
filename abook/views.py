from django.shortcuts import render
from django.http import HttpResponse

def get_index(request):
    return render(request, 'abook/index.html')