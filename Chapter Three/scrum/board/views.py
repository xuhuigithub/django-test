#!/bin/env python
#coding:utf-8
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import SprintSerializer,UserSerializer,TaskSerializer
from rest_framework import viewsets,authentication,permissions,filters
from .models import Sprint,Task
from .filter import TaskFilter
# Create your views here.
User = get_user_model()
class DefaultsMixin(object):
  #继承这个类，继承权限要求
  authentication_classes = (
    authentication.BasicAuthentication,
    authentication.TokenAuthentication,
  )
  permission_classes = (
    permissions.IsAuthenticated,
  )

  filter_backends = (
    filters.DjangoFilterBackend,
    filters.SearchFilter,
    filters.OrderingFilter,
  )
  paginate_by = 25
  paginate_by_param = '40'
  max_paginate_by = 100



class SprintViewSet(DefaultsMixin,viewsets.ModelViewSet):
  # lookup_field = 'name'
  # lookup_url_kwarg = 'name'
  #默认为pk 可以设置为其他字段，这pk不会是primary key的意思吧。。。。
  queryset = Sprint.objects.order_by('end')
  serializer_class = SprintSerializer
  search_fields = ('name',)
  ordering_fields = ('end','name',)

class TaskViewSet(DefaultsMixin,viewsets.ModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer
  filter_class = TaskFilter
  search_fields = ('name',)
  ordering_fields = ('name','order','started','completed')


class UserViewSet(DefaultsMixin,viewsets.ReadOnlyModelViewSet):
  lookup_field = User.USERNAME_FIELD
  lookup_url_kwarg = User.USERNAME_FIELD
  queryset = User.objects.order_by(User.USERNAME_FIELD)
  serializer_class = UserSerializer
  search_fields = (User.USERNAME_FIELD,)

