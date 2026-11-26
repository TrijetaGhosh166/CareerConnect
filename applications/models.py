from django.contrib.auth.models import User
from django.db import models

from jobs.models import Job


class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("reviewed", "Reviewed"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="applications/", blank=True)  # optional: falls back to profile resume
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "applicant")
        ordering = ["-applied_at"]

    @property
    def resume_file(self):
        if self.resume:
            return self.resume
        sp = getattr(self.applicant, "seeker_profile", None)
        return sp.resume if sp and sp.resume else None

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"
