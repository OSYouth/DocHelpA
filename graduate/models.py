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
                                           毕业设计任务书中“一、毕业设计目标”一般会随论文主题不同而无法统一\n
                                           因此在“一、毕业设计目标”提供支持替换部分关键内容的功能\n
                                           为减少负担，设计“一、毕业设计目标”的模板在教师维护后，替换部分内容建议由学生在第6步填写，教师可以修改和填写\n
                                           替换部分以'*'表示，最多支持5个，请确保替换部分顺序一致\n
                                           毕业设计任务书模板默认以大数据技术专业为例显示
                                           ''')
    cachet = models.ImageField('学院公章', upload_to='cachet_img/')
    goal = models.TextField('一、毕业设计目标', default='设计的目的在于考察学生利用大数据技术与应用专业知识进行大数据项目数据采集、处理及分析展示的能力。在指导教师的指导下，根据选择的毕业设计课题，获*的相关数据，利用大数据专业知识进行数据分析，并使用数据可视化技术对数据进行展示，为*')
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
    instructor = models.ForeignKey(UserInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "3.毕业设计任务书模板（如果只有一种模板，建议直接点击修改）"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.last_name + self.first_name

# 4. 毕业设计指导记录表模板
class GuideRecordTemplate(models.Model):
    instruction = models.TextField('说明', max_length=300,
                                   default='''本页面提供毕业设计指导记录表模板的维护\n
                                              如果指导过程比较固定，一般来说修改一次以后无需再次修改\n
                                              毕业设计指导记录表中的答辩一栏会根据第5步答辩信息表自动生成，无需填写''')
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
    guide_date3 = models.CharField('指导时间3_1', max_length=30, default=f'{time.localtime().tm_year}年2月28日')
    guide_loca3 = models.CharField('指导地点3_1', max_length=50, default='网络通信工具')
    guide_proc3 = models.TextField('指导过程记录3_1',
                                   default='上交初稿，指导老师审核初稿并提出修改意见，学生按照意见修改初稿')
    guide_cont3_2 = models.CharField('指导内容3_2', max_length=30, default='')
    guide_date3_2 = models.CharField('指导时间3_2', max_length=30, default=f'{time.localtime().tm_year}年3月30日')
    guide_loca3_2 = models.CharField('指导地点3_2', max_length=50, default='网络通信工具')
    guide_proc3_2 = models.TextField('指导过程记录3_2',
                                   default='在初稿的基础上根据指导老师意见进行完善，上交第一次修改稿，老师审核后提出改进意见，并按照修改意见进行完善')
    guide_cont3_3 = models.CharField('指导内容3_3', max_length=30, default='')
    guide_date3_3 = models.CharField('指导时间3_3', max_length=30, default=f'{time.localtime().tm_year}年5月7日')
    guide_loca3_3 = models.CharField('指导地点3_3', max_length=50, default='网络通信工具')
    guide_proc3_3 = models.TextField('指导过程记录3_3',
                                   default='在第一次修改稿的基础上进行完善，上交第二次修改稿，老师审核提出完善意见，并按照意见进行修改')
    guide_cont3_4 = models.CharField('指导内容3_4', max_length=30, default='')
    guide_date3_4 = models.CharField('指导时间3_4', max_length=30, default=f'{time.localtime().tm_year}年5月13日')
    guide_loca3_4 = models.CharField('指导地点3_4', max_length=50, default='网络通信工具')
    guide_proc3_4 = models.TextField('指导过程记录3_4', default='对毕业设计文档内容及格式进行完善，并进行查重，上交最终稿')
    instructor = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "4. 毕业设计指导记录表模板"
        verbose_name_plural = verbose_name


# 5.答辩安排信息文件上传
class DefenceBatch(models.Model):
    defence_file = models.FileField("学生毕业答辩信息文件", upload_to="defence_info/")

    class Meta:
        verbose_name = "5.学生毕业答辩信息文件上传"
        verbose_name_plural = verbose_name


class DefenceInfo(models.Model):
    design_type = models.CharField("毕业设计类型", max_length=20, default='')
    defence_date = models.CharField('答辩日期（格式2022年05月10日）', max_length=30, default='')
    defence_location = models.CharField("答辩地点", max_length=30, default='')
    recorder = models.CharField('记录人', max_length=30, default='')
    ach_grade = models.CharField('成果成绩', max_length=10, default='')
    defence_grade = models.CharField('答辩成绩', max_length=10, default='')
    final_grade = models.CharField("最终成绩", max_length=10, default='')
    def_inst1 = models.CharField('答辩教师1', max_length=30, default='*')
    def_inst2 = models.CharField('答辩教师2', max_length=30, default='*')
    def_inst3 = models.CharField('答辩教师3', max_length=30, default='*')
    def_inst4 = models.CharField('答辩教师4', max_length=30, default='*')
    def_inst5 = models.CharField('答辩教师5', max_length=30, default='*')
    assignment_template_id = models.CharField('任务书模板ID',  max_length=30, default='')
    stu = models.OneToOneField(UserInfo, on_delete=models.CASCADE)

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
