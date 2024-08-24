from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from .models import User
from .comments import *
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'index.html',{'log':'Log-In'})

def home(request):
    if request.session.get('username'):
        return render(request,"home.html")
    else:
       return redirect("/register/")

def signin(request):
    if request.method=='POST':
            funame=request.POST.get('username')
            fpassword=request.POST.get('password1')
            uname=User.objects.get(username=funame)
            pass1=uname.password
            print(uname," ",pass1)
            if not uname:
                messages.add_message(request,messages.WARNING,'User Does not exists')
                return redirect('/login/')
            elif not check_password(fpassword,pass1):     
                messages.add_message(request,messages.WARNING,'Enter The Correct Password')
                return redirect("/login/")
            else:
                request.session['username']= funame
                return redirect("/home/",{'log':'Log-Out'})


def login(request):
        return render(request,'login.html',{'log':'Log-In'})  


def stats(request):
    if request.session.get('username'):
        global video_id
        video_id=(str)(request.GET.get('video_id'))
        # print(video_id)
        list=info(video_id)
        print(list)
        context={'info':list}
        return render(request,'Stats.html',context) 
    else:
       return redirect("/register/")
    

def logout(request):
    try:
        del request.session['username']    
        return redirect('/',{'log':'Log-In'})    
    except Exception as e:
        return redirect('/register/',{'log':'Log-In'})

def sentiment(request):
    dict=sentAnal(video_id)
    videos_id=None
    return render(request,'sentiment.html',{'sent':dict})

def register(request):
    return render(request,'register.html',{'log':'Log-In'})


def signup(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        fname=request.POST.get('fulname')
        mail=request.POST.get('email')
        pas=request.POST.get('password1')
        pas1=request.POST.get('password2')
        print(uname," ",fname," ",mail," ",pas," ",pas1)
        if User.objects.filter(username=uname):
            messages.add_message(request,messages.WARNING,'Username Already Exists')
            return redirect('/register/')
        elif User.objects.filter(gmail=mail):
            messages.add_message(request,messages.WARNING,'This Email is Already In Use')
            return redirect('/register/')
        elif pas != pas1:
            messages.add_message(request,messages.WARNING,'Password Mismatch')
            return redirect('/register/')
        else:
            passs=make_password(pas)
            print(passs)
            user=User(username=uname,fullname=fname,gmail=mail,password=passs)
            user.save()
    request.session['username']=uname
    return redirect('/home/',{'log':'Log-Out'})
        

def contact(request):
    return render(request,'contact.html')


