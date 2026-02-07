from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Post, Seguidor, Comentario, Perfil


def feed(request):
    posts = Post.objects.all().order_by("-criado_em")
    return render(request, "feed.html", {"posts": posts})


def cadastro(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "cadastro.html", {"erro": "Username taken"})

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
def seguir_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    if usuario != request.user:
        relacao = Seguidor.objects.filter(seguidor=request.user, seguindo=usuario)

        if relacao.exists():
            relacao.delete()
        else:
            Seguidor.objects.create(seguidor=request.user, seguindo=usuario)

    return redirect("profile", user_id=user_id)


def perfil(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(autor=usuario).order_by("-criado_em")

    seguidores = Seguidor.objects.filter(seguindo=usuario).count()
    seguindo = Seguidor.objects.filter(seguidor=usuario).count()

    seguindo_usuario = False
    if request.user.is_authenticated:
        seguindo_usuario = Seguidor.objects.filter(
            seguidor=request.user,
            seguindo=usuario
        ).exists()

    perfil, _ = Perfil.objects.get_or_create(usuario=usuario)

    context = {
        "usuario": usuario,
        "perfil": perfil,
        "posts": posts,
        "seguidores": seguidores,
        "seguindo": seguindo,
        "seguindo_usuario": seguindo_usuario,
    }

    return render(request, "perfil.html", context)


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        bio = request.POST.get("bio", "")
        perfil.bio = bio

        perfil.save()
        return redirect("profile", user_id=request.user.id)

    context = {"perfil": perfil}
    return render(request, "editar_perfil.html", context)


@login_required
def comentar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        texto = request.POST["texto"]
        Comentario.objects.create(
            autor=request.user,
            post=post,
            texto=texto
        )

    return redirect("feed")
