from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("register/<str:role>/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]
