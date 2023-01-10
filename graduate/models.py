from django.db import models
from user.models import *

# 2.毕业设计选题文件上传，以创建学生用户信息、学生组，并填充必要的毕业设计项目信息GraduateProjectInfo
class TopicBatch(models.Model):
    topic_file = models.FileField("学生毕业设计选题文件", upload_to="topic_info/")
    class Meta:
        verbose_name = "2.学生毕业设计选题文件上传"
        verbose_name_plural = verbose_name

# 毕业设计任务书模板设定，一个老师一个模板
class AssignmentTemplate(models.Model):
    instruction = models.TextField('说明', max_length=300,
                                   default='''本页面提供毕业设计任务书模板的维护和学院公章的添加\n
                                           参考毕业设计任务书，在“一、毕业设计目标”需要替换关键字\n
                                           替换关键字由学生填写，设计留有最多5个关键字\n
                                           教师填写关键字前后的文本即可，空文本以“*”代替，无需修改\n
                                           可以下载本页底部的“毕业设计任务书模板.doc”参考
                                           ''')
    cachet = models.ImageField('学院公章', upload_to='cachet_img/')
    para1 = models.TextField('文本1', default='*')
    para2 = models.TextField('文本2', default='*')
    para3 = models.TextField('文本3', default='*')
    para4 = models.TextField('文本4', default='*')
    para5 = models.TextField('文本5', default='*')
    para6 = models.TextField('文本6', default='*')
    task_require = models.TextField('二、毕业设计任务及要求')
    step_way = models.TextField('三、毕业设计实施步骤和方法')
    schdeule = models.TextField('四、毕业设计进程安排', default='''1．选题：\t(%Y-1)年11月23日-(%Y-1)年11月27日\n
2．撰写开题提纲：\t(%Y-1)年11月30日-(%Y-1)年12月13日\n
3．收集资料及实施设计\t(%Y-1)年12月14日-%Y年2月28日\n
4．完成毕业设计初稿：\t%Y年3月1日前\n
5．完成毕业设计修改稿:\t%Y年3月30日前\n
6．完成毕业设计定稿：\t%Y年4月25日前\n
7．答辩：\t%Y年5月18日前\n''')
    thought = models.TextField('五、设计思路')
    result = models.TextField('六、成果表现形式')
    instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "3.毕业设计任务书模板"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.last_name + self.first_name

# 4.答辩安排信息表上传
class DefenceBatch(models.Model):
    defence_file = models.FileField("学生毕业答辩安排文件", upload_to="defence_info/")
    class Meta:
        verbose_name = "4.学生毕业答辩安排文件上传"
        verbose_name_plural = verbose_name

class DefenceInfo(models.Model):
    design_type = models.CharField("毕业设计类型", max_length=20, default='')
    defence_date = models.CharField('答辩日期（格式2022年05月10日）', max_length=30, default='')
    defence_location = models.CharField("答辩地点", max_length=30, default='')
    ach_grade = models.CharField('成果成绩', max_length=10, default='')
    defence_grade = models.CharField('答辩成绩', max_length=10, default='')
    final_grade = models.CharField("最终成绩", max_length=10, default='')
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')
    def_inst1 = models.CharField('答辩教师1', max_length=30, default='*')
    def_inst2 = models.CharField('答辩教师2', max_length=30, default='*')
    def_inst3 = models.CharField('答辩教师3', max_length=30, default='*')
    def_inst4 = models.CharField('答辩教师4', max_length=30, default='*')
    def_inst5 = models.CharField('答辩教师5', max_length=30, default='*')

# 5.毕业设计信息完善
class GraduateProjectInfo(models.Model):
    director = models.CharField('专业教研室主任', max_length=30, default='')
    dean = models.CharField('院长', max_length=30, default='')
    key_word1 = models.CharField('毕业设计评阅书关键替换字1', max_length=200, default='*')
    key_word2 = models.CharField('毕业设计评阅书关键替换字2', max_length=200, default='*')
    key_word3 = models.CharField('毕业设计评阅书关键替换字3', max_length=200, default='*')
    key_word4 = models.CharField('毕业设计评阅书关键替换字4', max_length=200, default='*')
    key_word5 = models.CharField('毕业设计评阅书关键替换字5', max_length=200, default='*')
    # 选题名称（学生）
    topic = models.CharField('选题名称', max_length=30, default='')
    # 班级（学生）
    class_name = models.CharField('班级', max_length=30, default='')
    defence_image = models.ImageField("答辩影像", upload_to='defence_img/%Y/')
    self_report = models.TextField("学生自述内容")
    quiz = models.TextField("提问与回答")
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    # instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    instructor = models.CharField('指导教师', max_length=30, default='')
    class Meta:
        verbose_name = "5.毕业设计信息完善（学生填写，教师可以修改）"
        verbose_name_plural = verbose_name

# 6.部门信息维护（了解怎么在一个model里面添加多个外键之后再优化）
# class Department(models.Model):
#     dept_name = models.CharField('部门', max_length=20, default='', primary_key=True)
#     dept_chief = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
#     cachet = models.ImageField('公章', max_length=200, default='')
#     class Meta:
#         verbose_name = "5.部门信息维护"
#         verbose_name_plural = verbose_name






