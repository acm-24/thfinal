from email import message
from http.client import HTTPResponse
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Question,User_points
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.contrib.sessions.models import Session
import django.contrib.auth as djangoAuth

def home(request):
    return render(request,"home.html")

def index(request):
    return render(request,"index.html")

def backup(request):
    return render(request,"backup.html")

def thanks(request):
    return render(request,"Thanks.html")

def register(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        e=request.POST.get('e_no')
        p1=request.POST.get('password1')
        p2=request.POST.get('password2')
        if p1!=p2:
            messages.warning(request,"Passwords does not match")
            return redirect('register')
        else:
            if User.objects.filter(username=e).exists():
                messages.warning(request,"This Enrollment no is already registered")
                return redirect('register')
            else:
                user=User.objects.create_user(username=e,password=p1,email=email,first_name=fname,last_name=lname)
                user.save()
                messages.success(request,"Registered sucessfully, Please signin to play")
                return redirect('signin')
    else:
        return render(request,"register.html")

def play(request):
    if request.session.has_key('is_logged'):
        e= request.session['enroll']
        play1=User_points.objects.get(e_no=e)
        if play1.cur_ques>=4:
            return render(request,"Thanks.html",{'play1':play1})
        qstn= Question.objects.get(q_id=play1.cur_ques)
        if request.method == "POST":
            if request.POST.get('ans')==qstn.q_ans:
                play1.cur_ques=play1.cur_ques+1
                play1.hint=0
                play1.reputation=play1.reputation+qstn.q_point
                if qstn.q_point>15:
                    qstn.q_point=qstn.q_point-1
                play1.save()
                qstn.save()
                if play1.cur_ques>=4:
                    return render(request,"Thanks.html",{'play1':play1})
            else:
                pass
        qstn= Question.objects.get(q_id=play1.cur_ques)
        return render(request,"play.html",{'qstn' : qstn,'play1':play1})   
    else:
        messages.warning(request,'Signin in first to play the game')
        return redirect('signin')

def first_letter(request):
    if request.session.has_key('is_logged'):
        e= request.session['enroll']
        play1=User_points.objects.get(e_no=e)
        qstn= Question.objects.get(q_id=play1.cur_ques)
        if request.method == "POST":
            if(play1.first_letter==0):
                play1.first_letter=1
                play1.reputation=play1.reputation-10
                play1.save()
            else:
                pass
            str1=qstn.q_ans
            messages.success(request,'First letter is '+str1[0])
        return render(request,"play.html",{'qstn' : qstn,'play1':play1})
    else:
        return redirect('signin')

def length(request):
    if request.session.has_key('is_logged'):
        e= request.session['enroll']
        play1=User_points.objects.get(e_no=e)
        qstn= Question.objects.get(q_id=play1.cur_ques)
        if request.method == "POST":
            if(play1.length==0):
                play1.length=1
                play1.reputation=play1.reputation-10
                play1.save()
            else:
                pass
            str1=qstn.q_ans
            messages.success(request,'Length of word is '+str(len(str1)))
        return render(request,"play.html",{'qstn' : qstn,'play1':play1})
    else:
        return redirect('signin')

def hint1(request):
    if request.session.has_key('is_logged'):
        e= request.session['enroll']
        play1=User_points.objects.get(e_no=e)
        qstn= Question.objects.get(q_id=play1.cur_ques)
        if request.method == "POST":
            if(play1.hint==0):
                play1.hint=1
                play1.reputation=play1.reputation-3
                play1.save()
            else:
                pass
            messages.success(request,'Hint 1 is '+qstn.hint1)
        return render(request,"play.html",{'qstn' : qstn,'play1':play1})
    else:
        return redirect('signin')

def hint2(request):
    if request.session.has_key('is_logged'):
        e= request.session['enroll']
        play1=User_points.objects.get(e_no=e)
        qstn= Question.objects.get(q_id=play1.cur_ques)
        if request.method == "POST":
            if(play1.hint==0):
                messages.warning(request,'You have to take Hint1 before taking Hint 2')
                return render(request,"play.html",{'qstn' : qstn,'play1':play1})
            elif(play1.hint==1):
                play1.hint=2
                play1.reputation=play1.reputation-5
                play1.save()
            else:
                pass
            messages.success(request,'Hint 2 is '+qstn.hint2)
        return render(request,"play.html",{'qstn' : qstn,'play1':play1})
    else:
        return redirect('signin')

def contact(request):
    return render(request,"contact.html")

def leaderboard(request):
    play1=User_points.objects.all().order_by('-reputation')[:10]
    return render(request,"leaderboard.html",{'play1' : play1})

def rules(request):
    return render(request,"rules.html")

def signin(request):
    if request.session.has_key('is_logged'):
        return redirect('play')
    else:
        djangoAuth.logout(request)
        if request.method == "POST":
            e=request.POST.get('e_no')
            p1=request.POST.get('pass1')
            user=auth.authenticate(username=e,password=p1)
            if user is not None:
                request.session['is_logged']=True
                request.session['enroll']=e
                print("session created")
                print (request.session['is_logged'])
                print (request.session['enroll'])
                auth.login(request,user)
                if User_points.objects.filter(e_no=e).exists():
                    pass
                else:
                    h=User_points.objects.create(e_no=e)
                    print("first time entry in user points table")
                    h.save()
                return redirect("play")
            else:
                messages.warning(request,"Authentication failed")
                return redirect('signin')
        else:
            return render(request,"signin.html")


# def signin(request):
#     if request.method == "POST":
#         e=request.POST.get('e_no')
#         p1=request.POST.get('pass1')
#         print(e)
#         print(p1)
#         if User_register.objects.filter(e_id=e).exists():
#             u_obj = User_register.objects.get(e_id=e)
#             if  u_obj.e_p!= p1:
#                 messages.warning(request,"Incorrect password")
#                 return redirect('signin')
#             else:
#                 if User_points.objects.filter(e_no=e).exists():
#                     pass
#                 else:
#                     h=User_points.objects.create(e_no=u_obj,reputation=100,cur_ques=1,hint=0)
#                     h.save()
#                 play1=User_points.objects.get(e_no=e)
#                 qstn= Question.objects.get(q_id=play1.cur_ques)
#                 return render(request,"play.html",{'qstn':qstn,'play1':play1})
#         else:
#             messages.warning(request,"Enrollment no not yet registered")
#             return redirect('signin')
#     else:
#         return render(request,"signin.html")
    

# def hunt_register(request):
#     if request.method == "POST":
#             e=request.POST.get('e_no')
#             p1=request.POST.get('password1')
#             p2=request.POST.get('password2')
#             print(e)
#             print(p1)
#             print(p2)
#             if p1!=p2:
#                 messages.warning(request,"Passwords does not match")
#                 return redirect('reg')
#             else:
#                 if User_register.objects.filter(e_id=e).exists():
#                     messages.warning(request,"This Enrollment no is already registered")
#                     return redirect('reg')
#                 else:
#                     h=User_register.objects.create(e_id=e,e_p=p1)
#                     h.save()
#                     messages.success(request,"Registered sucessfully, Please signin to play")
#                     return render(request,"signin.html")
#     else:
#         return render(request,"hunt_register.html")

def logout(request):
   try:
      del request.session['is_logged']
      del request.session['enroll']
      print ('session deleted')
   except:
      pass
   return redirect('signin')
