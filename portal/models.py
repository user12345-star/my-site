from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    email = models.EmailField(max_length=50, verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, verbose_name='Фото профиля')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('flowers', 'Цветы'),
        ('bouquets', 'Букеты'),
    ]

    FLOWERS_CHOICES = [
        ('roses', 'Розы'),
        ('tulips', 'Тюльпаны'),
        ('peonies', 'Пионы'),
        ('lilies', 'Лилии'),
        ('daisies', 'Ромашки'),
        ('baskets', 'Корзины с цветами'),
    ]

    BOUQUETS_CHOICES = [
        ('classic', 'Классические'),
        ('original', 'Оригинальные'),
        ('edible', 'Съедобные'),
        ('wedding', 'Свадебные'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    additional_image_1 = models.ImageField(upload_to='products/flowers/', null=True, blank=True, verbose_name='Дополнительное изображение 1')
    additional_image_2 = models.ImageField(upload_to='products/flowers/', null=True, blank=True, verbose_name='Дополнительное изображение 2')
    additional_image_3 = models.ImageField(upload_to='products/flowers/', null=True, blank=True, verbose_name='Дополнительное изображение 3')
    composition = models.TextField(verbose_name='Состав')
    width = models.FloatField(verbose_name='Ширина (см)')
    length = models.FloatField(verbose_name='Длина (см)')

    flowers = models.CharField(
        max_length=20,
        choices=FLOWERS_CHOICES,
        null=True,
        blank=True,
        verbose_name='Цветы'
    )

    bouquets = models.CharField(
        max_length=20,
        choices=BOUQUETS_CHOICES,
        null=True,
        blank=True,
        verbose_name='Букеты'
    )

    def __str__(self):
        return self.name


class Promotion(models.Model):
    image = models.ImageField(
        upload_to='promotions/',
        verbose_name='Изображение')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date_info = models.CharField(max_length=100, verbose_name='Информация о дате')

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    comment_text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления')

    def __str__(self):
        return f'Комментарий от {self.name}'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    review_text = models.TextField(verbose_name='Отзыв')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отзыв от {self.user.userprofile.first_name} {self.user.userprofile.last_name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('collecting', 'Собираем'),
        ('shipped', 'Отправлен'),
        ('received', 'Получен'),
        ('cancelled', 'Отменен'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('immediate', 'Оплата сразу'),
        ('upon_receipt', 'Оплата при получении'),
    ]

    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    name = models.CharField(max_length=100, verbose_name='Имя получателя')
    phone = models.CharField(max_length=20, verbose_name='Телефон получателя')
    email = models.EmailField(verbose_name='Email получателя')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    delivery_date = models.DateTimeField(verbose_name='Дата и время доставки')
    wishes = models.TextField(blank=True, verbose_name='Пожелания')
    payment_method = models.CharField(
        max_length=15,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='collecting',
        verbose_name='Статус'
    )

    def __str__(self):
        return f'Заказ {self.id} от {self.user_profile.first_name} {self.user_profile.last_name}'


