from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('User must have an username')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    username = models.TextField(
        verbose_name = 'username',
        max_length = 50,
        unique = True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELD = [] #password

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

class UserProfile(models.Model):
    name = models.CharField(max_length=30,null=True)
    interest = models.CharField(max_length=100,null=True)
    address = models.CharField(max_length=80,null=True)
    phone_no = models.IntegerField(null=True)
    email = models.EmailField(unique=True)
    website = models.CharField(max_length=100,null=True)
    about = models.TextField(null=True)
    image = models.ImageField(upload_to='user/',null=True)
    vuser = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name      

class Work(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    c_name = models.CharField(max_length=30)
    work_from = models.CharField(max_length=30)
    work_till = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.title

class Education(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    study_from = models.CharField(max_length=30)
    study_till = models.CharField(max_length=30)
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30) 
    name = models.CharField(max_length=30)
    in_progress = models.BooleanField(default=False)
    language = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    completion = models.IntegerField()
    image = models.ImageField(upload_to='project/',null=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30) 
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=50)
    description = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        value = self.subject + ' -> ' + self.email
        return value          




              

