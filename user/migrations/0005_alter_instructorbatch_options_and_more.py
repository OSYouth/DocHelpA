# Generated by Django 4.1.4 on 2023-01-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_userinfo_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instructorbatch',
            options={'verbose_name': '教师信息文件', 'verbose_name_plural': '教师信息文件'},
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='dept_name',
            field=models.CharField(default='', max_length=50, verbose_name='部门/学院'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='sign',
            field=models.ImageField(upload_to='sign_img/', verbose_name='签名照片'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='title',
            field=models.CharField(default='', max_length=30, verbose_name='职称'),
        ),
    ]
