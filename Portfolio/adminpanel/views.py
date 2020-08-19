from django.shortcuts import render, redirect
from django.contrib import auth
from datetime import datetime
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
    return render(request, 'admin-panel/panel/tables.html', {'data':profile,'project':project,'work':work,'education':education,'extra':extra,'active':'active'})

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
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_work(request):
    data = UserProfile.objects.get(vuser = request.user)
    if request.method == 'POST':
        if request.POST['title'] == '': 
            return render(request,'admin-panel/panel/add-work.html',{'data':data,'error':'Title is Empty','active':'active'})
        if request.POST['work_from'] != '':   
            if int(request.POST['work_from']) > datetime.now().year or int(request.POST['work_from']) < (datetime.now().year - 100):
                return render(request,'admin-panel/panel/add-work.html',{'data':data,'error':'Work Start Year is Invalid','active':'active'})
        if request.POST['work_till'] != '':
            if int(request.POST['work_till']) < int(request.POST['work_from']) or int(request.POST['work_till']) > (datetime.now().year + 70):       
                return render(request,'admin-panel/panel/add-work.html',{'data':data,'error':'Work End Year is Invalid','active':'active'})  
        work = Work()
        work.title = request.POST['title']
        work.c_name = request.POST['c_name']
        work.work_from = request.POST['work_from']
        work.work_till = request.POST['work_till']
        work.description = request.POST['description']
        work.user = request.user
        try:
            work.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/add-work.html',{'data':data,'error':'Could not Add Work Data!','active':'active'})    

        
    else:
        return render(request,'admin-panel/panel/add-work.html',{'data':data,'active':'active'})    

@login_required(login_url='login')
def edit_work(request, id):
    data = UserProfile.objects.get(vuser = request.user)
    work = Work.objects.get(id = id)
    if request.method == 'POST':
        if request.POST['work_from'] != '' and work.work_from != '':   
            if int(request.POST['work_from']) > datetime.now().year or int(request.POST['work_from']) < (datetime.now().year - 100) or int(request.POST['work_from']) > int(work.work_till):
                return render(request,'admin-panel/panel/edit-work.html',{'data':data,'work':work,'error':'Work Start Year is Invalid','active':'active'})

        if request.POST['work_till'] != '':
            if request.POST['work_from'] == '' and work.work_from != '': work_date = work.work_from
            elif work.work_from == '':
                return render(request,'admin-panel/panel/edit-work.html',{'data':data,'work':work,'error':'Work Start is Empty','active':'active'})
            elif request.POST['work_from'] != '': 
                work_date = request.POST['work_from']  

            if int(request.POST['work_till']) < int(work_date) or int(request.POST['work_till']) > (datetime.now().year + 70):       
                return render(request,'admin-panel/panel/edit-work.html',{'data':data,'work':work,'error':'Work End Year is Invalid','active':'active'})
                 

        if request.POST['title'] != '': work.title = request.POST['title']
        if request.POST['c_name'] != '': work.c_name = request.POST['c_name']
        if request.POST['work_from'] != '': work.work_from = request.POST['work_from']
        if request.POST['work_till'] != '': work.work_till = request.POST['work_till']
        if request.POST['description'] != '': work.description = request.POST['description']
        try:
            work.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/edit-work.html',{'data':data,'work':work,'error':'Could Not Edit Work','active':'active'})    
    else:      
        return render(request,'admin-panel/panel/edit-work.html',{'data':data,'work':work,'active':'active'}) 

@login_required(login_url='login')
def delete_work(request, id):
    work = Work.objects.get(id = id)
    work.delete()
    return redirect('view')

@login_required(login_url='login')
def add_education(request):
    data = UserProfile.objects.get(vuser = request.user)
    if request.method == 'POST':
        if request.POST['title'] == '': 
            return render(request,'admin-panel/panel/add-education.html',{'data':data,'error':'Title is Empty','active':'active'})
        if request.POST['study_from'] != '':   
            if int(request.POST['study_from']) > datetime.now().year or int(request.POST['study_from']) < (datetime.now().year - 100):
                return render(request,'admin-panel/panel/add-education.html',{'data':data,'error':'Education Start Year is Invalid','active':'active'})
        if request.POST['study_till'] != '':
            if int(request.POST['study_till']) < int(request.POST['study_from']) or int(request.POST['study_till']) > (datetime.now().year + 70):       
                return render(request,'admin-panel/panel/add-education.html',{'data':data,'error':'Education End Year is Invalid','active':'active'})

        education = Education()
        education.title = request.POST['title']
        education.name = request.POST['name']
        education.study_from = request.POST['study_from']
        education.study_till = request.POST['study_till']
        education.description = request.POST['description']
        education.user = request.user
        try:
            education.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/add-education.html',{'data':data,'error':'Could not Add Education Data!','active':'active'})    
    else:
        return render(request,'admin-panel/panel/add-education.html',{'data':data,'active':'active'})     

@login_required(login_url='login')
def edit_education(request, id):
    data = UserProfile.objects.get(vuser = request.user)
    education = Education.objects.get(id = id)
    if request.method == 'POST':
        if request.POST['study_from'] != '' and education.study_from != '':   
            if int(request.POST['study_from']) > datetime.now().year or int(request.POST['study_from']) < (datetime.now().year - 100) or int(request.POST['study_from']) > int(education.study_till):
                return render(request,'admin-panel/panel/edit-education.html',{'data':data,'education':education,'error':'Education Start Year is Invalid','active':'active'})

        if request.POST['study_till'] != '':
            if request.POST['study_from'] == '' and education.study_from != '': edu_date = education.study_from
            elif education.study_from == '':
                return render(request,'admin-panel/panel/edit-education.html',{'data':data,'education':education,'error':'Education Start is Empty','active':'active'})
            elif request.POST['study_from'] != '': 
                edu_date = request.POST['study_from']  

            if int(request.POST['study_till']) < int(edu_date) or int(request.POST['study_till']) > (datetime.now().year + 70):       
                return render(request,'admin-panel/panel/edit-education.html',{'data':data,'education':education,'error':'Education End Year is Invalid','active':'active'})

        if request.POST['title'] != '': education.title = request.POST['title']
        if request.POST['name'] != '': education.name = request.POST['name']
        if request.POST['study_from'] != '': education.study_from = request.POST['study_from']
        if request.POST['study_till'] != '': education.study_till = request.POST['study_till']
        if request.POST['description'] != '': education.description = request.POST['description']
        try:
            education.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/edit-education.html',{'data':data,'education':education,'error':'Could Not Edit Education','active':'active'})
              
    else:
        return render(request,'admin-panel/panel/edit-education.html',{'data':data,'education':education,'active':'active'})


@login_required(login_url='login')
def delete_education(request, id):
    education = Education.objects.get(id = id)
    education.delete()
    return redirect('view')

@login_required(login_url='login')
def add_project(request):
    data = UserProfile.objects.get(vuser = request.user)
    if request.method == 'POST':
        if request.POST['title'] == '':
            return render(request,'admin-panel/panel/add-project.html',{'data':data,'error':'Title is Empty','active':'active'})
        if request.POST['name'] == '':
            return render(request,'admin-panel/panel/add-project.html',{'data':data,'error':'Project Name is Empty','active':'active'})

        project = Project()
        project.title = request.POST['title']
        project.name = request.POST['name']     
        project.language = request.POST['language']
        project.description = request.POST['description']
        project.completion = request.POST['completion']
        project.in_progress = request.POST['in_progress']
        project.user = request.user    

        try:
            project.image = request.FILES['image']
        except MultiValueDictKeyError:
            pass

        try:
            project.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/add-project.html',{'data':data,'error':'Could not Add Project Data!','active':'active'})        
 
    else:
        return render(request,'admin-panel/panel/add-project.html',{'data':data,'active':'active'})      

@login_required(login_url='login')
def edit_project(request, id):
    data = UserProfile.objects.get(vuser = request.user)
    project = Project.objects.get(id = id)
    if request.method == 'POST':

        if request.POST['title'] != '': project.title = request.POST['title']
        if request.POST['name'] != '': project.name = request.POST['name']     
        if request.POST['language'] != '': project.language = request.POST['language']
        if request.POST['description'] != '': project.description = request.POST['description']
        if request.POST['completion'] != '': project.completion = request.POST['completion']
        if request.POST['in_progress'] != '': project.in_progress = request.POST['in_progress']
        try:
            project.image = request.FILES['image']
        except MultiValueDictKeyError:
            pass

        try:
            project.save()
            return redirect('view')
        except:
            return render(request,'admin-panel/panel/edit-project.html',{'data':data,'project':project,'error':'Could not Edit Project','active':'active'}) 
    else:
        return render(request,'admin-panel/panel/edit-project.html',{'data':data,'project':project,'active':'active'})    
        

@login_required(login_url='login')
def delete_project(request, id):
    project = Project.objects.get(id = id)
    project.delete()
    return redirect('view')                 


