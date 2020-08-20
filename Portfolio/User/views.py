from django.shortcuts import render, redirect
from .models import User, UserProfile, Work, Education, Project

# Create your views here.
def index(request):
    try:
        user = User.objects.get(active = True)
        profile = UserProfile.objects.get(vuser = user)
        work = Work.objects.filter(user = user)
        education = Education.objects.filter(user = user)
        project = Project.objects.filter(user = user)
        return render(request,'index.html',{'profile':profile,'work':work,'education':education,'project':project})
    except:
        return redirect('error404')
            
def error(request):
    return render(request,'error.html')   
