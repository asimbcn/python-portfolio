from django.shortcuts import render
from .models import User, UserProfile, Work, Education, Project

# Create your views here.
def index(request):
    user = User.objects.get(active = True)
    print(user)
    profile = UserProfile.objects.get(vuser = user)
    work = Work.objects.filter(user = user)
    education = Education.objects.filter(user = user)
    project = Project.objects.filter(user = user)
    print(project,work,education,project)
    return render(request,'index.html')
