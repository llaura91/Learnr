from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post


def feed(request):
    posts = Post.objects.all().order_by("-criado_em")
    return render(request, "feed.html", {"posts": posts})


def cadastro(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "cadastro.html", {"erro": "User already exists"})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("feed")

    return render(request, "cadastro.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("feed")
        else:
            return render(request, "login.html", {"erro": "Invalid login"})

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def criar_post(request):
    if request.method == "POST":
        texto = request.POST["texto"]
        Post.objects.create(autor=request.user, texto=texto)
        return redirect("feed")

    return render(request, "criar_post.html")


@login_required
def curtir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.curtidas.all():
        post.curtidas.remove(request.user)
    else:
        post.curtidas.add(request.user)

    return redirect("feed")

@login_required
def excluir_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.autor:
        post.delete()
        return redirect("feed")
    else:
        return render(request, "feed.html", {"erro": "You cannot delete this post."})