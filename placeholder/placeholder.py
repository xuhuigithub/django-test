#!/bin/env python
#coding:utf-8
import os
import sys

from django.conf import settings
from django import forms
DEBUG = os.environ.get('DEBUG','on') == 'on'
SCRET_KEY = os.environ.get('SECRET_KEY','5u-c&(-h^m&fsit8^#+m#s)(0qn)v5^oh&4cj0*y#j1q_gfulx')
#SCRET_KEY = os.environ.get('SECRET_KEY',os.urandom(32))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS','localhost').split(',')
BASE_DIR = os.path.dirname(__file__)

settings.configure(
  DEBUG=DEBUG,
  SCRET_KEY = SCRET_KEY,
  ALLOWED_HOSTS = ALLOWED_HOSTS,
  ROOT_URLCONF = __name__,
  MIDDLEWARE_CLASSES=(
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  ),
  INSTALLED_APPS = (
    'django.contrib.staticfiles',
  ),
  TEMPLATES = (
    {
      'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': (os.path.join(BASE_DIR,'templates'),),
    },
  ),
  STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
  ),
  STATIC_URL = '/static/',
),





from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse,HttpResponseBadRequest
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.cache import cache
from django.views.decorators.http import etag
from django.core.urlresolvers import reverse
from django.shortcuts import render
import hashlib

def generate_etag(request,width,height):
  content = 'Placeholder: {0} x {1}'.format(width,height)
  return hashlib.sha1(content.encode('utf-8')).hexdigest()

class ImageForm(forms.Form):
  height = forms.IntegerField(min_value=1,max_value=2000)
  width = forms.IntegerField(min_value=1,max_value=2000)

  def generate(self,image_format='PNG'):
    height = self.cleaned_data['height']
    width = self.cleaned_data['width']
    key = '{}.{}.{}'.format(width,height,image_format)
    content = cache.get(key)
    if content is None:
      image = Image.new('RGB',(width,height))
      draw = ImageDraw.Draw(image)
      text = '{} X {}'.format(width,height)
      textwidth,textheight = draw.textsize(text)
      if textwidth < width and textheight < height:
        texttop = (height - textheight) // 2
        textleft = (width - textwidth) // 2
        #文字距离应距离左边的位置
        draw.text((textleft,texttop),text,fill=(255,255,255))
        #draw.text的第一个参数是一个数组，写有x轴y轴的值，这个图片生成出来的文字在中间
      content = BytesIO()
      image.save(content,image_format)
      content.seek(0)
      cache.set(key,content,60 * 60)
    return content

#因为在HTTP协议规定中Etag的hash值没有规定的算法，所以这里我们可以自定义算法生成hash

@etag(generate_etag)
#generate是个新函数接受placeholder的参数
def placeholder(request,width,height):
  form = ImageForm({'height':height,'width':width})
  #给表单传值，让表单做验证
  if form.is_valid():
    image = form.generate()
    return HttpResponse(image,content_type='image/png')
  else:
    return HttpResponseBadRequest('Invalid Image Request')

def index(request):
  example = reverse('placeholder',kwargs={'width':50,'height':50})
  #这个placeholder就是url中的name参数
  content = {
    'example': request.build_absolute_uri(example)
  }
  return render(request,'home.html',content)
urlpatterns = (
  url(r'^$',index,name='homepage'),
  url(r'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$',placeholder,name='placeholder'),
)

application = get_wsgi_application()

if __name__ == "__main__":
  from django.core.management import execute_from_command_line
  execute_from_command_line(sys.argv)
