from django.db.models import Count
from django.shortcuts import render

from accounts.models import RecruiterProfile, SeekerProfile
from jobs.models import Job


def home(request):
    ctx = {"jobs": Job.objects.filter(is_active=True)[:9]}
    user = request.user
    if user.is_authenticated and hasattr(user, "profile"):
        ctx["role"] = user.profile.role
        if user.profile.role == "seeker":
            ctx["seeker"], _ = SeekerProfile.objects.get_or_create(user=user)
            ctx["applications"] = user.applications.select_related("job")[:5]
        else:
            ctx["recruiter"], _ = RecruiterProfile.objects.get_or_create(user=user)
            ctx["my_jobs"] = user.posted_jobs.annotate(n=Count("applications"))
    return render(request, "core/home.html", ctx)


def about(request):
    return render(request, "core/about.html")
