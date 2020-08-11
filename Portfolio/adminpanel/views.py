from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from User.models import User, UserProfile, Work, Education, Project, Contact

# Create your views here.
def login(request):
    if request.method == 'POST':
        PASS
    return render(request,'admin/login.html')

def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            return render(request, 'admin/register.html', {'error':'Username already exists'})
        except User.DoesNotExist:
            agree =  request.POST.get('agree-term', False)
            if agree == False:
                return render(request, 'admin/register.html', {'error':'Terms and Conditions not satisfied'})
            else:    
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                if request.POST['code'] != 'code':
                    user.delete()
                    return render(request, 'admin/register.html', {'error':'Invalid Code!'})
                profile = UserProfile()
                profile.name = 'Unknown'    
                profile.email = request.POST['email']
                profile.vuser = user
                try:
                    user.save()
                    profile.save()
                    return redirect('login')
                except:
                    user.delete()
                    return render(request,'admin/register.html',{'error':'Could Not Register User'})
    else:
        return render(request,'admin/register.html')  

@login_required(login_url='login')
def index(request):
    return render(request,'admin/panel.html')        

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


