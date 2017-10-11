#!/bin/env python
#coding:utf-8
import sys
import os

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)
settings.configure(
  DEBUG = True,
  SECRET_KEY = '5u-c&(-h^m&fsit8^#+m#s)(0qn)v5^oh&4cj0*y#j1q_gfulx',
  ROOT_URLCONF = 'sitebuilder.urls',
  MIDDLEWARE_CLASSES=(),
  INSTALLED_APPS=(
    'django.contrib.staticfiles',
    'sitebuilder',
  ),
  ALLOWED_HOSTS=['127.0.0.1'],
  TEMPLATES=(
    {
      'BACKEND': 'django.template.backends.django.DjangoTemplates',
      'DIRS': [],
      'APP_DIRS': True,
    },
  ),
  STATIC_URL='/static/',
  SITE_PAGES_DIRECTORY=os.path.join(BASE_DIR,'pages'),
)
if __name__ == "__main__":
  from django.core.management import execute_from_command_line
  execute_from_command_line(sys.argv)