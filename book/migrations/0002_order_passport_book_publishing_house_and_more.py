# Generated by Django 4.1.2 on 2022-11-07 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('date_finish', models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения заказа')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена заказа')),
                ('address_delivery', models.CharField(max_length=255, verbose_name='Адрес доставки')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['date_create'],
            },
        ),
        migrations.CreateModel(
            name='passport_book',
            fields=[
                ('article', models.IntegerField(verbose_name='Артикль')),
                ('features', models.CharField(max_length=255, verbose_name='Свойства книги')),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='book.books')),
            ],
            options={
                'verbose_name': 'Паспорт книги',
                'verbose_name_plural': 'Паспорт книги',
            },
        ),
        migrations.CreateModel(
            name='publishing_house',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название')),
                ('agent_firstname', models.CharField(max_length=50, verbose_name='Фамилия представителя')),
                ('agent_name', models.CharField(max_length=50, verbose_name='Имя представителя')),
                ('agent_patronymic', models.CharField(max_length=50, null=True, verbose_name='Отчество представителя')),
                ('agent_telephone', models.CharField(max_length=50, null=True, verbose_name='Телефон представителя')),
            ],
            options={
                'verbose_name': 'Издатель',
                'verbose_name_plural': 'Издатели',
            },
        ),
        migrations.AlterModelOptions(
            name='books',
            options={'ordering': ['name', '-price'], 'verbose_name': 'Книга', 'verbose_name_plural': 'Книги'},
        ),
        migrations.AlterField(
            model_name='books',
            name='count_pages',
            field=models.IntegerField(null=True, verbose_name='Количество страниц'),
        ),
        migrations.AlterField(
            model_name='books',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи'),
        ),
        migrations.AlterField(
            model_name='books',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='books',
            name='exists',
            field=models.BooleanField(default=True, verbose_name='Существует ли?'),
        ),
        migrations.AlterField(
            model_name='books',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название книги'),
        ),
        migrations.AlterField(
            model_name='books',
            name='photo',
            field=models.ImageField(null=True, upload_to='image/%Y/%m/%d', verbose_name='Фотография книги'),
        ),
        migrations.AlterField(
            model_name='books',
            name='price',
            field=models.FloatField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='books',
            name='release_date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата издания'),
        ),
        migrations.AlterField(
            model_name='books',
            name='update_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления записи'),
        ),
        migrations.CreateModel(
            name='pos_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_books', models.IntegerField(verbose_name='Количество книг')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.books', verbose_name='Книга')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Позиция заказа',
                'verbose_name_plural': 'Позиции заказов',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='books',
            field=models.ManyToManyField(through='book.pos_order', to='book.books'),
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('books', models.ManyToManyField(to='book.books')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.AddField(
            model_name='books',
            name='publisher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='book.publishing_house', verbose_name='Издатель'),
        ),
    ]