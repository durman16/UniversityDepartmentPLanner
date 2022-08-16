from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login/', views.login),
    path('logout/', views.logout_view),
    path('menu', views.menu),
    path('dolulukOraniForm/', views.dolulukOraniForm, name="dolulukOraniForm"),
    path('yeniBolumForm/', views.yeniBolumForm, name="yeniBolumForm"),
    path('istatistikForm/', views.istatistikForm, name="istatistikForm"),
    path('yerlestirmeForm/', views.yerlestirmeForm, name="yerlestirmeForm"),
    path('kontenjanForm/', views.kontenjanForm, name="kontenjanForm"),

]