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

def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_bar')
        if search_query:
            
            book_results = models.lesson.objects.filter(
                Q(ltitle__icontains=search_query) |
                Q(lesson_level__icontains=search_query) |
                Q(class_level__icontains=search_query) |
                Q(attribute__icontains=search_query)
            ).all()
            
            # Perform the search using Q objects for complex queries
            results = models.course.objects.filter(
                Q(course_name__icontains=search_query) |
                Q(c_type__icontains=search_query) |
                Q(meta_data__icontains=search_query)
            ).all()
            
            blog_results = models.article.objects.filter(
                Q(title__icontains=search_query) |
                Q(meta__icontains=search_query) |
                Q(search_str__icontains=search_query)
            ).all()
            
            paginator = Paginator(results, 20)
            book_paginator = Paginator(book_results, 20)
            blog_paginator = Paginator(blog_results, 20)
            
            context = {
                'results': paginator.page(1),
                'book_results': book_paginator.page(1),
                'blog_results': blog_paginator.page(1),
                'search_query': search_query,
            }
            return render(request, 'search.html', context=context)
        else:
            pass
    return render(request, 'search.html')