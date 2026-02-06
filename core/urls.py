from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed, name="feed"),
    path("cadastro/", views.cadastro, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("criar/", views.criar_post, name="create_post"),
    path("curtir/<int:post_id>/", views.curtir_post, name="like_post"),
]
