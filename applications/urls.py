from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.application_status, name="application_status"),
    path("apply/<int:job_id>/", views.apply, name="apply"),
    path("job/<int:job_id>/applicants/", views.applicants, name="applicants"),
    path("update/<int:application_id>/", views.update_status, name="update_status"),
]
