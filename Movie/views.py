from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.hashers import check_password,make_password
from .models import User
from .comments import *
from django.contrib import messages
import random
# Create your views here.
def index(request):
    return render(request,'index.html')

def home(request):
    if request.session.get('user'):
        return render(request,"home.html")
    else:
       return redirect("/register/")


def signin(request):
    try:
        if request.method=='POST':
                funame=request.POST.get('username')
                fpassword=request.POST.get('password1')
                uname=User.objects.get(username=funame)
                pass1=uname.password
                if not check_password(fpassword,pass1):     
                    messages.add_message(request,messages.WARNING,'Enter The Correct Password')
                    return redirect("/login/")
                else:
                    request.session['user']= funame
                    return redirect("/home/")
    except Exception as e:
            messages.add_message(request,messages.WARNING,'User Does not exists')
            return redirect('/login/') 
        


def login(request):
        return render(request,'login.html')  


def stats(request):
    if request.session.get('user'):
        global video_id
        video_id=(str)(request.GET.get('video_id'))
        list=info(video_id)
        print(list)
        context={'info':list}
        return render(request,'Stats.html',context) 
    else:
       return redirect("/register/")
    

def logout(request):
    try:
        request.session.flush()    
        return redirect('/',{'log':'Log-In'})    
    except Exception as e:
        return redirect('/register/')

def sentiment(request):
    dict=sentAnal(video_id)
    videos_id=None
    return render(request,'sentiment.html',{'sent':dict})

def register(request):
    conf=True
    return render(request,'register.html')


def signup(request):
    if request.method=='POST':
        global uname
        uname=request.POST.get('username')
        fname=request.POST.get('fulname')
        mail=request.POST.get('email')
        pas=request.POST.get('password1')
        pas1=request.POST.get('password2')
        # print(uname," ",fname," ",mail," ",pas," ",pas1)

        if len(User.objects.filter(username=uname)):
            messages.add_message(request,messages.WARNING,'Username Already Exists')
            return redirect('/register/')
        
        elif len(User.objects.filter(gmail=mail)):
            messages.add_message(request,messages.WARNING,'This Email is Already In Use')
            return redirect('/register/')
        
        elif pas != pas1:
            messages.add_message(request,messages.WARNING,'Password Mismatch')
            return redirect('/register/')
        
        else:
            passs=make_password(pas)
            user=User(username=uname,fullname=fname,gmail=mail,password=passs)
            user.save()
            request.session['username']= uname
            senEmail(mail)
            return redirect('/otp/',{'parent':'Sign-Up'})

    
    return redirect('/home/')
        

def contact(request):
    return render(request,'contact.html')


def profile(request):
    if request.session.get('user'):
        return render(request,'profile.html')
    else:
        return redirect('/login/')



def update(request):
    try:
        if request.method=='POST':
            email=request.POST.get("email")
            passw=request.POST.get("Password")
            if email == "": email=None
            if passw=="":passw=None
            mail=len(User.objects.filter(gmail=email))
            if mail == 0:
                print(mail)
                if email is None and passw is not None:
                    uid=request.session['user']
                    obj=User.objects.get(username=uid)
                    obj.password=make_password(passw)
                    obj.save()
                    messages.add_message(request,messages.SUCCESS,"Password Updated Successfully")
                    return redirect('/profile/')
                elif email is not None and passw is None:
                    uid=request.session['user']
                    obj=User.objects.get(username=uid)
                    obj.gmail=email
                    obj.save()
                    messages.add_message(request,messages.SUCCESS,"Email Updated Successfully")
                    return redirect('/profile/')
                elif email is not None and passw is not None:
                    if not (len(User.objects.filter(gmail=mail))):
                        messages.add_message(request,request.WARNING,'This email is Already Associated with Another Account')
                    uid=request.session.get('user',default='Guest')
                    obj=User.objects.get(username=uid)
                    obj.gmail=email
                    obj.password=make_password(passw)
                    obj.save()
                    messages.add_message(request,messages.SUCCESS,"Email and Password Updated Successfully")
                    return redirect('/profile/')
                else:
                    return redirect('/profile/')
            else:
                messages.add_message(request,messages.WARNING,'Email Already Exists')
                return redirect('/profile/')
    except Exception as e:
        return redirect('/profile/')

def otp_verification(request):
     if request.method=='POST':
            num=(int)(request.POST.get('password2'))
            uname=request.session.get('username')
            request.session.flush()
            user=User.objects.get(username=uname)
            otp=user.otp
            if num==otp:
                    user.otp=333
                    user.save()
                    request.session['user']=uname
                    return redirect('/home/')
            else:
                messages.add_message(request,messages.WARNING,'Enter Correct Otp')
                return redirect('/otp/')
     
     return redirect('/otp/') 


def forgot(request):
    return render(request,'OtpVerification.html',{'parent':'Log-In'})

def forgot_password(request):
    if request.method=='POST':
        mail=request.POST.get('email')
        if not (len(User.objects.filter(gmail=mail))):
            messages.add_message(request,messages.WARNING,'Enter a Valid Mail')
            return redirect('/forgot/')
        senEmail(mail)
        user=User.objects.get(gmail=mail).username
        request.session['username']=user
        return redirect('/otp/')
    return redirect('/login/')

def otp(request):
    return render(request,'OtpVerification.html',{'parent':'Sign-Up'})


