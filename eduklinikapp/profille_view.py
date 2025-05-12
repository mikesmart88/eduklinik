from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse as json
from . import models
from django.db.models import F, Q
from .functions import rand_string_generator
from django.db.models import Max
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse as json
from django.views.decorators.http import require_GET as re_ge
from django.contrib.auth.decorators import login_required as l_g
from django.contrib.auth import authenticate, login, logout
from user_agents import parse
from django.core.paginator import Paginator, EmptyPage


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        user_curcn = models.user_course.objects.filter(course_holder=current_user).count()
        private_count = models.tech_msg.objects.filter(student=current_user).count()
        cann_count = models.c_notification.objects.all().count()
        c_ann = models.c_notification.objects.order_by('-add_date')[:5]
        context = {
            'user': current_user,
            'pop_cur':user_cour,
            'curs_con': user_curcn,
            'tech_count': private_count,
            'anounce': c_ann,
            'cnt': cann_count,
        }
        return render(request, 'user/dashboard.html', context=context)
    else:
        return redirect('/user/login')

def notification(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        user_not = models.notification.objects.filter(user=current_user).order_by('-add_date').all()
        c_ann = models.c_notification.objects.order_by('-add_date').all()
        cann_count = models.c_notification.objects.all().count()
        page_n = request.GET.get('page', 1)
        p = Paginator(c_ann, 20)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'pop_cur':user_cour,
            'noti': user_not,
            'anounce': page,
            'cnt': cann_count
        }
        return render(request, 'user/notification.html', context=context)
    else:
        return redirect('/user/login')

def dash_course(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date').all()
        
        context = {
            'user': current_user,
            'pop_cur':user_cour,
        }
        return render(request, 'user/dash_course.html', context=context)
    else:
        return redirect('/user/login')
    
def private(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        context = {
            'user': current_user,
            'pop_cur':user_cour,
        }
        return render(request, 'user/private.html', context=context)
    else:
        return redirect('/user/login')
    
def performance(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        
        context = {
            'user': current_user,
            'pop_cur':user_cour,
        }
        return render(request, 'user/performance.html', context=context)
    else:
        return redirect('/user/login')
    
    
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        if current_user.acc_type == 'Admin':
            context = {
            'user': current_user,
            'pop_cur':user_cour,
            }
            return render(request, 'admin/profile.html', context=context)
            
        context = {
            'user': current_user,
            'pop_cur':user_cour,
        }
        return render(request, 'user/profile.html', context=context)
    else:
        return redirect('/user/login')
    
# admin\
    
def user_manage(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        all_user = models.profile.objects.exclude(user=user).all()
        context = {
            'user': current_user,
            'all': all_user,
        }
        return render(request, 'admin/users.html', context=context)
    else:
        return redirect('/user/login')
    
def ge_profile(request, str):
    pro = models.profile.objects.filter(user_token=str).first()
    context = {
        'user': pro,
    }
    return render(request, 'admin/profiles.html', context=context)


def setting(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        user_cour = models.user_course.objects.filter(course_holder=current_user).order_by('-date')[:10]
        if current_user.acc_type == 'Admin':
            context = {
            'user': current_user,
            'pop_cur':user_cour,
            }
            return render(request,'admin/setting.html', context=context)
            
        context = {
            'user': current_user,
            'pop_cur':user_cour,
        }
        return render(request, 'user/setting.html', context=context)
    else:
        return redirect('/user/login')
    

def user_register(request):
    try:
        if request.method == 'POST':
            username = request.POST['uname']
            full_name = request.POST['fname']
            phone = request.POST['phone'] 
            email = request.POST['email']
            country = request.POST['country']
            _code = request.POST['code']
            age = request.POST['age'] 
            password = request.POST['passwd']
            acct_type = request.POST['acct_type']
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            user_agent = parse(user_agent_string)
            browser = user_agent.browser.family
            browser_version = user_agent.browser.version_string
            os = user_agent.os.family
            device = user_agent.device.family
            device_brand = user_agent.device.brand
            x_forward = request.META.get('HTTP_X_FORWARDER_FOR')
            if x_forward is not None:
                ip = x_forward.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            validate_user = User.objects.filter(username=username).first()
            validate_email = User.objects.filter(email=email).first()
            if validate_user:
                return json({'E': 'Sorry this username is already taken'}, safe=False)
            elif validate_email:
                return json({'E': 'Sorry this email is already taken'}, safe=False)
            else:
                pass
            new_user = User.objects.create_user( username=username, email=email, password=password)
            new_user.first_name = full_name
            new_user.save()
            auth_user = User.objects.filter(username=username).first()
            if auth_user:
                new_holder = models.profile.objects.create(user=auth_user, Verified=True, country=country, phone_number=phone, ip_adress=ip, c_code=_code, browser=f'{browser}, {browser_version}', age=age, account_type=acct_type )
                new_holder.save()
                print('User login succesfully!!!')
                this_user = authenticate(request, username=username, password=password)
                login(request, this_user)
                ### send mail here #########################
                ############################################
                return json({'S': 'User created successful'}, safe=False)
            else:
               return json({'E': 'Sorry user could not be created'}, safe=False)
        else:
            return json({'E': 'Sorry not post request'}, safe=False)
    except BaseException as e:
        print(e)
        return json({'E': 'Sorry user could not be created'}, safe=False)


def login_user(request):
    try:
        if request.method == 'POST':
            user_name = request.POST['uname']
            passwd = request.POST['passwd']

            valid = User.objects.filter(username__exact=user_name).first()
            if valid is not None:
                this_user = authenticate(request, username=user_name, password=passwd)
                login(request, this_user)
                print('\n============\n  you are now logged in \n=============\n')
                return(json({'S':'Logged in sucessfully'}, safe=False))
            else:
                print('\n============\n  sorry this user is invalid \n=============\n')
                return(json({'E': 'sorry this user is invalid'}, safe=False))
        else:
            print('\n============\n  sorry this user is invalid \n=============\n')
            return(json({'E':'Post error ocurred'}, safe=False))
        
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, AttributeError) as err:
         print(err)
         return(json({'E': 'Invalid email or password!'}, safe=False))


def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        pass
