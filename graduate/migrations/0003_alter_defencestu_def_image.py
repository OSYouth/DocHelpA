# Generated by Django 4.1.4 on 2023-01-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduate', '0002_defencestu_stu_alter_defencestu_quiz_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defencestu',
            name='def_image',
            field=models.ImageField(upload_to='sign_img/', verbose_name='答辩影像'),
        ),
    ]
