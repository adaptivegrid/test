from django.contrib import admin
from .models import Client, Trainer, Personnel, Timetable, Product, Sales, Administratorsclass, Stock, Abonnement
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

#admin.site.register(Trainer)


class AgeFilter(admin.SimpleListFilter):
    """
    Создаем справа отдельный блок: фильтр по возрасту
    """

    title = 'Фильтр по возрасту'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return [
            ('<23', '18-23'),
            ('от 23 до 27', '23-27'),
            ('от 28 до 35', '28-35'),
            ('от 36 до 49', '36-49'),
            ('>=50', '>50'),
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<23':
            return queryset.filter(age__lt=23)
        if self.value() == 'от 23 до 27':
            return queryset.filter(age__gte=23).filter(age__lt=28)
        if self.value() == 'от 28 до 35':
            return queryset.filter(age__gte=28).filter(age__lt=36)
        if self.value() == 'от 36 до 49':
            return queryset.filter(age__gte=36).filter(age__lt=50)
        if self.value() == '>=50':
            return queryset.filter(age__gte=50)
        return queryset


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    #exclude = ['slug'] # исключить при добавлении нового клиента
    list_display = ['full_name', 'abonnement', 'date_ab', 'trainer', 'phone', 'gender', 'age'] # вывод столбцов
    list_editable = ['abonnement', 'date_ab', 'trainer'] # изменение записей
    search_fields = ['full_name', 'phone'] # поиск по имени
    list_filter = [AgeFilter, 'gender'] # фильтр сбоку
    #readonly_fields = ['age', 'date', 'trainer'] - нельзя редактировать поля
    ordering = ['full_name'] # сортировка по имени
    list_per_page = 10 # количество строк на странице

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'age', 'get_photo']
    prepopulated_fields = {"slug": ("full_name", )}

    def get_photo(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50" height="60"')

    get_photo.short_description = "Фото"

@admin.register(Personnel)
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ['position_gym', 'full_name', 'phone', 'age', 'get_photo']
    search_fields = ['full_name', 'phone']
    list_filter = ['position_gym']


    def get_photo(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="50" height="50"')

    get_photo.short_description = "Фото"

@admin.register(Administratorsclass)
class AdministratorsclassAdmin(admin.ModelAdmin):
    list_display = ['admins']

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['day', 'administrator', 'trainer_day']
    list_editable = ['administrator', 'trainer_day']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount', 'price']
    list_editable = ['amount', 'price']


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['who_ad', 'who_tr', 'what', 'when']
    list_editable = ['who_tr', 'what', 'when']
    list_filter = ['who_ad', 'who_tr']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_ac']
    prepopulated_fields = {"slug": ("name", )}

@admin.register(Abonnement)
class AbonnementAdmin(admin.ModelAdmin):
    list_display = ['abonnement', 'time', 'price']

