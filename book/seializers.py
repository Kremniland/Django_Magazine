# API

from rest_framework import serializers
from .models import books, publishing_house


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = books
        # fields = '__all__'
        fields = ['pk', 'name', 'description', 'price', 'count_pages', 'exists', 'publisher']


class EmailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    subject = serializers.CharField()
    content = serializers.CharField()
