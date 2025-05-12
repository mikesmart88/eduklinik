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
from django.core.paginator import Paginator, EmptyPage
from .functions import loop_mode
from django.conf import settings


# Create your views here.
@re_ge
def home(request):
    core = models.course.objects.filter(c_type='Core Academic Tracks')[:4]
    exam = models.course.objects.filter(c_type='Examination preperation')[:4]
    skill = models.course.objects.filter(c_type='Skill development services')[:4]
    spec = models.course.objects.filter(c_type='Specialized services')[:4]
    p_course = models.course.objects.annotate(high=Max('participant')).order_by('-pub_date')[:5]
    blog_view = models.article.objects.annotate(high=Max('views')).filter().order_by('-pub_date')[:3]
    context = {
        'core': core,
        'exam': exam,
        'skill': skill,
        'spec': spec,
        'home_bog': blog_view,
        'pop_cur': p_course,
    }
    
    return render(request, 'home.html', context=context)

@re_ge
def program(request):
    
    return render(request, 'programs.html')

def login_view(request):
    if request.user.is_authenticated:
        # check what type of use it is and return then to there dashboard
        #lets use student for now 
        return redirect('/dashboard')
    else:
        return render(request, 'user/login.html')
    
def register_view(request):
    if request.user.is_authenticated:
        # check what type of use it is and return then to there dashboard
        #lets use student for now 
        return redirect('/dashboard')
    else:
        return render(request, 'user/register.html')
    
    
def online_school(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        c_ann = models.c_notification.objects.order_by('-add_date')[:3]
        cann_count = models.c_notification.objects.all().count()
        context = {
            'user': current_user,
            'anounce': c_ann,
            'cnt': cann_count,
        }
        return render(request, 'online_school.html', context=context)
    else:
        return redirect('/user/login')
    
def course(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        p_course = models.course.objects.annotate(high=Max('participant')).order_by('-pub_date')[:10]
        cart_sub = models.subject.objects.prefetch_related('course').all()
        cann_count = models.c_notification.objects.all().count()
        context = {
            'user': current_user,
            'pop_cur': p_course,
            'subject': cart_sub,
            'subjects': cart_sub,
            'cnt': cann_count,
        }
        return render(request, 'courses/courseshome.html', context=context)
    else:
        return redirect('/user/login')
    
def popular_course(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        p_course = models.course.objects.annotate(high=Max('participant')).order_by('-pub_date').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(p_course, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'pop_cur': page,
            'cnt': cann_count,
        }
        return render(request, 'courses/popular.html', context=context)
    else:
        return redirect('/user/login')
    
def spec_cource(request, course):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        sub = models.subject.objects.filter(sub_name=course).first()
        cann_count = models.c_notification.objects.all().count()
        main_course = models.course.objects.filter(course_subject=sub).all()
        page_n = request.GET.get('page', 1)
        p = Paginator(main_course, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'pop_cur': page,
            'cnt': cann_count,
        }
        return render(request, 'courses/popular.html', context=context)
    else:
        return redirect('/user/login')

def get_course(request, str):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        main_course = models.course.objects.filter(c_str=str).first()
        cann_count = models.c_notification.objects.all().count()
        get_sub = models.subject.objects.filter(sub_name=main_course.course_subject).first()
        related = models.course.objects.filter(course_subject=get_sub).exclude(c_str=main_course.c_str).order_by('-pub_date')[:5]
        context = {
            'user': current_user,
            'main':main_course,
            'relative':related,
            'cnt': cann_count,
        }
        return render(request, 'courses/singlecourse.html', context=context)
    else:
        return redirect('/user/login')
    

def blog(request):
    popular_post = models.article.objects.annotate(high=Max('views')).filter().order_by('-pub_date')[:1]
    post = models.article.objects.all().order_by('-pub_date')
    page_n = request.GET.get('page', 1)
    p = Paginator(post, 15)
    try:
        page = p.page(page_n)
    except EmptyPage:
        page = p.page(1)
        
    context = {
        'popular': popular_post,
        'all_post': post,
        'page': page,
        
    }
    return render(request, 'blog.html', context=context)

def lesson_note(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        all_leson = models.lesson.objects.filter(attribute='lesson note').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(all_leson, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'l_all': page,
            'cnt': cann_count,
        }
        return render(request, 'lessonnotes/lesson.html', context=context)
    else:
        return redirect('/user/login')
    
def pass_quest(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        all_leson = models.lesson.objects.filter(attribute='past question').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(all_leson, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'l_all': page,
            'cnt': cann_count,
        }
        return render(request, 'pastquestions/pastquestion1.html', context=context)
    else:
        return redirect('/user/login')
    

def syllabuses(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        all_leson = models.lesson.objects.filter(attribute='syllabue').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(all_leson, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'l_all': page,
            'cnt': cann_count,
        }
        return render(request, 'syllabuses/syllabuses1.html', context=context)
    else:
        return redirect('/user/login')

def textbook(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        all_leson = models.lesson.objects.filter(attribute='textbook').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(all_leson, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'l_all': page,
            'cnt': cann_count,
        }
        return render(request, 'Textbooks/Textbooks1.html', context=context)
    else:
        return redirect('/user/login')
    
def handout(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        cann_count = models.c_notification.objects.all().count()
        all_leson = models.lesson.objects.filter(attribute='handout').all()
        page_n = request.GET.get('page', 1)
        p = Paginator(all_leson, 15)
        try:
            page = p.page(page_n)
        except EmptyPage:
            page = p.page(1)
        context = {
            'user': current_user,
            'l_all': page,
            'cnt': cann_count,
        }
        return render(request, 'handouts/handout1.html', context=context)
    else:
        return redirect('/user/login')
    
    
def payment(request, cstr):
    main = models.course.objects.filter(c_str=cstr).first()
    print(main.price)
    context = {
        'main': main,
        'amount': main.price,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'payments.html', context=context)

def lesson_pay(request, cstr):
    main = models.lesson.objects.filter(lesson_str=cstr).first()
    print(main.price)
    context = {
        'main':main,
        'amount': main.price,
        'paystack_pub_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'lesson_pay.html', context=context)

def webmanifest(request):
    return render(request, 'seo/manifest.json', content_type='application/json')


@re_ge
def about(request):
    cann_count = models.c_notification.objects.all().count()
    return render(request, 'about.html', {'cnt': cann_count,})


@re_ge
def contact(request):
    cann_count = models.c_notification.objects.all().count()
    return render(request, 'contact.html', {'cnt': cann_count,})

def singlelesson(request, l_str):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        main = models.lesson.objects.filter(lesson_str=l_str).first()
        cann_count = models.c_notification.objects.all().count()
        context = {
            'user': current_user,
            'main':main,
            'cnt': cann_count,
            
        }
        return render(request, 'lessonnotes/booksingle.html', context=context)
    else:
        return redirect('/user/login')
    


    