from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.messages import get_messages
from django.shortcuts import render, redirect
from .models import Profile

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("main:blog")
        else:
            return render(request, "accounts/login.html")
        
    elif request.method == "GET":
        return render(request, "accounts/login.html")
    
def logout(request):
    auth.logout(request)
    return redirect("main:blog")

def signup(request):
    if request.method == "POST":
        existed_users = Profile.objects.filter(user__username=request.POST["username"])
        storage = get_messages(request)
        storage.used = True

        if existed_users.count() > 0:
            messages.add_message(request, messages.INFO, "이미 존재하는 회원 이름(아이디)입니다!")
            return render(request, "accounts/signup.html")

        if request.POST["password"] != request.POST["confirm"]:
            messages.add_message(request, messages.INFO, "비밀번호 확인이 일치하지 않습니다.")
            return render(request, "accounts/signup.html")

        new_user = User.objects.create_user(
            username=request.POST["username"],
            password=request.POST["password"]
        )

        profile = new_user.profile
        profile.nickname = request.POST["nickname"]
        profile.age = request.POST["age"]
        profile.major = request.POST["major"]
        profile.profile_image = request.FILES.get("profile_image")
        profile.save()
        
        auth.login(request, new_user)
        return redirect("main:blog")
    
    return render(request, "accounts/signup.html")