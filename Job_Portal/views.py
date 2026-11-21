from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserProfileForm, JobPostForm
from .models import UserProfile, Job, JobApplication
from django.db.models import Q


@login_required
def dashboard_view(request):
  query = request.GET.get('q', '')
  jobs = Job.objects.all()

  if query:
    jobs = jobs.filter(
        Q(title__icontains=query)
        | Q(company_name__icontains=query)
        | Q(category__icontains=query)
        | Q(skills_set__icontains=query)
        | Q(job_description__icontains=query)
    )

  if hasattr(request.user, 'userprofile') and request.user.userprofile.user_type == 'recruiter':
    jobs = Job.objects.filter(recruiter=request.user)
    if query:
      jobs = jobs.filter(
          Q(title__icontains=query)
          | Q(company_name__icontains=query)
          | Q(category__icontains=query)
          | Q(skills_set__icontains=query)
          | Q(job_description__icontains=query)
      )

  context = {
      'jobs': jobs,
      'query': query,
  }
  return render(request, 'dashboard.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            UserProfile.objects.create(
                user=user,
                display_name=form.cleaned_data['display_name'],
                user_type=form.cleaned_data['user_type']
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    profile = request.user.userprofile
    context = {'profile': profile}
    
    if profile.user_type == 'recruiter':
        jobs = Job.objects.filter(recruiter=request.user)
        context['jobs'] = jobs
    else:
        
        query = request.GET.get('q', '')
        if query:
            jobs = Job.objects.filter(
                Q(skills_set__icontains=query) |
                Q(title__icontains=query) |
                Q(company_name__icontains=query) |
                Q(job_description__icontains=query)
            )
        else:
            jobs = Job.objects.all()
        context['jobs'] = jobs
        context['query'] = query
        context['applied_jobs'] = JobApplication.objects.filter(jobseeker=request.user).values_list('job_id', flat=True)
        
    return render(request, 'dashboard.html', context)

@login_required
def profile_manage_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile_manage.html', {'form': form})

@login_required
def post_job_view(request):
    if request.user.userprofile.user_type != 'recruiter':
        messages.error(request, 'Only recruiters can post jobs.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard')
    else:
        form = JobPostForm()
    return render(request, 'post_job.html', {'form': form})

@login_required
def apply_job_view(request, job_id):
    if request.user.userprofile.user_type != 'jobseeker':
        messages.error(request, 'Only jobseekers can apply for jobs.')
        return redirect('dashboard')
        
    job = get_object_or_404(Job, id=job_id)
    JobApplication.objects.get_or_create(job=job, jobseeker=request.user)
    messages.success(request, f'Successfully applied for {job.title}!')
    return redirect('dashboard')


@login_required
def skill_match_view(request):
    profile = request.user.userprofile
    context = {'profile': profile}
    
    if profile.user_type == 'jobseeker':
        
        user_skills = [skill.strip().lower() for skill in (profile.skills_set or "").split(',') if skill.strip()]
        
        
        matched_jobs = []
        all_jobs = Job.objects.all()
        for job in all_jobs:
            job_req_skills = [skill.strip().lower() for skill in job.skills_set.split(',') if skill.strip()]
            
            if any(skill in user_skills for skill in job_req_skills):
                matched_jobs.append(job)
        context['matched_jobs'] = matched_jobs
        
    elif profile.user_type == 'recruiter':
        
        recruiter_jobs = Job.objects.filter(recruiter=request.user)
        matches = []
        jobseekers = UserProfile.objects.filter(user_type='jobseeker')
        
        for job in recruiter_jobs:
            job_req_skills = [skill.strip().lower() for skill in job.skills_set.split(',') if skill.strip()]
            for seeker in jobseekers:
                seeker_skills = [skill.strip().lower() for skill in (seeker.skills_set or "").split(',') if skill.strip()]
                if any(skill in seeker_skills for skill in job_req_skills):
                    matches.append({'job': job, 'seeker': seeker})
        context['matches'] = matches
        
    return render(request, 'skill_match.html', context)


@login_required
def edit_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('dashboard')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'edit_job.html', {'form': form, 'job': job})

@login_required
def delete_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('dashboard')
    return render(request, 'delete_job.html', {'job': job})

@login_required
def job_applicants_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = JobApplication.objects.filter(job=job)
    return render(request, 'job_applicants.html', {'job': job, 'applications': applications})

@login_required
def job_detail_view(request, pk):
  job = get_object_or_404(Job, pk=pk)

  already_applied = JobApplication.objects.filter(
      job=job, jobseeker=request.user
  ).exists()

  is_owner = job.recruiter == request.user

  context = {
      'job': job,
      'already_applied': already_applied,
      'is_owner': is_owner,
  }
  return render(request, 'job_detail.html', context)