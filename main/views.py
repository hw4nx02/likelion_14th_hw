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
    new_post.writer = request.user
    new_post.category = request.POST["category"]
    new_post.content = request.POST["content"]

    if "image" in request.FILES:
        new_post.image = request.FILES["image"]

    new_post.save()
    save_tags(new_post)

    return redirect("main:post_detail", new_post.id)

def post_detail(request, post_id, edit_comment=-1):
    post = get_object_or_404(Post, pk=post_id)

    # 댓글 작성 (POST)
    # 로그인 사용자의 경우
    if request.user.is_authenticated:
        if request.method == "POST":
            new_comments = Comment() # Comment 객체 생성

            # Comment 객체 채우기
            new_comments.post = post
            new_comments.writer = request.user
            new_comments.content = request.POST["content"]

            new_comments.save()
            return redirect("main:post_detail", post_id)

    # 댓글 확인 (GET)
    comments = Comment.objects.filter(post=post)
    return render(request, "main/post_detail.html", {"post": post, "comments": comments, "edit_comment": edit_comment})

def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    edit_post = get_object_or_404(Post, pk=post_id)

    if edit_post.writer != request.user:
        return redirect("main:post_detail", edit_post.id)

    return render(request, "main/edit_post.html", {"post": edit_post})

def update_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    update_post = get_object_or_404(Post, pk=post_id)

    if update_post.writer != request.user:
        return redirect("main:post_detail", update_post.id)

    update_post.title = request.POST["title"]
    update_post.writer = request.user
    update_post.category = request.POST["category"]
    update_post.content = request.POST["content"]

    if "image" in request.FILES:
        update_post.image = request.FILES["image"]

    update_post.save()
    save_tags(update_post)

    return redirect("main:post_detail", update_post.id)

def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    delete_post = get_object_or_404(Post, pk=post_id)

    if delete_post.writer != request.user:
        return redirect("main:post_detail", delete_post.id)

    delete_post.delete()

    return redirect("main:blog")

def edit_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    edit_comment = get_object_or_404(Comment, pk=comment_id)

    if edit_comment.writer != request.user:
        return redirect("main:post_detail", edit_comment.post.id)
    
    return redirect("main:post_detail", edit_comment.post.id, edit_comment.id)

def update_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    update_comment = get_object_or_404(Comment, pk=comment_id)

    if update_comment.writer != request.user:
        return redirect("main:post_detail", update_comment.post.id)
    
    update_comment.content = request.POST["content"]
    update_comment.save()

    return redirect("main:post_detail", update_comment.post.id)

def delete_comment(request, comment_id):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    
    delete_comment = get_object_or_404(Comment, pk=comment_id)
    target_post = delete_comment.post

    if delete_comment.writer != request.user:
        return redirect("main:post_detail", target_post.id)
    
    delete_comment.delete()

    return redirect("main:post_detail", target_post.id)

def save_tags(post):
    words = post.content.split()
    tag_list = []

    for w in words:
        if len(w) > 0:
            if w[0] == "#":
                tag_list.append(w[1:])

    post.tags.clear()

    for t in tag_list:
        tag, boolean = Tag.objects.get_or_create(name=t)
        post.tags.add(tag)

def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "main/tag_list.html", {"tags": tags})

def tag_post_list(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = tag.posts.all()
    return render(request, "main/tag_post_list.html", {"tag": tag, "posts": posts})

# 게시물 좋아요 클릭 처리
def post_likes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    
    return redirect("main:post_detail", post.id)

# 댓글 좋아요 클릭 처리
def comment_likes(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    target_post = comment.post

    if request.user in comment.like.all():
        comment.like.remove(request.user)
        comment.like_count -= 1
        comment.save()
    else:
        comment.like.add(request.user)
        comment.like_count += 1
        comment.save()

    return redirect("main:post_detail", target_post.id)