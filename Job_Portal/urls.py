from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from MdMostafizurRahman_08_Jobportal import settings
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_manage_view, name='profile_manage'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('apply-job/<int:job_id>/', views.apply_job_view, name='apply_job'),
    path('skill-match/', views.skill_match_view, name='skill_match'),
    path('job/edit/<int:job_id>/', views.edit_job_view, name='edit_job'),
    path('job/delete/<int:job_id>/', views.delete_job_view, name='delete_job'),
    path('job/applicants/<int:job_id>/', views.job_applicants_view, name='job_applicants'),
    path('job/<int:pk>/', views.job_detail_view, name='job_detail'),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)