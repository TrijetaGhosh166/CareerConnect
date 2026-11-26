from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobForm
from .models import Job


def is_recruiter(user):
    return user.is_authenticated and hasattr(user, "profile") and user.profile.role == "recruiter"


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    q = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    if q:
        jobs = jobs.filter(Q(title__icontains=q) | Q(company__icontains=q) | Q(domain__icontains=q) | Q(skills_required__icontains=q))
    if location:
        jobs = jobs.filter(location__icontains=location)
    return render(request, "jobs/list.html", {"jobs": jobs, "q": q, "location": location})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = job.applications.filter(applicant=request.user).exists()
    return render(request, "jobs/detail.html", {"job": job, "already_applied": already_applied})


@login_required
def post_job(request):
    if not is_recruiter(request.user):
        messages.error(request, "Only recruiters can post jobs.")
        return redirect("jobs")
    form = JobForm(request.POST or None, initial={"company": getattr(getattr(request.user, "recruiter_profile", None), "company_name", "")})
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.recruiter = request.user
        job.save()
        messages.success(request, "Job posted.")
        return redirect("my_jobs")
    return render(request, "jobs/form.html", {"form": form})


@login_required
def my_jobs(request):
    if not is_recruiter(request.user):
        return redirect("jobs")
    jobs = request.user.posted_jobs.all()
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted.")
    return redirect("my_jobs")
