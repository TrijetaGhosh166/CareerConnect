from django.urls import path
from . import views

urlpatterns = [
    path("", views.job_list, name="jobs"),
    path("post/", views.post_job, name="post_job"),
    path("mine/", views.my_jobs, name="my_jobs"),
    path("<int:job_id>/", views.job_detail, name="job_detail"),
    path("<int:job_id>/delete/", views.delete_job, name="delete_job"),
]
