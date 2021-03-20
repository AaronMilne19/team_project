from django.shortcuts import render,redirect
from django.http import JsonResponse
from .AccountForm import RegisterForm, LoginForm,UserInfomationForm
from django.contrib.auth.models import User
from home.models import MVUser
from django.contrib.auth import authenticate, login as auth_login,logout as auth_loginout
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import hashlib,os,time



def register(request):
    if request.method == "GET":
        registerForm = RegisterForm()
        return render(request, 'register.html', {"registerForm": registerForm})
    else:
        registerForm = RegisterForm(request.POST)
        status = False
        if registerForm.is_valid():
            user = User.objects.create_user(
                username=registerForm.cleaned_data["username"],
                first_name=registerForm.cleaned_data["fristname"],
                password=registerForm.cleaned_data["password"],
                email=registerForm.cleaned_data["email"],
            )
            Nvuser = MVUser(DjangoUser=user, DateOfBirth=registerForm.cleaned_data["brith"],Surname=registerForm.cleaned_data["surname"])
            Nvuser.save()
            status = True
            auth_login(request, user)
            return JsonResponse({"status": status, "msg": "register sucess!"})
        else:
            return JsonResponse({"status": status, "res": registerForm.errors.as_json()})

def login(request):
    if request.method == "GET":
        loginForm = LoginForm()
        return render(request, 'login.html', {"loginForm": loginForm})
    else:
        loginForm = LoginForm(request.POST)
        status = False
        if loginForm.is_valid():
            username = loginForm.cleaned_data["username"]
            password = loginForm.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            status = True
            if user is not None:
                auth_login(request, user)


                return JsonResponse({"status": status, "msg": "Login Successful!"})
            else:
                return JsonResponse({"status": status, "msg": "login failed!"})
        else:
            return JsonResponse({"status": status, "res": loginForm.errors.as_json()})

@login_required(login_url="/login")
def account(request):
    if request.method=="GET":
        user=request.user
        userprofile=MVUser.objects.get(DjangoUser=user)
        # userInfomationForm=UserInfomationForm({
        #     "username":user.username,
        #     "email":user.email,
        #     "surname":userprofile.Surname,
        #     "fristname":user.first_name,
        #     "brith":userprofile.DateOfBirth
        # })
        return render(request,'Account_Settings.html',{"userprofile":userprofile,"user":user})
    else:
        userInfomationForm = UserInfomationForm(request.POST)
        status=False
        if userInfomationForm.is_valid():
            user = request.user
            userprofile = MVUser.objects.get(DjangoUser=user)
            user.username=userInfomationForm.cleaned_data["username"]
            user.first_name=userInfomationForm.cleaned_data["fristname"]
            user.email=userInfomationForm.cleaned_data["email"]
            userprofile.Surname=userInfomationForm.cleaned_data["surname"]
            userprofile.DateOfBirth=userInfomationForm.cleaned_data["brith"]
            user.save()
            userprofile.save()
            status=True
            return JsonResponse({"status":status,"msg":"Sucessful!"})
        else:
            return JsonResponse({"status":status,"res":userInfomationForm.errors.as_json()})

@login_required(login_url="/login")
def upload_avatar(request):
    if request.method=="GET":
      return render(request,'upload_avatar.html')
    else:
        try:
            s = request.FILES.get('file')
            ext = os.path.splitext(s.name)[1]
            timestrap = time.strftime('%Y%m%d',time.gmtime())
            md5_pwd = get_md5()
            NewFileName ="%s$$%s%s"%(s.name,md5_pwd,ext)
            file_save_path  = os.path.join(settings.BASE_DIR, "static", "uploads",timestrap)
            if not os.path.exists(file_save_path):
                os.mkdir(file_save_path)
            with open(os.path.join(file_save_path , NewFileName), 'wb') as f:
                for i in s.chunks():
                    f.write(i)
            res = {
                "code": 0,
                "msg": 'Sucessful!',
                "data": {
                    "src": "/" + os.path.join("static", "uploads", timestrap, NewFileName).replace("\\", "/"),
                }
            }
            userprofile=MVUser.objects.get(DjangoUser=request.user)
            userprofile.Avatar="/" + os.path.join("static", "uploads", timestrap, NewFileName).replace("\\", "/")
            userprofile.save()
        except:
            res = {
                "code": 1,
                "msg": 'Failed!',
            }
        return JsonResponse(res)

@login_required(login_url="/login")
def loginout(request):
    '''
      退出登录
    '''
    auth_loginout(request)
    return redirect('/account/login/')
def get_md5():
    time_now=timezone.now()
    m=hashlib.md5()
    m.update(str(time_now).encode())
    return  m.hexdigest()