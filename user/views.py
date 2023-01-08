from django.shortcuts import render, redirect
from .models import UserInfo
import pandas as pd
import numpy as np
from django.db.utils import IntegrityError


# Create your views here.
# 创建单个用户
def create_user(dic):
    if '工号' in dic.keys():
        try:
            UserInfo.objects.create_user(username=dic.get('工号'), password='123456', first_name=dic.get('姓名')[1:],
                                         last_name=dic.get('姓名')[:1], dept_name=dic.get('部门'),
                                         ID_num=dic.get('身份证号码'), is_staff=1)
        except IntegrityError: # 重复键值
            pass
    else:
        try:
            UserInfo.objects.create_user(username=dic.get('学号'), password='123456', first_name=dic.get('姓名')[1:],
                                 last_name=dic.get('姓名')[:1], dept_name=dic.get('学院'), title=dic.get('选题名称'),
                                 sign=dic.get('指导老师'), major=dic.get('专业'), in_case=dic.get('班级'))
        except IntegrityError:  # 重复键值
            pass

def batch_create_user(request):
    if request.method == 'GET':
        return render(request, 'upload_user_list.html')
    elif request.method == 'POST':
        # files = request.FILES.getlist('grades_file')
        file = request.FILES.get('user_list')
        user_data = pd.read_excel(file)
        # print(user_data)
        for i in range(user_data[pd.notnull(user_data['工号'])].shape[0]):
            create_user(user_data[pd.notnull(user_data['工号'])].iloc[i].to_dict())
        return redirect('http://127.0.0.1:8000/admin')

def upload_error(request):
    return render(request, 'upload_error.html')
