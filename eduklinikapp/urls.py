from django.urls import path
from . import views, search_views, profille_view, payment

urlpatterns = [
    path('', views.home, name='homepage'),
    path('programs/', views.program, name='school program'),
    path('user/login', views.login_view, name='user login page'),
    path('blog/', views.blog, name='blog pages'),
    path('user/register', views.register_view, name='user register page'),
    path('payment/pay/<cstr>', views.payment, name='payment page'),
    path('lesson/pay/<cstr>',views.lesson_pay, name='lesson payment'),
     path('lesson/verify-payment/<cstr>/', payment.lesson_verify_payment, name='verify payment'),
    path('verify-payment/<cstr>/', payment.verify_payment, name='verify payment'),
    path('search/', search_views.search, name='systerm search'),
    path('about/', views.about, name='about page'),
    path('contact/', views.contact, name='contact us'),
    
         #online school
    path('online_school/', views.online_school, name='online school page'),
    path('course/', views.course, name='corse pages'),
    path('course/popular', views.popular_course, name='popular post'),
    path('course/<course>', views.spec_cource, name='subject course'),
    path('course/single/<str>', views.get_course, name='single course pages'),
    path('leasson/', views.lesson_note, name='lesson note page'),
    path('past_question/', views.pass_quest, name='pass question docs'),
    path('syllabuse/', views.syllabuses, name='syllabuse page'),
    path('textbook/', views.textbook, name="text book page"),
    path('handout/', views.handout, name="handout page"),
    # dashboard
    path('dashboard/', profille_view.dashboard, name='user dashboard'),
    path('user/profile/', profille_view.profile, name='user profile'),
    path('notification/', profille_view.notification, name="notification"),
    path('accout/course/', profille_view.dash_course, name="your courses"),
    path('private_lesson/', profille_view.private, name='user private lessons'),
    path('performanc/', profille_view.performance, name='user performance'),
    
    #ajax
    path('new_user/', profille_view.user_register, name='new user registration'),
    path('log_user/', profille_view.login_user, name='user lofin'),
    path('logout/', profille_view.userlogout, name='user logout'),
    
    #admin
    path('user_manager/', profille_view.user_manage, name='user management'),
    path('user_profile/<str>', profille_view.ge_profile, name='profiles'),
    path('account/settings', profille_view.setting, name='user_setting'),
]