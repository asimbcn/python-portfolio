from django.shortcuts import render, redirect
from django.contrib import auth
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from User.models import User, UserProfile, Work, Education, Project

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
            return render(request, 'admin-panel/login.html', {'error':'User Not Registered'}) 
    else:        
        return render(request,'admin-panel/OTF.html')         

@login_required(login_url='login')
def index(request):
    user = request.user
    all_user = User.objects.all()
    profile = UserProfile.objects.filter(vuser = user).first()
    current = str(profile.vuser)
    project = Project.objects.filter(user = user).first()
    work = Work.objects.filter(user = user).first()
    education = Education.objects.filter(user = user).first()
    return render(request,'admin-panel/panel/panel.html',{'data':profile,'project':project,'work':work,'education':education,'all':all_user,'current':current})      

@login_required(login_url='login')
def table(request):
    user = request.user
    profile = UserProfile.objects.get(vuser = user)
    email = profile.email
    phone = str(profile.phone_no)
    extra = {
        'phone': phone[-3:],
        'email': email[0:2]
    }
    work = Work.objects.filter(user = user)
    education = Education.objects.filter(user = user)
    project = Project.objects.filter(user = user)
    return render(request, 'admin-panel/panel/tables.html', {'data':profile,'project':project,'work':work,'education':education,'extra':extra})

@login_required(login_url='login')
def edit_user(request):
    profile = UserProfile.objects.get(vuser = request.user)
    if request.method == 'POST':
        if request.POST['email'] != '':
            mail = UserProfile.objects.filter(email = request.POST['email'])
            if mail:
                return render(request,'admin-panel/panel/edit-user.html',{'data':profile,'error':'Email Already Exist'})
            else:
                profile.email = request.POST['email']
        if request.POST['name'] != '': profile.name = request.POST['name']
        if request.POST['interest'] != '': profile.interest = request.POST['interest']
        if request.POST['address'] != '': profile.address = request.POST['address']
        if request.POST['phone_no'] != '': profile.phone_no = request.POST['phone_no']    
        if request.POST['website'] != '': profile.website = request.POST['website']
        if request.POST['about'] != '': profile.about = request.POST['about']
        try:
            profile.image = request.FILES['image']
        except MultiValueDictKeyError:    
            pass

        try:
            profile.save()
            return redirect('index')
        except:
            return render(request,'admin-panel/panel/edit-user.html',{'data':profile,'error':'Profile Update Error'})
    else:
        return render(request,'admin-panel/panel/edit-user.html',{'data':profile})    

@login_required(login_url='login')
def edit_work(request):
    print('EDIT WORK')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


