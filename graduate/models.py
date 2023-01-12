from django.db import models
from user.models import *
import time


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
    schdeule = models.TextField('四、毕业设计进程安排',
                                default=f'''1．选题：\t{time.localtime().tm_year - 1}年11月23日-{time.localtime().tm_year - 1}年11月27日
                                            2．撰写开题提纲：\t{time.localtime().tm_year - 1}年11月30日-{time.localtime().tm_year - 1}年12月13日
                                            3．收集资料及实施设计\t{time.localtime().tm_year - 1}年12月14日-{time.localtime().tm_year}年2月28日
                                            4．完成毕业设计初稿：\t{time.localtime().tm_year}年3月1日前
                                            5．完成毕业设计修改稿:\t{time.localtime().tm_year}年3月30日前
                                            6．完成毕业设计定稿：\t{time.localtime().tm_year}年4月25日前
                                            7．答辩：\t{time.localtime().tm_year}年5月18日前''')
    thought = models.TextField('五、设计思路')
    result = models.TextField('六、成果表现形式')
    comment = models.TextField('指导教师意见', default='')
    rws_date = models.CharField('任务书落款日期', max_length=30, default=f'{time.localtime().tm_year - 1}年12月10日')
    instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "3.毕业设计任务书模板"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.last_name + self.first_name


# 4. 毕业设计指导记录表模板
class GuideRecordTemplate(models.Model):
    instruction = models.TextField('说明', max_length=300,
                                   default='''本页面提供毕业设计指导记录表模板的维护\n
                                               一般来说修改一次以后无需再修改''')
    guide_cont1 = models.CharField('指导内容1', max_length=30, default='毕业设计选题')
    guide_date1 = models.CharField('指导时间1', max_length=30, default=f'{time.localtime().tm_year - 1}年11月23日')
    guide_loca1 = models.CharField('指导地点1', max_length=50, default='网络通信工具')
    guide_proc1 = models.TextField('指导过程记录1',
                                   default='指导学生选题，讲解选题需要完成的工作内容，并下发毕业设计指南及模板')
    guide_cont2 = models.CharField('指导内容2', max_length=30, default='毕业设计工作计划')
    guide_date2 = models.CharField('指导时间2', max_length=30, default=f'{time.localtime().tm_year - 1}年11月30日')
    guide_loca2 = models.CharField('指导地点2', max_length=50, default='网络通信工具')
    guide_proc2 = models.TextField('指导过程记录2', default='下发毕业设计任务书，并指导学生制定毕业设计工作计划')
    guide_cont3 = models.CharField('指导内容3', max_length=30, default='毕业设计过程')
    guide_date3 = models.CharField('指导时间3', max_length=30, default=f'{time.localtime().tm_year}年2月28日')
    guide_loca3 = models.CharField('指导地点3', max_length=50, default='网络通信工具')
    guide_proc3 = models.TextField('指导过程记录3',
                                   default='上交初稿，指导老师审核初稿并提出修改意见，学生按照意见修改初稿')
    guide_cont4 = models.CharField('指导内容4', max_length=30, default='')
    guide_date4 = models.CharField('指导时间4', max_length=30, default=f'{time.localtime().tm_year}年3月30日')
    guide_loca4 = models.CharField('指导地点4', max_length=50, default='网络通信工具')
    guide_proc4 = models.TextField('指导过程记录4',
                                   default='在初稿的基础上根据指导老师意见进行完善，上交第一次修改稿，老师审核后提出改进意见，并按照修改意见进行完善')
    guide_cont5 = models.CharField('指导内容5', max_length=30, default='')
    guide_date5 = models.CharField('指导时间5', max_length=30, default=f'{time.localtime().tm_year}年5月7日')
    guide_loca5 = models.CharField('指导地点5', max_length=50, default='网络通信工具')
    guide_proc5 = models.TextField('指导过程记录5',
                                   default='在第一次修改稿的基础上进行完善，上交第二次修改稿，老师审核提出完善意见，并按照意见进行修改')
    guide_cont6 = models.CharField('指导内容6', max_length=30, default='毕业设计选题')
    guide_date6 = models.CharField('指导时间6', max_length=30, default=f'{time.localtime().tm_year}年5月13日')
    guide_loca6 = models.CharField('指导地点6', max_length=50, default='网络通信工具')
    guide_proc6 = models.TextField('指导过程记录6', default='对毕业设计文档内容及格式进行完善，并进行查重，上交最终稿')
    instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "4. 毕业设计指导记录表模板"
        verbose_name_plural = verbose_name


# 5.答辩安排信息表上传
class DefenceBatch(models.Model):
    defence_file = models.FileField("学生毕业答辩安排文件", upload_to="defence_info/")

    class Meta:
        verbose_name = "5.学生毕业答辩安排文件上传"
        verbose_name_plural = verbose_name


class DefenceInfo(models.Model):
    design_type = models.CharField("毕业设计类型", max_length=20, default='')
    defence_date = models.CharField('答辩日期（格式2022年05月10日）', max_length=30, default='')
    defence_location = models.CharField("答辩地点", max_length=30, default='')
    recorder = models.CharField('记录人', max_length=30, default='*')
    ach_grade = models.CharField('成果成绩', max_length=10, default='')
    defence_grade = models.CharField('答辩成绩', max_length=10, default='')
    final_grade = models.CharField("最终成绩", max_length=10, default='')
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE, default='')
    def_inst1 = models.CharField('答辩教师1', max_length=30, default='*')
    def_inst2 = models.CharField('答辩教师2', max_length=30, default='*')
    def_inst3 = models.CharField('答辩教师3', max_length=30, default='*')
    def_inst4 = models.CharField('答辩教师4', max_length=30, default='*')
    def_inst5 = models.CharField('答辩教师5', max_length=30, default='*')

# 6.毕业设计信息完善
class GraduateProjectInfo(models.Model):
    director = models.CharField('专业教研室主任', max_length=30, default='')
    dean = models.CharField('院长', max_length=30, default='')
    key_word1 = models.CharField('毕业设计评阅书替换字1', max_length=200, default='*')
    key_word2 = models.CharField('毕业设计评阅书替换字2', max_length=200, default='*')
    key_word3 = models.CharField('毕业设计评阅书替换字3', max_length=200, default='*')
    key_word4 = models.CharField('毕业设计评阅书替换字4', max_length=200, default='*')
    key_word5 = models.CharField('毕业设计评阅书替换字5', max_length=200, default='*')
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
        verbose_name = "6.毕业设计信息完善（学生填写，教师可以修改）"
        verbose_name_plural = verbose_name

# 7.部门信息维护（了解怎么在一个model里面添加多个外键之后再优化）
# class Department(models.Model):
#     dept_name = models.CharField('部门', max_length=20, default='', primary_key=True)
#     dept_chief = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
#     cachet = models.ImageField('公章', max_length=200, default='')
#     class Meta:
#         verbose_name = "5.部门信息维护"
#         verbose_name_plural = verbose_name
