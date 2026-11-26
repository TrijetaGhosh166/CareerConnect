from django.contrib.auth.models import User
from django.db import models


class Job(models.Model):
    TYPE_CHOICES = [("full", "Full-time"), ("part", "Part-time"), ("intern", "Internship"), ("contract", "Contract")]

    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_jobs")
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    domain = models.CharField("Hiring domain", max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="full")
    salary = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    skills_required = models.CharField(max_length=250, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} at {self.company}"
