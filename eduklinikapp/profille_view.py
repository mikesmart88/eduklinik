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