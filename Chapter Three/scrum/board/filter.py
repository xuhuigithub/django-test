#!/bin/env python
#coding:utf-8

import django_filters
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()


class NullFilter(django_filters.BooleanFilter):
  def filter(self,qs,value):
    if value is not None:
      return qs.filter(**{'%s__isnull' %self.name: value})
    return qs
#NullFilter用来过滤所有sprint(name参数值)为空的的task
#例如：http://127.0.0.1:10800/api/tasks/?backlog=True

class TaskFilter(django_filters.FilterSet):
  backlog = NullFilter(name='sprint')
  class Meta:
    model = Task
    fields = ('order','sprint','backlog','assigned',)
    #定义过滤字段例如http://127.0.0.1:10800/api/tasks/?order=11011
    #注意这个assgined 如果我们在浏览器中输入http://127.0.0.1:10800/api/tasks/?assigned=UserName，是不会有返回值的，因为User
    #只有当我们输入http://127.0.0.1:10800/api/tasks/?assigned=UserID时才会有返回值
    #下边的代码帮我们解决了这个问题

  def __init__(self,*args,**kwargs):
    super(TaskFilter,self).__init__(*args,**kwargs)
    self.filters['assigned'].extra.update(
      {'to_field_name':User.USERNAME_FIELD}
    )
