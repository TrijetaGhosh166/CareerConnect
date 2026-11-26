from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import RecruiterProfile, SeekerProfile


class RegisterForm(UserCreationForm):
    """Same form for Job Seeker and Recruiter."""
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField()
    phone = forms.CharField(label="Mobile number", max_length=15)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "phone", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = SeekerProfile
        exclude = ["user"]
        widgets = {
            "job_description": forms.Textarea(attrs={"rows": 3}),
            "achievements": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("cgpa", "field_of_study", "skill_1"):
            self.fields[name].required = True


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        exclude = ["user"]
        widgets = {"job_description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("company_name", "job_domain", "contact_details"):
            self.fields[name].required = True
