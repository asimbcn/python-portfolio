from django.shortcuts import render, redirect
from .models import User, UserProfile, Work, Education, Project, Contact


# Create your views here.
def index(request):
    try:
        user = User.objects.get(active=True)
        profile = UserProfile.objects.get(vuser=user)
        work = Work.objects.filter(user=user)
        education = Education.objects.filter(user=user)
        project = Project.objects.filter(user=user)
        return render(
            request,
            "index.html",
            {
                "profile": profile,
                "work": work,
                "education": education,
                "project": project,
            },
        )
    except:
        return redirect("error404")


def error(request):
    return render(request, "error.html")


def contact(request):
    if request.method == "POST":
        if (
            request.POST["name"] != ""
            and request.POST["email"] != ""
            and request.POST["subject"] != ""
            and request.POST["message"] != ""
        ):
            contact = Contact()
            contact.name = request.POST["name"]
            contact.email = request.POST["email"]
            contact.subject = request.POST["subject"]
            contact.description = request.POST["message"]
            try:
                user = User.objects.get(username=request.POST["user"])
                contact.user = user
            except:
                return render(request, "error.html")
            try:
                contact.save()
                return redirect("home")
            except:
                return render(request, "error.html")
        else:
            return render(request, "error.html")
    else:
        return redirect("home")
