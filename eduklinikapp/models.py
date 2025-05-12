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

class pro_image(models.Model):
    image = models.ImageField('user image', null=False, blank=False, upload_to='profile pics')
    is_edit = models.BooleanField('is edited', default=False)
    
    
    def __str__(self):
        return f'{self.image}'
    
    def save(self, *args, **kwargs):
        if self.is_edit == False:
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
                self.image = InMemoryUploadedFile(i_io, None, f'Blk_{rand_string_generator(10)}.webp', 'image/webp', None, None)

                self.is_edit = True 
           else:
               pass
        return super(pro_image, self).save(*args, **kwargs)

class profile(models.Model):

    acc_type = [
        ('Student','Student'),
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
    cos_count = models.BigIntegerField('course count', default=0)
    quz_count = models.BigIntegerField('quiz counr', default=0)
    profile_pics = models.ForeignKey('pro_image', on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField('user age ', default=0)  
    
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
    
class staff(models.Model):
    
    staff_typ = [
        ('Admin', 'Admin'),
        ('Teacher', 'Teacher'),
        ('Tutor', 'Tutor'),
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
        
        

class subject(models.Model):
    sub_name = models.CharField('cource_name eg mathematics english', null=True, max_length=200)
    
    def __str__(self):
        return self.sub_name

class course(models.Model):
    
    c_typ = [
        ('Core Academic Tracks', 'Core Academic Tracks'),
        ('Examination preperation', 'Examination preperation'),
        ('Skill development services', 'Skill development services'),
        ('Specialized services', 'Specialized services'),
    ]
    up_by = models.ForeignKey('staff', null=True, on_delete=models.PROTECT)
    course_subject = models.ForeignKey('subject', null=True, related_name='course', on_delete=models.CASCADE)
    course_name = models.CharField('course name assepts', null=True, blank=True, max_length=200)
    requiremwnt = models.CharField('requirments to partipate on this course', null=False, blank=True, max_length=1000)
    c_type = models.CharField('requirments to partipate on this course', null=False, blank=True, max_length=1000, choices=c_typ)
    lesson_count = models.BigIntegerField('number of leassons', default=0)
    meta_data = models.CharField('course meta decription', null=True, max_length=200)
    participant = models.BigIntegerField('number of students', default=0)
    weeks = models.CharField('specify how long it should take to complete the course', null=False, max_length=200, default='1 week')
    c_img = models.ImageField('add a image to decribe the corse', null=True, blank=True, max_length=200)
    pub_date = models.DateTimeField('date time of upload', default=timezone.now)
    bio = models.TextField('decription and article abour this course', null=True)
    tag = models.CharField('write tag and colms of what the skill give to the user eg *bacis knowleged, *health care', null=False, default='*basic,', max_length=200)
    c_str = models.CharField('course spec id', null=True, blank=True, max_length=200, unique=True)
    price = models.BigIntegerField('course price amount', default=0)
    drive_link = models.URLField('drive link of the course', null=True, blank=True, max_length=1000000)
    course_tralle = models.FileField('course trailer shot vedio', null=True, blank=True, upload_to='free_file')
    
    def __str__(self):
        return f'{str(self.course_subject)}'
    
    class Meta:
        ordering = ['-pub_date']

    def was_publised_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def save(self, *args, **kwargs):
        self.c_str = rand_string_generator(10)
        return super(course, self).save(*args, **kwargs)
        

class lesson(models.Model):
    
    l_typ = [
        ('Basic', 'Basic'),
        ('Advance', 'Advance'),
        ('Master', 'Master'),
    ]
    
    cls = [
        ('JAMB', 'JAMB'),
        ('WAEC', 'WAEC'),
        ('BECE', 'BECE'),
        ('Common entrance', 'Common entrance'),
    ]
    
    
    l_attr = [
        ('lesson note', 'lesson note'),
        ('past question', 'past question'),
        ('syllabue', 'syllabue'),
        ('textbook', 'textbook'),
        ('handout', 'handout'),
        ('pdf-ebook', 'pdf-ebook'),
    ]
    
    add_by = models.ForeignKey('staff', null=True, on_delete=models.PROTECT)
    under_course = models.ForeignKey('course', null=True, on_delete=models.CASCADE)
    ltitle = models.CharField('lesson name', blank=False, max_length=200)
    lesson_dic = models.TextField('write note and description of the lesson if in single', null=True, blank=True)
    lesson_str = models.CharField('leason spec id', null=True, blank=True, max_length=200, unique=True)
    lesson_img = models.ImageField('add a image to decribe the lesson', null=True, blank=True)
    lesson_tralle = models.FileField('lesson trailer shot vedio', null=True, blank=True, upload_to='free_file')
    lesson_level = models.CharField('leasson level', null=False, blank=True, choices=l_typ, default='Basic', max_length=200)
    class_level = models.CharField('leasson class', null=True, blank=True, choices=cls, default='', max_length=200)
    pub_date = models.DateTimeField('date time of upload', default=timezone.now)
    file_package = models.FileField('lesson file package', null=True, blank=True, upload_to='lesson_files')
    attribute = models.CharField('leasson artibute', null=True, max_length=200, choices=l_attr)
    price = models.BigIntegerField('course price amount', default=0)
    actton_btn = models.CharField('add a text to show in the button do not add the if file is cassifiled as the rest of others this is mainly for the single lesson page', null=True, blank=True, max_length=200)
    class Meta:
        ordering = ['-pub_date']

    def was_publised_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    

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
    
class quize(models.Model):
    quize_lesson = models.ForeignKey('lesson', verbose_name='leasson whit the quiz', on_delete=models.CASCADE)
    quize_str = models.CharField('quiz id to track do not add this', null=True, blank=True, max_length=500)
    
    def __str__(self):
        return f'{self.quize_lesson} ---- new lesson'
    
class quiz_question(models.Model):
    link_to = models.ForeignKey('quize', verbose_name='to the quiz the question is lined to', on_delete=models.CASCADE)
    question = models.CharField('quiz question', null=False, blank=False, max_length=2000)
    option_A = models.CharField('option A', null=False, blank=False, max_length=500)
    option_B = models.CharField('option B', null=False, blank=False, max_length=500)
    option_C = models.CharField('option C', null=False, blank=False, max_length=500)
    
    def __str__(self):
        return f'{self.link_to.quize_lesson} ------ question and option'
    
class user_answer(models.Model):
    the_question = models.ForeignKey('quiz_question', verbose_name='the question', on_delete=models.CASCADE)
    the_answer = models.CharField('the answer to the question', null=False, blank=False, max_length=500)
    is_corrent = models.BooleanField('if the answer is correct if not pls leave as node and recore the score in the score board', default=False)
    
    def __str__(self):
        return f''
    

class course_payment(models.Model):
    user = models.ForeignKey('profile', verbose_name='user payment get', on_delete=models.CASCADE)
    cours = models.ForeignKey('course', on_delete=models.CASCADE)
    amount = models.BigIntegerField('price to pay', default=0)
    payment_form = models.CharField('payment method', null=True, max_length=200)
    is_paid = models.BooleanField('if the course is paid', default=False)
    
    def __str__(self):
        return f'{self.user} --- new purchase'
    
class transaction(models.Model):
    amount = models.BigIntegerField('amount paid', default=0)
    email = models.EmailField('user email', null=True, blank=True)
    decript = models.CharField('payment decription', name=False, max_length=200)
    date = models.DateTimeField('date time of transaction', default=timezone.now)
    status = models.BooleanField('payment status', default=False)
    
    def __str__(self):
        return f'{self.tran_holder} ---- transaction'
    
class user_course(models.Model):
    course_holder = models.ForeignKey('profile', verbose_name='user holding the course', on_delete=models.CASCADE)
    main_course = models.ForeignKey('course', on_delete=models.CASCADE)
    date = models.DateTimeField('date and time course was added', default=timezone.now)
    
    class Meta:
        ordering = ['-date']

    def was_publised_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        return f'{self.course_holder} ---courses'
    
    def save(self, *args, **kwargs):
        
        pro = profile.objects.filter(user=self.course_holder.user).first()
        if pro:
            profile.objects.filter(user=self.course_holder.user).update(cos_count=F('cos_count') +1)
            pro.refresh_from_db()
        else:
            pass
        return super(user_course, self).save(*args, **kwargs)
        
    
class notification(models.Model):
    user = models.ForeignKey('profile', on_delete=models.CASCADE)
    msg = models.TextField('not message', null=True, max_length=200)
    is_new = models.BooleanField('if not is new', default=True)
    add_date = models.DateTimeField('date added', default=timezone.now) 
    
    class Meta:
        ordering = ['-add_date']

    def was_publised_recently(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)     
    
    def __str__(self):
        return f'{self.user} ---- new notification'
    
    def save(self, *args, **kwargs):
        if self.is_new == True:
            pro = profile.objects.filter(user=self.user.user).first()
            if pro:
                profile.objects.filter(user=self.user.user).update(not_counnt=F('not_count') +1)
                pro.refresh_from_db()
            else:
                pass
            return super(notification, self).save(*args, **kwargs)
        
class c_notification(models.Model):
    the_staff = models.ForeignKey('staff', on_delete=models.CASCADE)
    msg = models.TextField('not message', null=True, max_length=200)
    is_new = models.BooleanField('if not is new', default=True)      
    add_date = models.DateTimeField('date added', default=timezone.now)
    linked_to = models.URLField('place or page where the notification will direct to', null=True, blank=True )
    
    def __str__(self):
        return f'{self.the_staff} ---- new notification'
    
    class Meta:
        ordering = ['-add_date']

    def was_publised_recently(self):
        return self.add_date >= timezone.now() - datetime.timedelta(days=1)
    
    
class tech_msg(models.Model):
    teacher = models.ForeignKey('staff', on_delete=models.PROTECT)
    student = models.ForeignKey('profile', on_delete=models.CASCADE)
    img = models.ImageField('image post', null=True, blank=True)
    msg = models.TextField('message', null=False, blank=False)
    spec_str = models.CharField('linked to ', null=True, blank=True, max_length=200)
    is_linked = models.BooleanField('if teacher is linked already', default=False)
    video = models.FileField('video post', null=True, blank=True)
    date = models.DateTimeField('date and time of post', default=timezone.now)
    docs_file = models.FileField('document file', null=True, blank=True)
    
    def __str__(self):
        return f'{self.teacher} --- {self.student} --- private leason'


    
    
    