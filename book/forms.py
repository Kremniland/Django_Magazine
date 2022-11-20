from django import forms

from .models import books, publishing_house, category, order, pos_order, passport_book

import re
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

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
    category = forms.ModelMultipleChoiceField(
        label='Жанры',
        queryset=category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
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


class PublishingHouseForm(forms.ModelForm):
    class Meta:
        model = publishing_house
        fields = ['title', 'agent_firstname', 'agent_name','agent_patronymic','agent_telephone']
        
        widgets = {
            'title': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'agent_firstname': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'agent_name': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'agent_patronymic': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'agent_telephone': forms.NumberInput(
                attrs={

                    'class': 'form-control',
                }
            ),
        }
    
    def clean_agent_telephone(self):
        agent_telephone = self.cleaned_data['agent_telephone']
        if re.match(r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}', agent_telephone):
            raise ValidationError('Формат записи телефона:+7(___)___-__-__')
        return agent_telephone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['title', 'description', 'books']

        widgets = {
            'title': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'descriptions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'books': forms.SelectMultiple(
                attrs={

                    'class': 'form-control',
                }
            )
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['date_finish', 'price', 'address_delivery']

        widgets = {            
            'date_finish': forms.SelectDateWidget(
                attrs={

                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            'address_delivery': forms.TextInput(
                attrs={

                    'class': 'form-control',
                }
            ),
            # 'books': forms.SelectMultiple(
            #     attrs={

            #         'class': 'form-control',
            #     }
            # ),
        }

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget= forms.TextInput(attrs={'class': 'form-control',}),
        min_length=2,
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )
    password1 = forms.CharField(
        label='Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control',}),
        # }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Ваш логин',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
        min_length=2,
    )
    password = forms.CharField(
        label='Ваш пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', }),
    )

class ContactForm(forms.Form):
    # recipient = forms.EmailField(
    #     label='Получатель',
    #     widget=forms.EmailInput(
    #         attrs={'class': 'form-control',}
    #     )
    # )
    subject = forms.CharField(
        label='Заголовок письма:',
        widget=forms.TextInput(
            attrs={'class': 'form-control',}
        ),       
    )
    content = forms.CharField(
        label='Текст письма:',
        widget=forms.Textarea(
            attrs={
            'class': 'form-control',
            'rows': 7,
            }
        )
    )