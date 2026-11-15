from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  USER_TYPES = [
      ('jobseeker', 'Jobseeker'),
      ('recruiter', 'Recruiter'),
  ]
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  user_type = models.CharField(max_length=20, choices=USER_TYPES, default='jobseeker')
  display_name = models.CharField(max_length=100, blank=True, null=True)

  profile_picture = models.ImageField(
      upload_to='profiles/', blank=True, null=True
  )
  phone_number = models.CharField(max_length=20, blank=True, null=True)
  location = models.CharField(max_length=100, blank=True, null=True)
  website = models.URLField(blank=True, null=True)
  bio = models.TextField(blank=True, null=True)

  company_info = models.TextField(blank=True, null=True)
  skills_set = models.TextField(blank=True, null=True)
  resume = models.FileField(upload_to='resumes/', blank=True, null=True)

  def __str__(self):
    return self.user.username

class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    number_of_openings = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    job_description = models.TextField()
    skills_set = models.CharField(max_length=255, help_text="Required skills")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker.username} applied for {self.job.title}"