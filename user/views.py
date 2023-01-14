from django.shortcuts import render, redirect
from .models import UserInfo
import pandas as pd
import numpy as np
from django.db.utils import IntegrityError
from django.http import HttpResponse, FileResponse, StreamingHttpResponse
import qrcode

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

def generate_vrcode(request):
    vstr = f'''
    BEGIN:VCARD
    VERSION:4.0
    N:{request.user.last_name}
    FN:{request.user.first_name}
    TITLE:{request.user.title}
    ORG:湖南商务职业技术学院{request.user.dept_name}
    TEL;CELL:(+86){request.user.phone}
    EMAIL;PREF;INTERNET:{request.user.email}
    END:VCARD
    '''

    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr.add_data(vstr)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(f'media/instructor_info/{request.user.last_name+request.user.first_name}.jpg')
    file = open(f'media/instructor_info/{request.user.last_name+request.user.first_name}.jpg', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={(request.user.last_name+request.user.first_name).encode("utf-8").decode("ISO-8859-1")}.jpg'
    return response
