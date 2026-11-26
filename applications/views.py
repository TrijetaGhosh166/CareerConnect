from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import SeekerProfile
from jobs.models import Job
from .forms import ApplicationForm
from .models import Application


def _role(user):
    return user.profile.role if hasattr(user, "profile") else None


@login_required
def apply(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    if _role(request.user) != "seeker":
        messages.error(request, "Only job seekers can apply.")
        return redirect("job_detail", job_id=job.id)
    if job.applications.filter(applicant=request.user).exists():
        messages.info(request, "You have already applied for this job.")
        return redirect("application_status")
    seeker, _ = SeekerProfile.objects.get_or_create(user=request.user)
    if not seeker.is_complete:
        messages.warning(request, "Please complete your profile (CGPA, field and Skill 1) before applying.")
        return redirect("edit_profile")
    form = ApplicationForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        application = form.save(commit=False)
        application.job = job
        application.applicant = request.user
        application.save()
        messages.success(request, "Application submitted!")
        return redirect("application_status")
    return render(request, "applications/apply.html", {"form": form, "job": job, "seeker": seeker})


@login_required
def application_status(request):
    if _role(request.user) == "recruiter":
        jobs = request.user.posted_jobs.annotate(n=Count("applications"))
        return render(request, "applications/status.html", {"role": "recruiter", "jobs": jobs})
    applications = request.user.applications.select_related("job")
    return render(request, "applications/status.html", {"role": "seeker", "applications": applications})


@login_required
def applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = job.applications.select_related("applicant__seeker_profile", "applicant__profile")
    return render(request, "applications/applicants.html", {
        "job": job,
        "applications": applications,
        "status_choices": Application.STATUS_CHOICES,
    })


@login_required
def update_status(request, application_id):
    application = get_object_or_404(Application, id=application_id, job__recruiter=request.user)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, "Status updated.")
    return redirect("applicants", job_id=application.job.id)
