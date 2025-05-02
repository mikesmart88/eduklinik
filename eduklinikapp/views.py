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


# Create your views here.
@re_ge
def home(request):
    core = models.course.objects.filter(c_type='Core Academic Tracks')[:4]
    exam = models.course.objects.filter(c_type='Examination preperation')[:4]
    skill = models.course.objects.filter(c_type='Skill development services')[:4]
    spec = models.course.objects.filter(c_type='Specialized services')[:4]
    blog_view = models.article.objects.annotate(high=Max('views')).filter().order_by('-pub_date')[:3]
    context = {
        'core': core,
        'exam': exam,
        'skill': skill,
        'spec': spec,
        'home_bog': blog_view
    }
    
    return render(request, 'home.html', context=context)

@re_ge
def program(request):
    
    return render(request, 'programs.html')

def login_view(request):
    if request.user.is_authenticated:
        # check what type of use it is and return then to there dashboard
        #lets use student for now 
        return redirect('/user/dashboard')
    else:
        return render(request, 'user/login.html')
    
def register_view(request):
    if request.user.is_authenticated:
        # check what type of use it is and return then to there dashboard
        #lets use student for now 
        return redirect('/user/dashboard')
    else:
        return render(request, 'user/register.html')
    
    
def online_school(request):
    if request.user.is_authenticated:
        user = request.user
        current_user = models.profile.objects.filter(user=user).first()
        pics = models.userimage.objects.filter(profile=current_user).first()
        context = {
            'user': current_user,
            'img': pics,
        }
        return render(request, 'online_school.html', context=context)
    else:
        return redirect('/user/login')


def blog(request):
    popular_post = models.article.objects.annotate(high=Max('views')).filter().order_by('-pub_date')[:1]
    post = models.article.objects.all().order_by('-pub_date')
    page_n = request.GET.get('page', 1)
    p = Paginator(post, 1)
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