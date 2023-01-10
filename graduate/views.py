from django.shortcuts import render
from .models import *
from user.models import UserInfo
from docx import Document
from docx.shared import Pt,Cm    #字号
from docx.oxml.ns import qn    #字体
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING   #对齐
from docx.enum.table import WD_TABLE_ALIGNMENT    #对齐


# Create your views here.
# 生成要下载的压缩包
def download(request):
    # 根据指导老师、时间，按学号创建文件夹，并对每个学生生成4个文件
    # 根据指导老师、时间，按文件名创建文件夹，并生成指导老师名下所有的学生的文件
    generate_zdjlb(request.user.username)
# def download_grade_analysis(request, name):
#     file = open(f'media/grades_files/{name}', 'rb')
#     response = FileResponse(file)
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = f'attachment;filename={name}'
#     return response

# 生成毕业设计指导记录表
def generate_zdjlb(stu_no):
    stu = UserInfo.objects.get(username=stu_no)
    stu_project = GraduateProjectInfo.objects.get(stu=stu)
    word_name =stu_no + "+" + stu_project.class_name + "+" + stu.last_name + stu.first_name + "+毕业设计指导记录表.docx"
    word = Document()
    word.styles['Normal'].font.name = 'Arial'
    word.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    title = word.add_paragraph('湖南商务职业技术学院毕业设计指导记录表')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.bold = True
    table = word.add_table(rows=2, cols=6, style='Table Grid')
    table_cells = table.rows[0].cells
    table.rows[0].cells[0].text = '学生姓名'
    table.rows[0].cells[1].text = stu.last_name + stu.first_name
    table.rows[0].cells[2].text = '二级学院'
    table.rows[0].cells[3].text = stu.dept_name
    table.rows[0].cells[4].text = '班级名称'
    table.rows[0].cells[5].text = stu_project.class_name
    table.rows[1].cells[0].text = '专业名称'
    table.rows[1].cells[1].text = stu.major
    table.rows[1].cells[2].text = '学    号'
    table.rows[1].cells[3].text = stu_no
    table.rows[1].cells[4].text = '指导教师'
    table.rows[1].cells[5].text = stu_project.instructor
    table.add_row().cells

    word.save(f'media/download_files/{word_name}')