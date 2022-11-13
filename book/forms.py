from django import forms

from .models import books, publishing_house, category, order, pos_order, passport_book

import re
from django.core.exceptions import ValidationError


class BookAddForm(forms.Form):
    name = forms.CharField(
        max_length=150,  # Максимальная длина строки
        min_length=2,  # Минимальная длина строки
        strip=True,  # Очищение от пробельных символов
        empty_value='Название',  # Значение при пустой строке
        label='Название книги',  # Псевдоним выводимый на странице
        widget=forms.TextInput(  # Явное определения виджета (формы поля)  [Field(Widget)]
            attrs={  # Перечисление свойств виджета (в теге <input>)
                'class': 'form-control',  # <input class="form-control">
                'placeholder': 'Название книги',  # <input class="form-control" placeholder="Название книги">
            }
        )
    )
    count_pages = forms.IntegerField(
        min_value=5,  # Минимальное числовое значение
        max_value=6000,  # Максимальное числовое значение
        label='Количество страниц',  # Псевдоним выводимый на странице
        initial=100,  # Значение по умолчанию
        step_size=5,  # Шаг значения

        required=False,  # Обязательное поле (True)
        help_text='Впишите количество страниц',  # Подсказка снизу поля

        widget=forms.NumberInput(  # Явное определения виджета (формы поля)  [Field(Widget)]
            attrs={  # Перечисление свойств виджета (в теге <input>)
                'class': 'form-control',  # <input class="form-control">
                'placeholder': 'Количество страниц',  # <input class="form-control" placeholder="Название книги">
            }
        )
    )
    price = forms.FloatField(
        min_value=50,  # Минимальное числовое значение
        label='Цена книги',  # Псевдоним выводимый на странице
        widget=forms.NumberInput(  # Явное определения виджета (формы поля)  [Field(Widget)]
            attrs={  # Перечисление свойств виджета (в теге <input>)
                'class': 'form-control',  # <input class="form-control">
                'placeholder': 'Цена книги',  # <input class="form-control" placeholder="Название книги">
            }
        )
    )
    description = forms.CharField(
        min_length=2,
        label='Описание',
        widget=forms.Textarea(  # Переопределение виджета (TextInput)
            attrs={  # Свойства тега <input>
                'class': 'form-control',
                'placeholder': 'Описание книги',
                'aria-label':'With textarea',
            }
        )
    )
    # bool_field = forms.BooleanField()
    # email_field = forms.EmailField()
    # file_field = forms.FileField()
    # image_field = forms.ImageField()
    # decimal_field = forms.DecimalField(
    #     min_value=5,  # Минимальное числовое значение
    #     max_value=6000,  # Максимальное числовое значение
    #     max_digits=8,  # Максимальное количество цифр в значении (max_length)
    #     decimal_places=2,  # Количество цифр после запятой
    #     step_size=0.01,  # Шаг значения
    # )
    # datetime_field = forms.DateTimeField(
    #     widget=forms.DateTimeInput
    # )
    # date_field = forms.DateField(
    #     widget=forms.SelectDateWidget
    # )
    # time_field = forms.TimeField(
    #     widget=forms.TimeInput
    # )
    # choice_field = forms.ChoiceField(
    #     choices=( # Настройка выпадающего списка
    #         ('dost', "Доставка курьером"),  # Значение (передаваемое), Отображение (на сайте)
    #         ('pocht', "Доставка почтой"),
    #         ('sam', "Самовывоз"),
    #     ),
    #     widget=forms.CheckboxSelectMultiple
    # )


class BookForm(forms.ModelForm):
    class Meta:
        model = books
        # fields = '__all__' # Все поля
        fields = ['name', 'description', 'price', 'count_pages', 'publisher']

        widgets = {
            'name': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'descriptions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'count_pages': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'publisher': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match(r'\d', name):
            raise ValidationError('Название не должно начинаться с цифры')
        return name

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        # if re.match(r'\+7\([0-9][0-9][0-9]\)[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]', telephone):  # +7(___)___-__-__
        if re.match(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}', telephone): # +7(___)___-__-__
            raise ValidationError('Формат записи телефона:+7(___)___-__-__')
        return telephone