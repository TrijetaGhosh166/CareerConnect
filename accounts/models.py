from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Common data for every user: role + mobile number."""
    ROLE_CHOICES = [("seeker", "Job Seeker"), ("recruiter", "Recruiter")]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class SeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seeker_profile")
    institution = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=100, blank=True)
    cgpa = models.DecimalField("Marks / CGPA", max_digits=5, decimal_places=2, null=True, blank=True)
    field_of_study = models.CharField("Field", max_length=100, blank=True)
    experience_years = models.DecimalField("Experience (years)", max_digits=4, decimal_places=1, null=True, blank=True)
    company_name = models.CharField(max_length=150, blank=True)
    job_description = models.TextField(blank=True)
    skill_1 = models.CharField("Skill 1", max_length=80, blank=True)
    skill_2 = models.CharField("Skill 2", max_length=80, blank=True)
    skill_3 = models.CharField("Skill 3", max_length=80, blank=True)
    preferred_language = models.CharField(max_length=100, blank=True)
    achievements = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)

    @property
    def is_complete(self):
        return self.cgpa is not None and bool(self.field_of_study) and bool(self.skill_1)

    def skills(self):
        return [s for s in (self.skill_1, self.skill_2, self.skill_3) if s]

    def __str__(self):
        return f"Seeker: {self.user.username}"


class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    company_name = models.CharField(max_length=150, blank=True)
    job_domain = models.CharField(max_length=100, blank=True)
    job_description = models.TextField("Description of job", blank=True)
    contact_details = models.CharField(max_length=250, blank=True)
    google_form_link = models.URLField("Link of personal Google Form", blank=True)

    @property
    def is_complete(self):
        return bool(self.company_name and self.job_domain and self.contact_details)

    def __str__(self):
        return f"Recruiter: {self.user.username}"
