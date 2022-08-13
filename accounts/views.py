import email
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .models import Account
import json
import pickle
from .predict import predict_capacity
from .demand import predict_demand




model = pickle.load(open('accounts/model.pkl', 'rb'))
json_data = open('accounts/data_2021.json', encoding='utf-8')  
data1 = json.loads(json_data.read()) 
# data2 = json.dumps(json_data) 
def home(request):
    if request.method == 'POST':
        username = request.POST['loginName']
        password = request.POST.get('loginPassword')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return render(request, 'accounts/menu.html', {})
        else:
            messages.error(request, "Kullanıcı adı veya Şifre hatalı!")
            return render(request, 'accounts/login.html', {})
    if request.user.is_authenticated:
        return render(request, 'accounts/menu.html', {})
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
        # print("username: ",username)
        # print("email: ",email)
        # print("university: ",university)
        # print("password: ",password)
        if password == password2:
            if not Account.objects.filter(username=username).exists():
                user = Account.objects.create_user(username, email, password)
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
        # print(username)
        # print(password)
        # print(user)
        if user is not None:
            login(request, user)
            return render(request, 'base/menu.html')
        else:
            messages.error(request, "Kullanıcı adı veya Şifre hatalı!")
            return render(request, 'accounts/login.html', {})
    return render(request, 'accounts/menu.html')
def dolulukOraniForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        universite = request.user.university
        bolum = request.POST["bolum"]
        print("bolum: ",bolum)
        print("universite: ",universite)
        # print(data1)
        data1_dict = [x for x in data1 if x[0] == bolum and x[2] == universite]
        print(data1_dict)
        try: result = predict_capacity(bolum, universite)
        except: result = "Bulunamadı"
        result = int(100*result)
        return render(request, 'accounts/resultOgrenimUcreti.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/dolulukOraniForm.html', {"user":user, "university": university})
def yeniprogramForm(request):
    if request.method == 'POST':
        user = request.user
    return render(request, 'accounts/yeniprogramForm.html')
    
def demandForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        universite = request.user.university
        bolum = request.POST["bolum"]
        print("bolum: ",bolum)
        print("universite: ",universite)
        # print(data1)
        data1_dict = [x for x in data1 if x[0] == bolum and x[2] == universite]
        print(data1_dict)
        try: result = predict_demand(bolum, universite)
        except: result = "Bulunamadı"
        return render(request, 'accounts/resultDemand.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/demandForm.html', {"user":user, "university": university})


def resultOgrenimUcreti(request):
    if request.method == 'POST':
        user = request.user
    return render(request, 'accounts/resultOgrenimUcreti.html')

