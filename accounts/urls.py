from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login/', views.login),
    path('logout/', views.logout_view),
    path('dolulukOraniForm/', views.dolulukOraniForm, name="dolulukOraniForm"),
    path('yeniprogramForm/', views.yeniprogramForm),
    path('ogrenimucretiForm/', views.ogrenimucretiForm),
    path('resultOgrenimUcreti', views.resultOgrenimUcreti),
    path('menu', views.menu),
]