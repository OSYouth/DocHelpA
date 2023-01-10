from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserInfo(AbstractUser):
    # 手机号码
    phone = models.CharField('手机号码', max_length=11, default='')
    # 部门/学院
    dept_name = models.CharField('部门/学院', max_length=50, default='')
    # 身份证号码
    ID_num = models.CharField('身份证号码', max_length=18, default='')
    # 签名照片
    sign = models.ImageField('签名照片', upload_to='sign_img/')
    # 充值积分
    charge_point = models.IntegerField('充值积分', default=0)
    # 赠送积分
    bonus_point = models.IntegerField('赠送积分', default=1200)
    # 备用字段
    in_case = models.CharField('备用字段', max_length=100, default='')
    # 教研室（教师）/专业（学生）
    major = models.CharField('教研室/专业', max_length=30, default='')
    # 职称（教师）
    title = models.CharField('职称', max_length=30, default='')
    class Meta:
        verbose_name = "1.用户信息"
        verbose_name_plural = verbose_name

class InstructorBatch(models.Model):
    instructor_file = models.FileField("教师信息文件", upload_to="instructor_info/")
    class Meta:
        verbose_name = "0.教师用户批量创建（管理员）"
        verbose_name_plural = verbose_name