from django.core.exceptions import ValidationError
from django.db import models
from pytils.translit import slugify
from django.urls import reverse
import re



def mobile_validate(value):
    mobile_re = re.compile(r'^(8|\+7)?[\d\- ]{10}$')
    if not mobile_re.match(value):
        raise ValidationError('Ошибка формата номера мобильного телефона')



class Trainer(models.Model):
    full_name = models.CharField("ФИО", max_length=40)
    age = models.IntegerField("Возраст", null=True)
    phone = models.CharField("Телефон", max_length=12, validators=[mobile_validate])
    trainer_email = models.EmailField("Почта", blank=True)
    time_create = models.DateTimeField("Регистрация", auto_now=True)
    about_trainer = models.TextField("О тренере", max_length=2000, blank=True)
    photo = models.ImageField(upload_to="trainer/", default=None, null=True, blank=True, verbose_name='Фото')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")


    def save(self, *args, **kwargs):
        self.slug = slugify(self.full_name)
        super(Trainer, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('slug-name', args=[self.slug])

    def __str__(self):
        return f'{self.full_name}'


    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"


class Personnel(models.Model):
    ADMINISTRATOR = 'ADMIN'
    EQUIPMENT_SERVICE = 'EQUIP'
    ACCOUNTANT = 'ACCOU'
    CLEANING_WOMAN = 'CLEAN'
    POSITION = [
        (ADMINISTRATOR, 'Администратор'),
        (EQUIPMENT_SERVICE, 'Техник'),
        (ACCOUNTANT, 'Бухгалтер'),
        (CLEANING_WOMAN, 'Уборщица'),
    ]
    position_gym = models.CharField("Должность", max_length=5, choices=POSITION, default=" ")
    full_name = models.CharField("ФИО", max_length=40)
    age = models.IntegerField("Возраст", null=True)
    phone = models.CharField("Телефон", max_length=12, validators=[mobile_validate])
    trainer_email = models.EmailField("Почта", blank=True)
    time_create = models.DateTimeField("Регистрация", auto_now=True)
    photo = models.ImageField(upload_to="personnel/", default=None, null=True, blank=True, verbose_name='Фото')


    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

class Administratorsclass(models.Model):
    admins = models.ForeignKey(Personnel, on_delete=models.PROTECT, null=True,
                                      blank=True, verbose_name='Администратор')

    def __str__(self):
        return f'{self.admins}'

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

class Timetable(models.Model):
    day = models.CharField("День недели", max_length=12)
    administrator = models.ForeignKey(Administratorsclass, on_delete=models.PROTECT, null=True,
                                      blank=True, verbose_name='Администратор')
    trainer_day = models.ForeignKey(Trainer, on_delete=models.PROTECT, null=True,
                                    blank=True, verbose_name='Дежурный тренер')
    def __str__(self):
        return f'{self.day}'

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"

class Product(models.Model):
    product = models.CharField("Товар", max_length=30)
    amount = models.CharField("Количество", max_length=30)
    price = models.CharField("Цена, руб.", max_length=30)

    def __str__(self):
        return f'{self.product} - {self.price}руб.'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Sales(models.Model):
    who_ad = models.ForeignKey(Administratorsclass, on_delete=models.PROTECT, null=True,
                                      blank=True, verbose_name='Администратор продал')
    who_tr = models.ForeignKey(Trainer, on_delete=models.PROTECT, null=True,
                                      blank=True, verbose_name='Тренер продал')
    what = models.ForeignKey(Product, on_delete=models.PROTECT, null=True,
                                      blank=True, verbose_name='Какой товар продан')
    when = models.DateField(default=None, null=True, blank=True, verbose_name='День продажи')

    def __str__(self):
        return f'{self.who_ad} {self.who_tr} {self.what}'

    class Meta:
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"


class Client(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    DAY = 'D'
    EVENING = 'E'
    FREE = 'F'
    EXPIRED = 'X'
    NO = 'N'
    ABONNEMENT = [
        (DAY, 'Дневной'),
        (EVENING, 'Вечерний'),
        (FREE, 'Свободный'),
        (EXPIRED, 'Истёк'),
        (NO, 'Нет')
    ]
    full_name = models.CharField("ФИО", max_length=40)
    gender = models.CharField("Пол", max_length=1, choices=GENDER, default=MALE)
    age = models.IntegerField("Возраст", null=True)
    phone = models.CharField("Телефон", max_length=12, validators=[mobile_validate])
    client_email = models.EmailField("Почта", blank=True)
    time_create = models.DateTimeField("Регистрация", auto_now=True)
    abonnement = models.CharField("Абонемент", max_length=1, choices=ABONNEMENT, default=" ",)
    date_ab = models.DateField(default=None, null=True, blank=True, verbose_name='Срок действия абонемента')
    trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Тренер')

    def __str__(self):
        return f'{self.full_name} - {self.phone}, {self.gender}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Stock(models.Model):
    name = models.CharField("Название", max_length=100)
    about_stock = models.TextField("Описание", max_length=2200, blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    date_ac = models.DateField(default=None, null=True, blank=True, verbose_name='Срок окончания акции')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Stock, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('slug-name', args=[self.slug])

    def __str__(self):
        return f'{self.name} {self.date_ac}'

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

class Abonnement(models.Model):
    abonnement = models.CharField("Абонемент", max_length=100)
    time = models.CharField("Время посещения", max_length=100)
    price = models.IntegerField("Цена, руб.", null=True, blank=True)

    def __str__(self):
        return f'{self.abonnement} {self.time} {self.price}'

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"