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
    add_form_template = 'admin/graduate/topicbatch/add/add_topic.html'
    def add_view(self, request, form_url="", extra_context=None):
        if request.FILES.get('topic_file'):
            file = request.FILES.get('topic_file')
            if file.name.split(".")[-1] not in ['xls', 'xlsx']:
                extra_context = '上传文件格式错误'
                return redirect('/user/upload_error')
            stu_data = pd.read_excel(file).replace("\s+","",regex=True)
            # 用户组权限设置
            # 参考 https://www.cnblogs.com/55zjc/p/16544103.html
            group = Group.objects.filter(name="学生")
            if len(group)==0:  # 如果学生这个Group不存在
                view_graduateprojectinfo = Permission.objects.get(codename='view_graduateprojectinfo')
                change_graduateprojectinfo = Permission.objects.get(codename='change_graduateprojectinfo')
                group = Group.objects.create(name="学生")
                group.permissions.set([view_graduateprojectinfo, change_graduateprojectinfo])
            else:
                group = group[0]
            for i in range(stu_data[pd.notnull(stu_data['学号'])].shape[0]):
                create_student(group, stu_data[pd.notnull(stu_data['学号'])].iloc[i].to_dict())
            # print(stu_data)
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)

# 3.毕业设计任务书模板设定
@admin.register(AssignmentTemplate)
class AssignmentTemplateAdmin(admin.ModelAdmin):
    change_list_template = 'admin/graduate/assignmenttemplate/assignment_template_list.html'
    change_form_template = 'admin/graduate/assignmenttemplate/change_assignmenttemplate.html'
    list_display = ['id','instruction']
    readonly_fields = ['instruction', 'schdeule']
    fields = ['instruction', 'cachet', 'goal', 'task_require', 'step_way', 'schdeule', 'thought', 'result', 'comment', 'rws_date', 'instructor']
    def get_queryset(self, request):
        qs = super(AssignmentTemplateAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor__username=request.user)

    def get_changeform_initial_data(self, request):
        return {'instructor': request.user}

# 4.毕业设计指导记录表模板维护
@admin.register(GuideRecordTemplate)
class GuideRecordTemplateAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'instruction']
    readonly_fields = ['instruction']
    fields = ['instruction', ('guide_cont1', 'guide_date1', 'guide_loca1', 'guide_proc1'), ('guide_cont2', 'guide_date2', 'guide_loca2', 'guide_proc2'), ('guide_cont3', 'guide_date3', 'guide_loca3', 'guide_proc3', 'guide_date3_2', 'guide_loca3_2', 'guide_proc3_2',  'guide_date3_3', 'guide_loca3_3', 'guide_proc3_3', 'guide_date3_4', 'guide_loca3_4', 'guide_proc3_4')]
    def get_queryset(self, request):
        qs = super(GuideRecordTemplateAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(instructor__username=request.user)

# 5.答辩安排信息表上传
@admin.register(DefenceBatch)
class DefenceBatchAdmin(admin.ModelAdmin):
    list_display = ['defence_file']
    add_form_template = 'admin/graduate/defencebatch/add/add_defence.html'
    def add_view(self, request, form_url="", extra_context=None):
        if request.FILES.get('defence_file'):
            file = request.FILES.get('defence_file')
            if file.name.split(".")[-1] not in ['xls', 'xlsx']:
                extra_context = '上传文件格式错误'
                return redirect('/user/upload_error')
            defence_data = pd.read_excel(file).replace("\s+","",regex=True)
            for i in range(defence_data.shape[0]):
                create_defence_info(defence_data.iloc[i].to_dict())
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)

# 6.毕业设计信息完善（还有关键词要填）
@admin.register(GraduateProjectInfo)
class GraduateProjectInfoAdmin(admin.ModelAdmin):
    change_list_template = 'admin/graduate/graduateprojectinfo/info_list.html'
    list_display = ['stu', 'class_name', 'dean', 'director', 'instructor', 'topic', 'key_word1', 'key_word2', 'key_word3', 'key_word4', 'key_word5', 'defence_image', 'self_report', 'quiz']
    list_editable = ['topic', 'key_word1', 'key_word2', 'key_word3', 'key_word4', 'key_word5', 'self_report', 'quiz']
    # list_display_links = ['stu']
    fields = ['topic', ('class_name', 'stu'), ('dean', 'director', 'instructor'), 'key_word1', 'key_word2', 'key_word3', 'key_word4', 'key_word5', 'defence_image', 'self_report', 'quiz']
    readonly_fields = [ 'class_name', 'instructor', 'stu']
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
        stu = UserInfo.objects.create_user(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:], last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'), is_staff=1, major=dic.get('专业'), title='ungraduate')
        group.user_set.add(stu.id)
        GraduateProjectInfo.objects.create(stu=stu, topic=dic.get('选题名称'), instructor=dic.get('指导老师'), class_name=dic.get('班级'), director=dic.get('专业教研室主任'), dean=dic.get('学院院长'))
    except IntegrityError:  # 重复键值
        # 为当年毕设没过的同学设计：可能指导教师已经创建了该学生，然后存在系统用户当中了
        # UserInfo.objects.update_or_create(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:], last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'), is_staff=1, major=dic.get('专业'), title='ungraduate')
        pass

def create_defence_info(dic):
    try:
        DefenceInfo.objects.update_or_create(stu=UserInfo.objects.get(username=dic.get('学号')), design_type=dic.get("毕业设计类型"), defence_date=dic.get('答辩日期（格式2022年05月10日）'), defence_location=dic.get("答辩地点"), recorder=dic.get('记录人'), ach_grade=dic.get('成果成绩'), defence_grade=dic.get('答辩成绩'), final_grade=dic.get("最终成绩"), def_inst1=dic.get('答辩教师1'), def_inst2=dic.get('答辩教师2'), def_inst3=dic.get('答辩教师3'), def_inst4=dic.get('答辩教师4'), def_inst5=dic.get('答辩教师5'), assignment_template_id=dic.get('任务书模板ID'))
    except IntegrityError:  # 重复键值
        pass

