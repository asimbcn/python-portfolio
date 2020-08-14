from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from User.models import User, UserProfile, Work, Education, Project, Contact

# Create your views here.
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            profile = UserProfile.objects.get(vuser = user)
            if profile.name == 'Unknown':
                return redirect('otf')
            else:    
                return redirect('index')
        else:
            try:
                user = User.objects.get(username=request.POST['username'])
                if user:
                    return render(request, 'account/login.html',{'error':'Incorrect Password'})
            except:
                return render(request, 'admin-panel/login.html',{'error':'Incorrect Username'})

        # return render(request,'admin-panel/login.html')    
    else:    
        return render(request,'admin-panel/login.html')

def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            return render(request, 'admin-panel/register.html', {'error':'Username already exists'})
        except User.DoesNotExist:
            agree =  request.POST.get('agree-term', False)
            if agree == False:
                return render(request, 'admin-panel/register.html', {'error':'Terms and Conditions not satisfied'})
            else:    
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
                if request.POST['code'] != 'code':
                    user.delete()
                    return render(request, 'admin-panel/register.html', {'error':'Invalid Code!'})
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
                    return render(request,'admin-panel/register.html',{'error':'Could Not Register User'})
    else:
        return render(request,'admin-panel/register.html')

@login_required(login_url='login')
def OTF(request):
    if request.method == 'POST':
        try:
            user = request.user
            profile = UserProfile.objects.get(vuser = user)
            profile.name = request.POST['name']
            profile.interest = request.POST['interest']
            profile.address = request.POST['address']
            if request.POST['phone'] == '':
                profile.phone_no = '000000'
            else:    
                profile.phone_no = request.POST['phone']
            profile.website = request.POST['website']
            profile.about = request.POST['about']

            work = Work()
            work.title = request.POST['title']
            work.c_name = request.POST['cname']
            work.work_from = request.POST['wfrom'] 
            work.work_till = request.POST['wtill']
            work.description = request.POST['wdesc']
            work.user = user

            education = Education()
            education.title = request.POST['etitle']
            education.name = request.POST['ename']
            education.study_from = request.POST['efrom']
            education.study_till = request.POST['etill']
            education.description = request.POST['edesc']
            education.user = user
            
            project = Project()
            project.title = request.POST['ptitle']
            project.name = request.POST['pname']
            project.user = user

            try:
                profile.save()
                work.save()
                education.save()
                project.save()
                return redirect('index')

            except:
                work.delete()
                education.delete()
                project.delete()
                logout()     

        except UserProfile.DoesNotExist:
            return render(request, 'admin-panel/OTF', {'error':'User Not Registered'})    
            return redirect('otf') 
    else:        
        return render(request,'admin-panel/OTF.html')         

@login_required(login_url='login')
def index(request):
    user = request.user
    all_user = User.objects.all()
    profile = UserProfile.objects.get(vuser = user)
    current = str(profile.vuser)
    project = Project.objects.get(user = user)
    return render(request,'admin-panel/panel/panel.html',{'data':profile,'project':project,'all':all_user,'current':current})      

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


