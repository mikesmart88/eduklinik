from django.contrib import admin
from .models import  profile, staff, article, course, lesson, link, subject, user_course, transaction, course_payment, notification, c_notification, pro_image
# Register your models here.

admin.site.register(profile)
admin.site.register(staff)
admin.site.register(article)
admin.site.register(course)
admin.site.register(lesson)
admin.site.register(link)
admin.site.register(subject)
admin.site.register(user_course)
admin.site.register(transaction)
admin.site.register(course_payment)
admin.site.register(notification)
admin.site.register(c_notification)
admin.site.register(pro_image)