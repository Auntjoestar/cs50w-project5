from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/<int:user>", views.profile, name="profile"),
    path("picture/edit", views.change_picture, name="change_picture"),
    path("profile/edit", views.change_profile, name="change_profile"),
]