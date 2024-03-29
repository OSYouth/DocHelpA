# Generated by Django 4.1.4 on 2023-04-29 23:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction', models.TextField(default='本页面提供 成绩分析单 和 教学质量分析 模板的维护\n\n                                           ', max_length=300, verbose_name='说明')),
                ('name', models.CharField(default='模板名', max_length=50, verbose_name='模板名')),
                ('comment', models.TextField(default='总体来说，学生成绩一般，还可以取得更好的成绩，实际动手能力还有待提高，试卷难度适中。', verbose_name='四、考试反映的问题及试卷评价')),
                ('basic_condition', models.TextField(default='上课期间大部分学生上课都比较积极和认真，在做例题和练习时，学生遇到问题都会及时向老师询问。考查采用学习通题库随机组卷的方式。', verbose_name='（一）班级教学情况分析\n1. 学生基本情况')),
                ('teaching_condition', models.TextField(default='第一，积极向教学丰富的教师请教教学经验；第二，上课前认真备课，并且坚持课前演练；第三，针对学生素质不等，所以授课时要考虑整体情况，因材施教，既不能太快也不能太慢，更加不能太枯燥。', verbose_name='（一）班级教学情况分析\n2. 教师教学情况')),
                ('experience', models.TextField(default='为了保证学生能够学会项目相关的知识，一定要在每讲完一个知识点后给学生理解和练习的时间，教师要走下讲堂，认真发现学生的问题，对于那些不会动手的学生要手把手教，把他们及时入门。', verbose_name='（二）取得成功的经验及失误的教训分析')),
                ('advice', models.TextField(default='1. 学生的思想教育很重要，技术再厉害，思想也要先行。\n2. 通过从提交的结果发现，在今后的教学过程中，需要更加注意细节；另外就是要注重逻辑思维的养成以及分析和解决问题的能力培养。\n3. 培养学生的实际动手能力很重要，要充分调动学生学习的积极性。\n', verbose_name='（三）合理化建议')),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '2.分析 模板（包括成绩分析单 和 教学质量分析）',
                'verbose_name_plural': '2.分析 模板（包括成绩分析单 和 教学质量分析）',
            },
        ),
        migrations.CreateModel(
            name='GradesFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(default='', max_length=50, verbose_name='院部')),
                ('major', models.CharField(default='', max_length=30, verbose_name='教研室')),
                ('template_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grades.analysistemplate', verbose_name='模板ID')),
            ],
            options={
                'verbose_name': '3.学生成绩单上传',
                'verbose_name_plural': '3.学生成绩单上传',
            },
        ),
    ]
