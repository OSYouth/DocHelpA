from django.shortcuts import render
from django.http import FileResponse

def upload_success(request):
    message = request.session.pop('down_file', False)
    return render(request, 'upload_success.html', locals())

def upload_error(request):
    return render(request, 'upload_error.html')

def download_grade_analysis(request, name):
    file = open(f'media/grades_files/{name}', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={name}'
    return response

