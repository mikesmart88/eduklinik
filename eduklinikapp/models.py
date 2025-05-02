from django.db import models
from django.contrib.auth.models import User
import os, datetime, string, random
from django.utils import timezone
from django.urls import reverse
from PIL import Image, ImageDraw, ImageFont
import PIL
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import F, Q
from .functions import rand_string_generator, s_remove

# Create your models here.

class profile(models.Model):

    acc_type = [
        ('General','General'),
        ('Admin','Admin'),
        ('staff', 'Staff'),
        ('Parent', 'Parent'),
    ]
    user = models.OneToOneField(User, verbose_name='user', on_delete= models.CASCADE)
    is_disabled = models.BooleanField('if this account is disabled', default=False)
    country = models.CharField('user country', null=False, blank=False, max_length=1000)
    Verified = models.BooleanField('if the user is verified', default=False)
    user_token = models.CharField('user token', null=True, blank=True, max_length=200, unique=True)
    phone_number = models.CharField('user mobile number', null=False, blank=False, max_length=50)
    is_edit = models.BooleanField('if the user have edited ', default=False)
    account_type = models.CharField('the account type', null=True, blank=False, max_length=200, choices=acc_type, default='General')
    not_count =  models.BigIntegerField('user notification  count', default=0)
    date_joined = models.DateTimeField('the date time account was created', default=timezone.now)
    ip_adress = models.GenericIPAddressField('user ip adress', null=True, blank=True)
    reset_code = models.CharField('user one time reset code', null=True, blank=True, max_length=100)
    c_code = models.CharField('user country code', null=True, blank=True, max_length=11)
    refer_code = models.CharField('user referial code', null=True, blank=True, unique=True, max_length=100)
    browser = models.CharField('user access browser', null=True, blank=True, max_length=100)
    qr_code = models.ImageField('user qrcode', null=True, blank=True, upload_to='qrcodes')
    
    def __str__(self):
        return str(self.user)
    
    def get_exact_user(self):
        return reverse('blkapp:reset_profile', kwargs={'token':self.user_token})
        
    def save(self, *args, **kwargs):

        if self.is_edit == False:
            self.user_token = f'B{rand_string_generator(10)}'
            self.refer_code = rand_string_generator(7)
            self.is_edit = True 
            
        else:
            pass
        return super(profile, self).save(*args, **kwargs)

class userimage(models.Model):
    profile = models.ForeignKey('profile', on_delete=models.CASCADE)
    pics = models.ImageField('user image', null=False, blank=False, upload_to='profile pics')
    is_edit = models.BooleanField('is edited', default=False)
    
    def __str__(self):
        return f'{self.profile} --- images'
    
    def save(self, *args, **kwargs):

        if self.is_edit == False:
           if self.pics:
                # editing the inage frame and moviefile
                in_img = Image.open(self.pics)
                in_img = in_img.convert("RGB")

                # resizing the frame

                i = in_img
                img_h = i.height-30 if i.height > 400 else i.height-10
                img_w = i.width-30  if i.width > 400 else i.width-10
                i = i.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)

                i_io = BytesIO()
                i.save(i_io, format='PNG')
                self.pics = InMemoryUploadedFile(i_io, None, f'Blk_{self.profile}{rand_string_generator(10)}.webp', 'image/webp', None, None)

                self.is_edit = True 
           else:
               pass
        return super(userimage, self).save(*args, **kwargs)
    
    
class staff(models.Model):
    
    staff_typ = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Totor', 'Tutor'),
        ('Contributor', 'Contributor'),
        ('Developer', 'Developer'),
    ]
    staff_holder = models.ForeignKey('profile', on_delete=models.CASCADE)
    name = models.CharField('staff name', null=False, blank=False, max_length=200)
    staff_token = models.CharField('staff token', null=True, blank=True, max_length=200, unique=True)
    is_assined = models.BooleanField('if user is assignrd to a studen', default=False)
    staff_type = models.CharField('the staff type', null=False, blank=False, max_length=200, choices=staff_typ, default='Teachers')
    staff_whatsapp = models.URLField('staff whatsapp link', null=False, blank=True)
    staff_facebook = models.URLField('staff facebook link', null=False, blank=True)
    staff_telegram = models.URLField('staff telegram link', null=False, blank=True)
    
    def __str__(self):
        return f'{self.staff_holder} --- staff'
    
    def save(self, *args, **kwargs):
        self.user_token = f'staff{rand_string_generator(10)}'
        return super(staff, self).save(*args, **kwargs)
    
    

# blog contents

class article(models.Model):
    author = models.ForeignKey('staff', on_delete=models.CASCADE)
    title = models.CharField('article title', null=False, blank=False, max_length=200)
    meta = models.CharField('metadata', null=False, blank=False, max_length=200)
    search_str = models.CharField('search str to search blog', null=True, blank=True, max_length=200, unique=True)
    post_str = models.CharField('post spec id', null=True, blank=True, max_length=200, unique=True)
    context = models.TextField('article context and text', null=False, blank=False)
    image = models.ImageField('artile image/post', null=True, blank=False, upload_to='post_images')
    is_edited = models.BooleanField('if post has been edited', default=False)
    pub_date = models.DateTimeField('date time of post', default=timezone.now)
    likes_count = models.BigIntegerField('likes count', default=0)
    views = models.BigIntegerField('blog views', default=0)
    commet_count = models.BigIntegerField('blog views', default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-pub_date']

    def was_publised_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def save(self, *args, **kwargs):
        if self.is_edited == False:
            self.post_str = f'Post_{self.title}_{rand_string_generator(10)}'
            
            if self.image:
                # editing the inage frame and moviefile
                in_img = Image.open(self.image)
                in_img = in_img.convert("RGB")
                # resizing the frame
                i = in_img
                img_h = i.height-30 if i.height > 400 else i.height-10
                img_w = i.width-30  if i.width > 400 else i.width-10
                i = i.resize((img_w, img_h), PIL.Image.Resampling.LANCZOS)
                i_io = BytesIO()
                i.save(i_io, format='PNG')
                self.image = InMemoryUploadedFile(i_io, None, f'post_{self.title}{rand_string_generator(10)}.webp', 'image/webp', None, None)
                self.is_edited =True
            else:
                pass
        else:
            pass
        return super(article, self).save(*args, **kwargs)
        
        



class course(models.Model):
    
    c_typ = [
        ('Core Academic Tracks', 'Core Academic Tracks'),
        ('Examination preperation', 'Examination preperation'),
        ('Skill development services', 'Skill development services'),
        ('Specialized services', 'Specialized services'),
    ]
    
    course_name = models.CharField('cource_name eg mathematics english', null=False, max_length=200)
    requiremwnt = models.CharField('requirments to partipate on this course', null=False, blank=True, max_length=1000)
    c_type = models.CharField('requirments to partipate on this course', null=False, blank=True, max_length=1000, choices=c_typ)
    lesson_count = models.BigIntegerField('number of leassons', default=0)
    meta_data = models.CharField('course meta decription', null=False, max_length=200)
    participant = models.BigIntegerField('number of students', default=0)
    weeks = models.CharField('specify how long it should take to complete the course', null=False, max_length=200, default='1 week')
    c_img = models.ImageField('add a image to decribe the corse', null=True, blank=True, max_length=200)
    
    def __str__(self):
        return self.course_name

    
class lesson(models.Model):
    
    l_typ = [
        ('Basic', 'Basic'),
        ('Advance', 'Advance'),
        ('Master', 'Master'),
    ]
    
    cls = [
        ('Basic6', 'Basic6'),
        ('Jss1', 'Jss1'),
        ('Jss2', 'Jss2'),
        ('Jss3', 'Jss3'),
        ('Ss1', 'Ss1'),
        ('Ss2', 'Ss2'),
        ('Ss3', 'Ss3'),
    ]
    
    under_course = models.ForeignKey('course', on_delete=models.CASCADE)
    ltitle = models.CharField('lesson name', blank=False, max_length=200)
    lesson_str = models.CharField('leason spec id', null=True, blank=True, max_length=200, unique=True)
    lesson_img = models.CharField('add a image to decribe the lesson', null=False, blank=True, max_length=200)
    lesson_level = models.CharField('leasson level', null=False, blank=True, choices=l_typ, default='Basic', max_length=200)
    class_level = models.CharField('leasson class', null=False, blank=True, choices=cls, default='Basic6', max_length=200)
    
    def __str__(self):
        return f'{self.under_course} {self.ltitle} ---lesson'
    
    def save(self, *args, **kwargs):
        self.lesson_str = rand_string_generator(10)
        add_course = course.objects.filter(course_name=self.under_course.course_name).first()
        if add_course:
            course.objects.filter(course_name=self.under_course.course_name).update(lesson_count=F('lesson_count') +1)
            add_course.refresh_from_db()
        else:
            pass
        return super(lesson, self).save(*args, **kwargs)
    
    
class link(models.Model):
    under_leason = models.ForeignKey('lesson', on_delete=models.CASCADE)
    link_name = models.CharField('link name', blank=False, max_length=200)
    url_link = models.URLField('url link direction', null=False, blank=False)
    date_added = models.DateTimeField('date time link was added', default=timezone.now)
    
    def __str__(self):
        return self.link_name

            
        
    
    