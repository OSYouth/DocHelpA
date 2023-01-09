from django.contrib import admin
from .models import *
from user.models import UserInfo
import pandas as pd
import numpy as np
from django.db.utils import IntegrityError
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect

# 2.毕业设计选题上传
@admin.register(TopicBatch)
class TopicBatchAdmin(admin.ModelAdmin):
    list_display = ['topic_file']

    def add_view(self, request, form_url="", extra_context=None):
        if request.FILES.get('topic_file'):
            file = request.FILES.get('topic_file')
            if file.name.split(".")[-1] not in ['xls', 'xlsx']:
                extra_context = '上传文件格式错误'
                return redirect('/user/upload_error')
            stu_data = pd.read_excel(file)
            # 用户组权限设置
            # 参考 https://www.cnblogs.com/55zjc/p/16544103.html
            group = Group.objects.filter(name="学生")
            if len(group)==0:  # 如果学生这个Group不存在
                view_graduateprojectinfo = Permission.objects.get(codename='view_graduateprojectinfo')
                change_graduateprojectinfo = Permission.objects.get(codename='change_graduateprojectinfo')
                group = Group.objects.create(name="学生")
                group.permissions.set([view_graduateprojectinfo, change_graduateprojectinfo])
            for i in range(stu_data[pd.notnull(stu_data['学号'])].shape[0]):
                create_student(group, stu_data[pd.notnull(stu_data['学号'])].iloc[i].to_dict())
            # print(stu_data)
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)


# 3.毕业设计任务书模板设定
@admin.register(AssignmentTemplate)
class AssignmentTemplateAdmin(admin.ModelAdmin):
    list_display = ['instructor']
    readonly_fields = ['instruction','instructor']
    # fields = ['username', ('last_name', 'first_name'), ('dept_name', 'major'), 'title', ('phone', 'email'), 'sign']

    def get_queryset(self, request):
        qs = super(AssignmentTemplateAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor__username=request.user)

# 4.答辩安排信息表上传
@admin.register(DefenceBatch)
class DefenceBatchAdmin(admin.ModelAdmin):
    list_display = ['defence_file']

    def add_view(self, request, form_url="", extra_context=None):
        if request.FILES.get('defence_file'):
            file = request.FILES.get('defence_file')
            if file.name.split(".")[-1] not in ['xls', 'xlsx']:
                extra_context = '上传文件格式错误'
                return redirect('/user/upload_error')
            defence_data = pd.read_excel(file)
            for i in range(defence_data.shape[0]):
                create_defence_info(defence_data.iloc[i].to_dict())
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)


# 5.毕业设计信息完善（还有关键词要填）
@admin.register(GraduateProjectInfo)
class GraduateProjectInfoAdmin(admin.ModelAdmin):
    # AssignmentTemplate.objects.get()
    list_display = ['stu', 'class_name', 'topic','instructor']
    fields = [('topic', 'instructor'), ('class_name', 'stu'), ('dean', 'director'), 'key_word1', 'key_word2', 'key_word3', 'key_word4', 'key_word5', 'defence_image', 'self_report', 'quiz']
    readonly_fields = ['topic', 'class_name', 'instructor', 'stu']
    def get_queryset(self, request):
        qs = super(GraduateProjectInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif len(request.user.username) < 12:   #教师工号一般为5位，小于学号的12位
            return qs.filter(instructor = (request.user.last_name+request.user.first_name))
        return qs.filter(stu=request.user)

# 通过选题信息表格 创建单个学生用户，并在GraduateProjectInfo中添加相应信息
def create_student(group, dic):
    try:
        stu = UserInfo.objects.create_user(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:],
                                           last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'),
                                           is_staff=1, major=dic.get('专业'))
        group.user_set.add(stu.id)
        GraduateProjectInfo.objects.create(stu=stu, topic=dic.get('选题名称'), instructor=dic.get('指导老师'),
                                           class_name=dic.get('班级'), director=dic.get('专业教研室主任'), dean=dic.get('学院院长'))
    except IntegrityError:  # 重复键值
        pass

def create_defence_info(dic):
    try:
        DefenceInfo.objects.create(stu=UserInfo.objects.get(username=dic.get('学号')), design_type=dic.get("毕业设计类型"),
                                   defence_date=dic.get('答辩日期（格式2022年05月10日）'), defence_location=dic.get("答辩地点"),
                                   ach_grade=dic.get('成果成绩'), defence_grade=dic.get('答辩成绩'),
                                   final_grade=dic.get("最终成绩"), def_inst1=dic.get('答辩教师1'),
                                   def_inst2=dic.get('答辩教师2'), def_inst3=dic.get('答辩教师3'),
                                   def_inst4=dic.get('答辩教师4'), def_inst5=dic.get('答辩教师5'),
                                   def_inst6=dic.get('答辩教师6'))
    except IntegrityError:  # 重复键值
        pass
