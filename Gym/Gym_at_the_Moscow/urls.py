from .import views
from django.urls import path


urlpatterns = [
    path('', views.show_info, name='home'),
    path('abonnement/', views.abon_func, name='abon-name'),
    path('hall/', views.hall_func, name='hall-name'),
    path('trainer/', views.trainer_func, name='trainer-name'),
    path('stock/', views.stock_func, name='stock-name'),
    path('trainer/<slug:slug_trainer>', views.slug_func, name='slug-name'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]