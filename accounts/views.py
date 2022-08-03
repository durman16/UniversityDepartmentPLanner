import email
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User


# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST['loginName']
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user is not None:
            login(request)
            return render(request, 'accounts/home.html')
        else:
            messages.error(request, "Kullanıcı adı veya Şifre hatalı!")
            return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/home.html')

def login(request):
    return render(request, 'accounts/login.html')
def logout_view(request):
    logout(request)
    return render(request, 'accounts/home.html')
def register(request):
    if request.method == 'POST':
        username = request.POST['registerUsername']
        email = request.POST['registerEmail']
        university = request.POST.get('registerUniversity')
        password = request.POST['registerPassword']
        password2 = request.POST['registerRepeatPassword']
        print("username: ",username)
        print("email: ",email)
        print("university: ",university)
        print("password: ",password)
        if password == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, email, password)
                user.university = university
                user.save()
                messages.success(request, "Kullanıcı oluşturuldu!")
            else:
                messages.error(request, "Kullanıcı adı kullanılıyor!")
        else:
            messages.error(request, "Parola eşleşmiyor!")
    return render(request, 'accounts/login.html')
def menu(request):
    if request.method == 'POST':
        username = request.POST['loginName']
        password = request.POST.get('loginPassword')
        user = authenticate(username=username, password=password)
        print(username)
        print(password)
        print(user)
        if user is not None:
            login(request, user)
            return render(request, 'base/menu.html')
        else:
            messages.error(request, "Kullanıcı adı veya Şifre hatalı!")
            return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/menu.html')

