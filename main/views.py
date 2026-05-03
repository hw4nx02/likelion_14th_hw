from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def mainpage(request):
    context = {
        "isSummary": 1,
        "generation": 14,
        "welcome": "Django Basic",
    }
    return render(request, "main/mainpage.html", context)

def secondpage(request):
    context = {
        "isSummary": 0,
        "welcome": "Let Me Introduce Myself",
    }
    return render(request, "main/secondpage.html", context)

def blog(request):
    posts = Post.objects.all()

    return render(request, "main/blog.html", {"posts": posts})

def new_post(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    return render(request, "main/new_post.html")

def create_post(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    new_post = Post()

    new_post.title = request.POST["title"]
    new_post.writer = request.user.username
    new_post.category = request.POST["category"]
    new_post.content = request.POST["content"]
    new_post.pub_date = request.POST["pub_date"]

    if "image" in request.FILES:
        new_post.image = request.FILES["image"]

    new_post.save()

    return redirect("main:post_detail", new_post.id)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "main/post_detail.html", {"post": post})

def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    edit_post = get_object_or_404(Post, pk=post_id)

    if edit_post.writer != request.user.username:
        return redirect("main:detail", edit_post.id)

    return render(request, "main/edit_post.html", {"post": edit_post})

def update_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    update_post = get_object_or_404(Post, pk=post_id)

    if update_post.writer != request.user.username:
        return redirect("main:detail", update_post.id)

    update_post.title = request.POST["title"]
    update_post.writer = request.user.username
    update_post.category = request.POST["category"]
    update_post.content = request.POST["content"]
    update_post.pub_date = request.POST["pub_date"]

    if "image" in request.FILES:
        update_post.image = request.FILES["image"]

    update_post.save()

    return redirect("main:post_detail", update_post.id)

def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    delete_post = get_object_or_404(Post, pk=post_id)

    if delete_post.writer != request.user.username:
        return redirect("main:detail", delete_post.id)

    delete_post.delete()

    return redirect("main:blog")