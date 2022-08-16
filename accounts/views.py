import email
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .models import Account
import json
import pickle
from .predict import predict_dolulukOrani, predict_enrollment, predict_point, b2_enrollment, b2_point, enrollment_2c, predict_capacity
# from .demand import predict_demand


# json_data = open('accounts/data/data_2021.json', encoding='utf-8')  
# data1 = json.loads(json_data.read()) 
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
        ucret = request.POST['registerUcret']
        print("username: ",username)
        print("email: ",email)
        print("university: ",university)
        print("password: ",password)
        print("password: ",ucret)
        if password == password2:
            if not Account.objects.filter(username=username).exists():
                user = Account.objects.create_user(username, email, password)
                user.university = university
                user.ucret = ucret
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

def yeniBolumForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        fakulte = request.POST["fakulte"]
        kontenjan = request.POST["kontenjan"]
        burs = request.POST["burs"]
        kriter = request.POST["kriter"]
        top_n = request.POST["top-n"]
        # print("fakulte: ",fakulte)
        # print("kontenjan: ",kontenjan)
        # print("kriter: ",kriter)
        # print("top_n: ",top_n)
        fakulte = fakulte.replace('%', '')
        burs = burs.replace('%', '')
        if kriter == "1":
            tahmin = "Yerleştirme"
            result = predict_enrollment(fakulte, burs, kontenjan)
            result = result.groupby(['bolum']).mean().sort_values(by=['predict'], ascending=False)
            result = result.iloc[:int(top_n)]
            bolums = []
            results = []
            for i, row in result.iterrows():
                results.append(round(row[0]))
                bolums.append(row.name.replace('bolum_', ''))
            # print(bolums)
            # print(results)
            return render(request, 'accounts/resultYeniBolum.html', {"user":user, "fakulte": fakulte, "burs":burs, "tahmin":tahmin, "results": results, "bolums": bolums})
        if kriter == "2":
            tahmin = "Gelir"
            result = predict_enrollment(fakulte, burs, kontenjan)
            result = result.groupby(['bolum']).mean().sort_values(by=['predict'], ascending=False)
            result = result.iloc[:int(top_n)]
            bolums = []
            results = []
            try: ucret = request.user.ucret
            except: ucret = 0
            for i, row in result.iterrows():
                results.append(round(row[0])*request.user.ucret)
                bolums.append(row.name.replace('bolum_', ''))
            return render(request, 'accounts/resultYeniBolum.html', {"user":user, "fakulte": fakulte, "burs":burs, "tahmin":tahmin, "results": results, "bolums": bolums})
        if kriter == "3":
            tahmin = "Taban Puanı"
            result = predict_point(fakulte, burs, kontenjan)
            print(result)
            result = result.groupby(['bolum']).mean().sort_values(by=['predict'], ascending=False)
            result = result.iloc[:int(top_n)]
            bolums = []
            results = []
            for i, row in result.iterrows():
                results.append(round(row[0],3))
                bolums.append(row.name.replace('bolum_', ''))
            return render(request, 'accounts/resultYeniBolum.html', {"user":user, "fakulte": fakulte, "burs":burs, "tahmin":tahmin, "results": results, "bolums": bolums})
        # return render(request, 'accounts/resultYeniBolum.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/yeniBolumForm.html', {"user":user, "university": university})


def istatistikForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        fakulte = request.POST["fakulte"]
        bolum = request.POST["bolum"]
        kontenjan = request.POST["kontenjan"]
        istatistik = request.POST["istatistik"]
        print("fakulte: ",fakulte)
        print("bolum: ",bolum)
        print("kontenjan: ",kontenjan)
        print("istatistik: ",istatistik)
        if istatistik == '1':
            tahmin_name = "Yerleştirme"
            result = b2_enrollment(fakulte, bolum, kontenjan)
            result = round(result)
            print(result)
            return render(request, 'accounts/resultIstatistik.html', {"user":user, "fakulte": fakulte, "bolum":bolum, "tahmin_name":tahmin_name, "result": result, "kontenjan": kontenjan})
        elif istatistik == '2':
            tahmin_name = "Gelir"
            result = b2_enrollment(fakulte, bolum, kontenjan)
            try: ucret = request.user.ucret
            except: ucret = 0
            result = round(result)*ucret
            print(result)
            return render(request, 'accounts/resultIstatistik.html', {"user":user, "fakulte": fakulte, "bolum":bolum, "tahmin_name":tahmin_name, "result": result, "kontenjan": kontenjan})
        elif istatistik == '3':
            tahmin_name = "Taban Puan"
            result = b2_point(fakulte, bolum, kontenjan)
            result = round(result, 3)
            print(result)
            return render(request, 'accounts/resultIstatistik.html', {"user":user, "fakulte": fakulte, "bolum":bolum, "tahmin_name":tahmin_name, "result": result, "kontenjan": kontenjan})
        # return render(request, 'accounts/resultYeniBolum.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/istatistikForm.html', {"user":user, "university": university})


def yerlestirmeForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        fakulte = request.POST["fakulte"]
        bolum = request.POST["bolum"]
        print("fakulte: ",fakulte)
        print("bolum: ",bolum)
        result = enrollment_2c(university, fakulte, bolum)
        result = str(result).replace('[', '').replace(']', '')
        print(result)
        result = round(float(result))
        return render(request, 'accounts/resultYerlestirme.html', {"user":user, "fakulte": fakulte, "bolum":bolum, "university":university, "result": result})
        # return render(request, 'accounts/resultYeniBolum.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/yerlestirmeForm.html', {"user":user, "university": university})


def dolulukOraniForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        universite = request.user.university
        bolum = request.POST["bolum"]
        print("bolum: ",bolum)
        fakulte = request.POST["fakulte"]
        print("fakulte: ",fakulte)
        print("bolum: ",bolum)
        print("universite: ",universite)
        # print(data1)
        # data1_dict = [x for x in data1 if x[0] == bolum and x[2] == universite]
        # print(data1_dict)
        try:
            result = predict_dolulukOrani(bolum, universite)
            result = int(100*result)
        except: result = "Bulunamadı"
        
        return render(request, 'accounts/resultDolulukOrani.html', {'bolum':bolum, 'fakulte':fakulte, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/dolulukOraniForm.html', {"user":user, "university": university})





def kontenjanForm(request):
    user = request.user
    university = request.user.university
    if request.method == 'POST':
        fakulte = request.POST["fakulte"]
        bolum = request.POST["bolum"]
        tabanPuani = request.POST["tabanPuani"]
        yerlesme = request.POST["yerlesme"]
        print("fakulte: ",fakulte)
        print("bolum: ",bolum)
        print("tabanPuani: ",tabanPuani)
        print("yerlesme: ",yerlesme)
        result = predict_capacity(university, fakulte, bolum, tabanPuani, yerlesme )
        result = str(result).replace('[', '').replace(']', '').replace('.', '')
        return render(request, 'accounts/resultKontenjan.html', {'bolum':bolum, 'fakulte':fakulte, 'universite':university, 'result':result, 'tabanPuani':tabanPuani, 'yerlesme':yerlesme})
        # return render(request, 'accounts/resultYeniBolum.html', {'bolum':bolum, 'universite':universite, 'result':result})
    print("GET")
    return render(request, 'accounts/kontenjanForm.html', {"user":user, "university": university})











