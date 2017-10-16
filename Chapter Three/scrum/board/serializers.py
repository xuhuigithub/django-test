#!/bin/env python
#coding:utf-8
from rest_framework import serializers
from .models import Sprint,Task
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

User = get_user_model()

class SprintSerializer(serializers.ModelSerializer):
  links = serializers.SerializerMethodField()
  class Meta:
    model = Sprint
    fields = ('id','name','description','end','links',)
  def get_links(self,obj):
    request = self.context['request']
    return {
      'self':reverse('sprint-detail',kwargs={'pk':obj.pk},request=request)
      #{'pk':obj.pk} 对应的是Viewset中的lookup字段
    }

class TaskSerializer(serializers.ModelSerializer):
  assigned = serializers.SlugRelatedField(
    slug_field=User.USERNAME_FIELD,required=False,allow_null= True,
    queryset=User.objects.all()
  )
  # sprint = serializers.SlugRelatedField(
  #   slug_field= 'name',required=False,read_only=True,allow_null=True
  # )
  links = serializers.SerializerMethodField()
  status_display = serializers.SerializerMethodField()
  #这个字段必须包换在Meta类中的fields中
  class Meta:
    model = Task
    fields = ('id','name','sprint','status',
              'status_display','order','assigned','started','completed','links'
              )
  def get_status_display(self,obj):
    #status_display与上边的fields中定义的字段名有关联
    return obj.get_status_display()

  def get_links(self,obj):
    request = self.context['request']
    links =  {
      'self':reverse('task-detail',kwargs={'pk':obj.pk},request=request),
      'sprint': None,
      'assigned': None,
    }
    if obj.sprint_id:
      links['sprint'] = reverse('sprint-detail',kwargs={'pk':obj.sprint_id},request=request)
    if obj.assigned:
      links['assigned'] = reverse('user-detail',kwargs={User.USERNAME_FIELD:obj.assigned},request=request)
    return links

class UserSerializer(serializers.ModelSerializer):
  full_name = serializers.CharField(source='get_full_name',read_only=True)
  links = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ('id',User.USERNAME_FIELD,'full_name','is_active','links',)

  def get_links(self,obj):
    request = self.context['request']
    username = obj.get_username()
    return {
      'self': reverse('user-detail',
                      kwargs={User.USERNAME_FIELD: username},request=request),
    }