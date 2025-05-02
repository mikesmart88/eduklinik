from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    path('programs/', views.program, name='school program'),
    path('user/login', views.login_view, name='user login page'),
    path('blog/', views.blog, name='blog pages'),
    path('user/register', views.register_view, name='user register page'),
    
    #online school
    path('online_school/', views.online_school, name='online school page'),
]