# Create your views here.
import sys
sys.path.append('dependencies')
import os, os.path
import json

from django.http import HttpResponse
from django.template import Context, loader

#from article import ArticleData


def get_all_days():
    path = 'static_data'
    providers = os.listdir(path)
    articles_by_day = {}
    return providers


def index(request):
    t = loader.get_template('summary.html')
    c = Context({'providers':get_all_days()})
    return HttpResponse(t.render(c))