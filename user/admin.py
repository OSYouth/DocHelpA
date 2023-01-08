from django.contrib import admin
from .models import *
import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group, Permission

admin.site.site_header = '毕业设计'
admin.site.site_title = "test"

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'dept_name', 'last_name', 'first_name']
    search_fields = ['username']
    readonly_fields = ['username']
    # fields = ['username', ('last_name', 'first_name'), ('dept_name', 'major'),'title', ('phone', 'email'), 'sign']
    # 设置用户登录admin时只能看到自己录入的内容
    # https: // blog.csdn.net / xmy7007 / article / details / 122760597
    def get_queryset(self, request):
        qs = super(UserInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user)

@admin.register(InstructorBatch)
class InstructorBatchAdmin(admin.ModelAdmin):
    list_display = ['instructor_file']
    def add_view(self, request, form_url="", extra_context=None):
        if request.FILES.get('instructor_file'):
            file = request.FILES.get('instructor_file')
            if file.name.split(".")[-1] not in ['xls', 'xlsx']:
                extra_context = '上传文件格式错误'
                return redirect('/user/upload_error')
            user_data = pd.read_excel(file)
            # 用户组权限设置
            # 参考 https://www.cnblogs.com/55zjc/p/16544103.html
            group = Group.objects.filter(name="教师")
            if group: #  如果教师这个Group不存在
                view_userinfo = Permission.objects.get(codename='view_userinfo')
                change_userinfo = Permission.objects.get(codename='change_userinfo')
                group = Group.objects.create(name="教师")
                group.permissions.set([view_userinfo,change_userinfo])
            for i in range(user_data[pd.notnull(user_data['工号'])].shape[0]):
                create_instructor(group, user_data[pd.notnull(user_data['工号'])].iloc[i].to_dict())
            print(user_data)
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)


# Create your views here.
# 创建单个Instructor
def create_(group, dic):
    try:
        instructor = UserInfo.objects.create_user(username=dic.get('工号'), password='123456', first_name=dic.get('姓名')[1:],
                                         last_name=dic.get('姓名')[:1], dept_name=dic.get('部门'),
                                         ID_num=dic.get('身份证号码'), is_staff=1)
        group.user_set.add(instructor.id)
    except IntegrityError:  # 重复键值
        pass