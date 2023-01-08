from django.db import models
from user.models import *

# Create your models here.
class TopicBatch(models.Model):
    topic_file = models.FileField("毕业设计选题文件", upload_to="topic_info/")
    class Meta:
        verbose_name = "毕业设计选题文件上传"
        verbose_name_plural = verbose_name

class GraduateProjectInfo(models.Model):
    # 选题名称（学生）
    topic = models.CharField('选题名称', max_length=30, default='')
    # 班级（学生）
    class_name = models.CharField('班级', max_length=30, default='')
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')
    instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')
    defence_image = models.ImageField("答辩影像", upload_to='defence_img/%Y/')
    self_report = models.TextField("学生自述内容")
    quiz = models.TextField("提问与回答")

# class AssignmentTemplate(models.Model):
#
#     instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')

class DefenceBatch(models.Model):
    defence_file = models.FileField("答辩安排信息表", upload_to="defence_info/")
    class Meta:
        verbose_name = "答辩安排信息表上传"
        verbose_name_plural = verbose_name

class DefenceInfo(models.Model):
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')
    design_type = models.CharField("毕业设计类型", max_length=20, default='')
    defence_date = models.DateField('答辩日期（格式2022年05月10日）')
    defence_location = models.CharField("答辩地点", max_length=20, default='')
    ach_grade = models.DecimalField('成果成绩', max_digits=3, decimal_places=2, default=0.0)
    defence_grade = models.DecimalField('答辩成绩', max_digits=3, decimal_places=2, default=0.0)
    defence_grade = models.CharField("最终成绩", max_length=5, default='')
    def_inst1 = models.CharField("答辩教师1", max_length=10, default='')
    def_inst2 = models.CharField("答辩教师2", max_length=10, default='')
    def_inst3 = models.CharField("答辩教师3", max_length=10, default='')
    def_inst4 = models.CharField("答辩教师4", max_length=10, default='')
    def_inst5 = models.CharField("答辩教师5", max_length=10, default='')
    def_inst6 = models.CharField("答辩教师6", max_length=10, default='')






