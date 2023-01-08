from django.contrib import admin
from .models import *

admin.site.site_header = '毕业设计助手'

# Register your models here.
@admin.register(GraduateProjectInfo)
class GraduateProjectInfoManager(admin.ModelAdmin):
    list_display = [ 'self_report', 'quiz']
    readonly_fields = ['topic', 'class_name', 'instructor']
    # fields = ['def_image',  'self_report', 'quiz']

@admin.register(InstructorBatch)
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
            if group: #  如果学生这个Group不存在
                view_userinfo = Permission.objects.get(codename='view_graduateprojectinfo')
                change_userinfo = Permission.objects.get(codename='change_graduateprojectinfo')
                group = Group.objects.create(name="学生")
                group.permissions.set([view_graduateprojectinfo,change_graduateprojectinfo])
            for i in range(stu_data[pd.notnull(stu_data['学号'])].shape[0]):
                create_student(group, stu_data[pd.notnull(stu_data['学号'])].iloc[i].to_dict())
            print(stu_data)
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)

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
            # 用户组权限设置
            # 参考 https://www.cnblogs.com/55zjc/p/16544103.html
            group = Group.objects.filter(name="教师")
            # if group: #  如果学生这个Group不存在
            #     view_userinfo = Permission.objects.get(codename='view_graduateprojectinfo')
            #     change_userinfo = Permission.objects.get(codename='change_graduateprojectinfo')
            #     group = Group.objects.create(name="教师")
            #     group.permissions.set([view_graduateprojectinfo,change_graduateprojectinfo])
            for i in range(defence_data[pd.notnull(defence_data['学号'])].shape[0]):
                create_defence_info(group, defence_data[pd.notnull(defence_data['学号'])].iloc[i].to_dict())
            extra_context = '上传成功'
        return self.changeform_view(request, None, form_url, extra_context)

# 通过选题信息表格 创建单个学生用户
def create_student(group, dic):
    try:
        stu = UserInfo.objects.create_user(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:],
                                     last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'),
                                     is_staff=1, major=dic.get('专业'))
        group.user_set.add(stu.id)
        GraduateProjectInfo.objects.create(stu=stu, topic=dic.get('选题名称'), instructor=dic.get('指导老师'), class_name=dic.get('班级'))
    except IntegrityError:  # 重复键值
        pass

def crecreate_defence_info(group, dic):
    try:
        stu = UserInfo.objects.create_user(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:],
                                     last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'),
                                     is_staff=1, major=dic.get('专业'))
        group.user_set.add(stu.id)
        GraduateProjectInfo.objects.create(topic = dic.get('选题名称'), instructor=dic.get('指导老师'), class_name=dic.get('班级'))
    except IntegrityError:  # 重复键值
        pass