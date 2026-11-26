from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume", "cover_letter"]
        labels = {"resume": "Resume (optional - your profile resume is used if empty)"}
        widgets = {"cover_letter": forms.Textarea(attrs={"rows": 5})}
