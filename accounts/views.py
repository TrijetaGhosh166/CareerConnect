from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import RecruiterProfileForm, RegisterForm, SeekerProfileForm
from .models import Profile, RecruiterProfile, SeekerProfile


def registration(request):
    """Step 1: choose a role."""
    if request.method == "POST":
        role = request.POST.get("role")
        if role in ("seeker", "recruiter"):
            return redirect("register", role=role)
        messages.error(request, "Please choose a role.")
    return render(request, "accounts/registration.html")


def register(request, role):
    """Step 2: same form for both roles. Saves User + Profile, then goes to Home."""
    if role not in ("seeker", "recruiter"):
        return redirect("registration")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.first_name = form.cleaned_data["first_name"]
        user.last_name = form.cleaned_data["last_name"]
        user.email = form.cleaned_data["email"]
        user.save()
        Profile.objects.create(user=user, role=role, phone=form.cleaned_data["phone"])
        if role == "seeker":
            SeekerProfile.objects.create(user=user)
        else:
            RecruiterProfile.objects.create(user=user)
        auth_login(request, user)
        messages.success(request, "Welcome to CareerConnect! Please complete your profile.")
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form, "role": role})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("home")  # always land on Home
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("home")


@login_required
def edit_profile(request):
    if not hasattr(request.user, "profile"):
        return redirect("home")
    role = request.user.profile.role
    if role == "seeker":
        instance, _ = SeekerProfile.objects.get_or_create(user=request.user)
        form_class = SeekerProfileForm
    else:
        instance, _ = RecruiterProfile.objects.get_or_create(user=request.user)
        form_class = RecruiterProfileForm
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("home")
    return render(request, "accounts/edit_profile.html", {"form": form, "role": role})
