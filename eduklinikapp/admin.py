from django.contrib import admin
from .models import  profile, userimage, staff, article, course, lesson, link
# Register your models here.

admin.site.register(profile)
admin.site.register(userimage)
admin.site.register(staff)
admin.site.register(article)
admin.site.register(course)
admin.site.register(lesson)
admin.site.register(link)