from django.db import models
from user.models import UserInfo

# Create your models here.
class AnalysisTemplate(models.Model):
    instruction = models.TextField('说明', max_length=300,
                                   default='''本页面提供 成绩分析单 和 教学质量分析 模板的维护\n
                                           ''')
    name = models.CharField('模板名', max_length=50, default='默认模板')
    comment = models.TextField('四、考试反映的问题及试卷评价', default='总体来说，学生成绩一般，还可以取得更好的成绩，实际动手能力还有待提高，试卷难度适中。')

    basic_condition = models.TextField('（一）班级教学情况分析\n1. 学生基本情况', default='上课期间大部分学生上课都比较积极和认真，在做例题和练习时，学生遇到问题都会及时向老师询问。考查采用学习通题库随机组卷的方式。')
    teaching_condition = models.TextField('（一）班级教学情况分析\n2. 教师教学情况', default='第一，积极向教学丰富的教师请教教学经验；第二，上课前认真备课，并且坚持课前演练；第三，针对学生素质不等，所以授课时要考虑整体情况，因材施教，既不能太快也不能太慢，更加不能太枯燥。')
    experience = models.TextField('（二）取得成功的经验及失误的教训分析', default='为了保证学生能够学会项目相关的知识，一定要在每讲完一个知识点后给学生理解和练习的时间，教师要走下讲堂，认真发现学生的问题，对于那些不会动手的学生要手把手教，把他们及时入门。')
    advice = models.TextField('（三）合理化建议',
                              default='1. 学生的思想教育很重要，技术再厉害，思想也要先行。\n'
                                      '2. 通过从提交的结果发现，在今后的教学过程中，需要更加注意细节；另外就是要注重逻辑思维的养成以及分析和解决问题的能力培养。\n'
                                      '3. 培养学生的实际动手能力很重要，要充分调动学生学习的积极性。\n')
    instructor = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='教师ID（本系统ID和工号可能不同，请勿修改）')

    class Meta:
        verbose_name = "2.分析 模板（包括成绩分析单 和 教学质量分析）"
        verbose_name_plural = verbose_name

        def __str__(self):
            return self.last_name + self.first_name

class GradesFiles(models.Model):
    dept_name = models.CharField('院部', max_length=50, default='')
    major = models.CharField('教研室', max_length=30, default='')
    template_id = models.ForeignKey(AnalysisTemplate, verbose_name='模板ID', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "3.学生成绩单上传"
        verbose_name_plural = verbose_name

