from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "domain", "location", "job_type", "salary", "skills_required", "description"]
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}
