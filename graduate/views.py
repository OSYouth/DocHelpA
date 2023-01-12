from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .models import *
from user.models import UserInfo
from docx import Document
from docx.shared import Pt,Cm    #字号
from docx.oxml.ns import qn    #字体
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING   #对齐
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT    #对齐
import time
import pandas as pd
import numpy as np

# Create your views here.
# 生成要下载的压缩包
def download(request):
    # 根据指导老师、时间，按学号创建文件夹，并对每个学生生成4个文件
    # 根据指导老师、时间，按文件名创建文件夹，并生成指导老师名下所有的学生的文件
    # name = generate_zdjlb('201904040111', '00530')
    # name = generate_pyb('201904040111', '00530')
    name = generate_rws('201904040111', '00530')
    return render(request, 'upload_success.html', locals())

def download_test(request, name):
    file = open(f'media/download_files/{name}', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={name}'
    return response

# 生成毕业设计任务书
def generate_rws(stu_no, inst_no):
    stu = UserInfo.objects.get(username=stu_no)
    inst = UserInfo.objects.get(username=inst_no)
    stu_project = GraduateProjectInfo.objects.get(stu=stu)
    stu_defence = DefenceInfo.objects.get(stu=stu)
    temp = AssignmentTemplate.objects.get(instructor=inst)
    word_name = stu_no + "+" + stu_project.class_name + "+" + stu.last_name + stu.first_name + "+毕业设计答辩记录表.docx"
    word = Document()
    # 先对于文档英文为Arial，中文为宋体所有字体设置为小四，所有字体设置为小四，
    word.styles['Normal'].font.name = 'Arial'
    word.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    word.styles['Normal'].font.size = Pt(12)
    word.sections[0].left_margin = Cm(2.1)
    word.sections[0].right_margin = Cm(2.1)
    title = word.add_paragraph('湖南商务职业技术学院毕业设计任务书')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.bold = True
    table = word.add_table(rows=9, cols=6, style='Table Grid')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 表头前三行对齐格式统一
    align_cccccl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    row1 = []    #第1行的元素值用列表存储
    row1.append('学生姓名')
    row1.append(stu.last_name + stu.first_name)
    row1.append('二级学院')
    row1.append(stu.dept_name)
    row1.append('班级名称')
    row1.append(stu_project.class_name)
    for cell, align, ele in zip(table.rows[0].cells, align_cccccl, row1):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row2 = []  # 第2行的元素值用列表存储
    row2.append('专业名称')
    row2.append(stu.major)
    row2.append('学      号')
    row2.append(stu_no)
    row2.append('指导教师')
    row2.append(stu_project.instructor)
    for cell, align, ele in zip(table.rows[1].cells, align_cccccl, row2):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row3 = []  # 第3行的元素值用列表存储
    row3.append("选题名称")
    row3.append('')
    row3.append('')
    row3.append(stu_project.topic)
    row3.append("设计类型")
    row3.append(stu_defence.design_type)
    table.rows[2].cells[1].merge(table.rows[2].cells[3])
    for cell, align, ele in zip(table.rows[2].cells, (align_clcl*2)[:6], row3):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)
    # 从第四行开始，全部都只有一个单元格
    for i in range(3,9):
        table.rows[i].cells[0].merge(table.rows[i].cells[5])
    table.rows[3].cells[0].paragraphs[0].add_run('一、毕业设计目标')
    design_object = temp.para1+stu_project.key_word1+temp.para2+stu_project.key_word2+temp.para3+stu_project.key_word3+temp.para4+stu_project.key_word4+temp.para5+stu_project.key_word5+temp.para6
    table.rows[3].cells[0].add_paragraph().add_run('\t'+design_object.strip('*'))

    table.rows[4].cells[0].paragraphs[0].add_run('二、毕业设计任务及要求')
    table.rows[4].cells[0].add_paragraph().add_run('\t'+temp.task_require.replace('\r\n','\n\t'))

    table.rows[5].cells[0].paragraphs[0].add_run('三、毕业设计实施步骤和方法')
    table.rows[5].cells[0].add_paragraph().add_run('\t'+temp.step_way.replace('\r\n','\n\t'))

    table.rows[6].cells[0].paragraphs[0].add_run('四、毕业设计进程安排')
    table.rows[6].cells[0].add_paragraph().add_run('\t'+temp.schdeule.replace('\n\n','\n\t'))

    table.rows[7].cells[0].paragraphs[0].add_run('五、设计思路')
    table.rows[7].cells[0].add_paragraph().add_run('\t'+temp.thought.replace('\r\n','\n\t'))

    table.rows[8].cells[0].paragraphs[0].add_run('六、成果表现形式')
    table.rows[8].cells[0].add_paragraph().add_run('\t'+temp.result.replace('\r\n','\n\t'))

    # 保证table格式里面的行高至少为1cm
    for i in range(9):
        table.rows[i].height = Cm(1)
        for cell in table.rows[i].cells:
            for p in cell.paragraphs:
                p.paragraph_format.line_spacing = Pt(20)
                p.paragraph_format.space_after = Pt(0)

    table2 = word.add_table(rows=2, cols=14, style='Table Grid')
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.rows[0].cells[1].merge(table2.rows[0].cells[13])
    table2.rows[0].cells[0].paragraphs[0].add_run('指导教师意见')
    table2.rows[0].cells[1].add_paragraph().add_run(temp.comment)
    p10 = table2.rows[0].cells[1].add_paragraph('签字：')
    p10.add_run().add_picture(f'media/{inst.sign}', width=Cm(1.8))
    p10.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table2.rows[0].cells[1].add_paragraph(temp.rws_date).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    table2.rows[1].cells[1].merge(table2.rows[1].cells[6])
    table2.rows[1].cells[8].merge(table2.rows[1].cells[13])
    table2.rows[1].cells[0].paragraphs[0].add_run('教研室主任审批意见')
    table2.rows[1].cells[1].add_paragraph('      同意实施')
    table2.rows[1].cells[1].add_paragraph()
    p11_1 = table2.rows[1].cells[1].add_paragraph('签字：')
    p11_1.add_run().add_picture(f'media/{inst.sign}', width=Cm(1.8))
    p11_1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table2.rows[1].cells[1].add_paragraph(temp.rws_date).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table2.rows[1].cells[7].paragraphs[0].add_run('学院审批意见')
    table2.rows[1].cells[7].paragraphs[0].width = Cm(2.1)
    table2.rows[1].cells[8].add_paragraph('      同意实施')
    table2.rows[1].cells[8].add_paragraph()
    p11_2 = table2.rows[1].cells[8].add_paragraph('签字：')
    p11_2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p11_2.add_run().add_picture(f'media/{inst.sign}', width=Cm(1.5))
    # p11_2.add_run().add_picture(f'media/{temp.cachet}', width=Cm(4))
    table2.rows[1].cells[8].add_paragraph(temp.rws_date).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for i in range(2):
        table2.rows[i].height = Cm(1)

    bz1 = word.add_paragraph('注：1. 设计类型包括产品设计、流程设计或方案设计。')
    bz2 = word.add_paragraph('       2. 本表一式两份，一份二级学院留存，一份发给学生。')
    bz3 = word.add_paragraph('       3. 所有签字处必须手写，其他内容可打印，未签字者，不予开题。')
    for p in [bz1, bz2, bz3]:
        p.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.space_after = Pt(0)
        for run in p.runs:
            run.font.size = Pt(10.5)

    word.save(f'media/download_files/{word_name}')
    return word_name

# 生成毕业设计指导记录表
def generate_zdjlb(stu_no):
    stu = UserInfo.objects.get(username=stu_no)
    stu_project = GraduateProjectInfo.objects.get(stu=stu)
    stu_defence = DefenceInfo.objects.get(stu=stu)
    word_name =stu_no + "+" + stu_project.class_name + "+" + stu.last_name + stu.first_name + "+毕业设计指导记录表.docx"
    word = Document()
    # 先对于文档英文为Arial，中文为宋体所有字体设置为小四，所有字体设置为小四，
    word.styles['Normal'].font.name = 'Arial'
    word.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    word.styles['Normal'].font.size = Pt(12)
    title = word.add_paragraph('湖南商务职业技术学院毕业设计指导记录表')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.bold = True
    table = word.add_table(rows=3, cols=6, style='Table Grid')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 表头前三行对齐格式统一
    align_cccccl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    row1 = []    #第1行的元素值用列表存储
    row1.append('学生姓名')
    row1.append(stu.last_name + stu.first_name)
    row1.append('二级学院')
    row1.append(stu.dept_name)
    row1.append('班级名称')
    row1.append(stu_project.class_name)
    for cell, align, ele in zip(table.rows[0].cells, align_cccccl, row1):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row2 = []  # 第2行的元素值用列表存储
    row2.append('专业名称')
    row2.append(stu.major)
    row2.append('学      号')
    row2.append(stu_no)
    row2.append('指导教师')
    row2.append(stu_project.instructor)
    for cell, align, ele in zip(table.rows[1].cells, align_cccccl, row2):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row3 = []  # 第3行的元素值用列表存储
    row3.append("选题名称")
    row3.append('')
    row3.append('')
    row3.append(stu_project.topic)
    row3.append("设计类型")
    row3.append(stu_defence.design_type)
    table.rows[2].cells[1].merge(table.rows[2].cells[3])
    for cell, align, ele in zip(table.rows[2].cells, (align_clcl*2)[:6], row3):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)
    for i in range(3):
        table.rows[i].height = Cm(1)

    table2 = word.add_table(rows=8, cols=5, style='Table Grid')
    # 统一将第2个表格的第4列和第5列合并
    for i in range(8):
        table2.rows[i].cells[3].merge(table2.rows[i].cells[4])
        table2.rows[i].height = Cm(1)
    row4 = []  # 第4行的元素值用列表存储    默认第5个元素和第4个一样，不做处理
    row4.append("指导内容")
    row4.append('指导时间')
    row4.append('指导地点')
    row4.append("指导过程记录")
    for cell, align, ele in zip(table2.rows[0].cells[:4], align_cccccl[:4], row4):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
        for run in cell.paragraphs[0].runs:
            run.font.size = Pt(14)
            run.font.bold = True

# 从这一行开始后面的6行可以用for循环结合数据库进行遍历
    # 在进入程序开始需要引入老师的信息以调用指导记录表的模板信息
    # 还需要注意日期的年份要在程序里面重新获取，以免模板在教师修改后，年份写死了
    row5 = []  # 第5行的元素值用列表存储    默认第5个元素和第4个一样，不做处理
    row5.append("毕业设计选题")
    row5.append(f'{time.localtime().tm_year-1}年11月23日')
    row5.append('网络通信工具')
    row5.append("指导学生选题，讲解选题需要完成的工作内容，并下发毕业设计指南及模板")
    for cell, align, ele in zip(table2.rows[1].cells[:4], align_clcl, row5):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row6 = []  # 第6行的元素值用列表存储    默认第5个元素和第4个一样，不做处理
    row6.append("毕业设计工作计划")
    row6.append(f'{time.localtime().tm_year-1}年11月30日')
    row6.append('网络通信工具')
    row6.append("下发毕业设计任务书，并指导学生制定毕业设计工作计划")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[2].cells[:4], align_clcl, row6):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    # 合并作为毕业设计过程的单元格
    table2.rows[3].cells[0].merge(table2.rows[6].cells[0])
    row7 = []  # 第7行的元素值用列表存储    默认第5个元素和第4个一样，不做处理
    row7.append("毕业设计过程")
    row7.append(f'{time.localtime().tm_year}年2月28日')
    row7.append('网络通信工具')
    row7.append("上交初稿，指导老师审核初稿并提出修改意见，学生按照意见修改初稿。")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[3].cells[:4], align_clcl, row7):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row8 = []  # 第8行的元素值用列表存储    第1列置空，默认第5个元素和第4个一样，不做处理
    row8.append(f'{time.localtime().tm_year}年3月30日')
    row8.append('网络通信工具')
    row8.append("在初稿的基础上根据指导老师意见进行完善，上交第一次修改稿，老师审核后提出改进意见，并按照修改意见进行完善。")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[4].cells[1:4], align_clcl[1:], row8):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row9 = []  # 第9行的元素值用列表存储    第1列置空，默认第5个元素和第4个一样，不做处理
    row9.append(f'{time.localtime().tm_year}年5月1日')
    row9.append('网络通信工具')
    row9.append("在第一次修改稿的基础上进行完善，上交第二次修改稿，老师审核提出完善意见，并按照意见进行修改")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[5].cells[1:4], align_clcl[1:], row9):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row10 = []  # 第10行的元素值用列表存储    第1列置空，默认第5个元素和第4个一样，不做处理
    row10.append(f'{time.localtime().tm_year}年5月10日')
    row10.append('网络通信工具')
    row10.append("对毕业设计文档内容及格式进行完善，并进行查重，上交最终稿。")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[6].cells[1:4], align_clcl[1:], row10):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row11 = []  # 第11行的元素值用列表存储    第1列置空，默认第5个元素和第4个一样，不做处理
    row11.append('毕业设计答辩')
    row11.append(f'{time.localtime().tm_year}年5月15日')
    row11.append('线上')
    row11.append("答辩")
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    for cell, align, ele in zip(table2.rows[7].cells, align_clcl, row11):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)

    bz1 = word.add_paragraph('注：1. 设计类型包括产品设计、流程设计或方案设计。')
    bz2 = word.add_paragraph('       2. 毕业设计过程部分，指导教师可根据实际情况自行增加或删除行。')
    for p in [bz1, bz2]:
        p.paragraph_format.line_spacing = Pt(12)
        for run in p.runs:
            run.font.size = Pt(10.5)

    word.save(f'media/download_files/{word_name}')
    return word_name


# 生成毕业设计评阅表
def generate_pyb(stu_no, inst_no):
    stu = UserInfo.objects.get(username=stu_no)
    inst = UserInfo.objects.get(username=inst_no)
    stu_project = GraduateProjectInfo.objects.get(stu=stu)
    stu_defence = DefenceInfo.objects.get(stu=stu)
    word_name = stu_no + "+" + stu_project.class_name + "+" + stu.last_name + stu.first_name + "+毕业设计评阅表.docx"
    word = Document()
    # 先对于文档英文为Arial，中文为宋体所有字体设置为小四，所有字体设置为小四，
    word.styles['Normal'].font.name = 'Arial'
    word.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    word.styles['Normal'].font.size = Pt(12)
    word.sections[0].left_margin = Cm(2.1)
    word.sections[0].right_margin = Cm(2.1)
    title = word.add_paragraph('湖南商务职业技术学院毕业设计评阅表')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.bold = True
    table = word.add_table(rows=7, cols=6, style='Table Grid')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 表头前三行对齐格式统一
    align_cccccl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    row1 = []    #第1行的元素值用列表存储
    row1.append('学生姓名')
    row1.append(stu.last_name + stu.first_name)
    row1.append('二级学院')
    row1.append(stu.dept_name)
    row1.append('班级名称')
    row1.append(stu_project.class_name)
    for cell, align, ele in zip(table.rows[0].cells, align_cccccl, row1):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row2 = []  # 第2行的元素值用列表存储
    row2.append('专业名称')
    row2.append(stu.major)
    row2.append('学      号')
    row2.append(stu_no)
    row2.append('指导教师')
    row2.append(stu_project.instructor)
    for cell, align, ele in zip(table.rows[1].cells, align_cccccl, row2):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row3 = []  # 第3行的元素值用列表存储
    row3.append("选题名称")
    row3.append('')
    row3.append('')
    row3.append(stu_project.topic)
    row3.append("设计类型")
    row3.append(stu_defence.design_type)
    table.rows[2].cells[1].merge(table.rows[2].cells[3])
    for cell, align, ele in zip(table.rows[2].cells, (align_clcl*2)[:6], row3):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)
    for i in range(3):
        table.rows[i].height = Cm(1)

    table.rows[3].cells[0].merge(table.rows[3].cells[5])
    table.rows[3].cells[0].paragraphs[0].add_run('评价标准').bold =True
    table.rows[3].cells[0].paragraphs[0].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    row4_1 = table.rows[3].cells[0].add_paragraph()
    row4_1.add_run('1. 选题：').bold = True
    row4_1.add_run('重点评价毕业设计选题的专业性、实践性和工作量。')
    row4_2 = table.rows[3].cells[0].add_paragraph('')
    row4_2.add_run('2. 设计实施：').bold = True
    row4_2.add_run('评价毕业设计项目实施中技术路线的可行性、设计过程的完整性和设计依据的可靠性；按期圆满完成规定的任务，工作量饱满，难度较大；工作努力，遵守纪律；工作作风严谨务实。')
    row4_3 = table.rows[3].cells[0].add_paragraph('')
    row4_3.add_run('3. 分析与解决问题的能力：').bold = True
    row4_3.add_run('能运用所学知识和技能去发现与解决实际问题；能对设计进行理论分析，得出有价值的结论。')
    row4_4 = table.rows[3].cells[0].add_paragraph('')
    row4_4.add_run('4. 成果质量：').bold = True
    row4_4.add_run('以学生毕业设计形成的最终技术文件为主要考察对象，重点评价设计技术文件的规范性、技术方案的科学性和技术设计的创新性。')
    row4_5 = table.rows[3].cells[0].add_paragraph('')
    row4_5.add_run('5. 答辩情况：').bold = True
    row4_5.add_run('阐述课题的设计思路、主要依据、结论、体会和改进意见；回答问题的准确性、敏锐性、全面性、语言表达能力、逻辑条理性。')
    # 对于前5段统一将字体设置为10.5磅
    for i in range(1,6):
        for run in table.rows[3].cells[0].paragraphs[i].runs:
            run.font.size = Pt(10.5)
    row4_6 = table.rows[3].cells[0].add_paragraph('')
    tmp4 = row4_6.add_run('说明：')
    tmp4.bold = True
    tmp4.font.size = Pt(10.5)
    row4_6.add_run('1）指导老师根据标准1—4给出成果成绩').font.size = Pt(10.5)
    row4_6.add_run('（选题10分，设计实施30分，分析与解决问题的能力10分，成果质量50分）')
    row4_6.add_run('，答辩组根据标准1—5给出答辩成绩').font.size = Pt(10.5)
    row4_6.add_run('（选题10分，设计实施20分，分析与解决问题的能力10分，成果质量30分，答辩情况30分）')
    row4_6.add_run('，成果成绩和答辩成绩均采用百分制。').font.size = Pt(10.5)
    row4_7 = table.rows[3].cells[0].add_paragraph('')
    row4_7.add_run('         2）毕业设计最终成绩：成果成绩占40%，答辩成绩占60%，采用五级制').font.size = Pt(10.5)
    row4_7.add_run('（优秀：90以上，良：80-89，中：70-79，及格：60-69，不及格：60分以下）')
    row4_7.add_run('进行评定。').font.size = Pt(10.5)
    for p in table.rows[3].cells[0].paragraphs:
        p.paragraph_format.first_line_indent = Pt(21)
        p.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        # p.paragraph_format.line_spacing = Pt(12)
        p.paragraph_format.space_after = Pt(0)

    table.rows[4].cells[0].merge(table.rows[4].cells[5])
    table.rows[4].cells[0].paragraphs[0].add_run('指导老师评价意见，并对是否同意参加答辩作出明确说明\n').bold = True
    row5_2 = table.rows[4].cells[0].add_paragraph('')
    row5_2.add_run('文档撰写规范，方案设计完善，格式符合要求，同意答辩。\n')
    row5_3 = table.rows[4].cells[0].add_paragraph('')
    tmp5 = row5_3.add_run(' 指导老师签名：')
    tmp5.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    # row5_3.paragraph_format.first_line_indent = Pt(150)
    row5_3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    tmp_day = pd.to_datetime(stu_defence.defence_date, format='%Y年%m月%d日')-pd.tseries.offsets.DateOffset(days=1)
    row5_4 = table.rows[4].cells[0].add_paragraph(tmp_day.strftime('%Y年%m月%d日'))
    row5_4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table.rows[4].cells[0].add_paragraph()

    table.rows[5].cells[0].merge(table.rows[5].cells[5])
    table.rows[5].cells[0].paragraphs[0].add_run('答辩组评价意见\n').bold = True
    row6_2 = table.rows[5].cells[0].add_paragraph('')
    row6_2.add_run('问题回答准确，条理清晰，答辩通过。\n')
    row6_3 = table.rows[5].cells[0].add_paragraph('')
    tmp6 = row6_3.add_run('答辩组老师（三人以上）签名：')
# 签名要对答辩的老师进行遍历
    tmp6.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    tmp6.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    tmp6.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    tmp6.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    row6_3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    row6_4 = table.rows[5].cells[0].add_paragraph(stu_defence.defence_date)
    row6_4.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table.rows[5].cells[0].add_paragraph()

    align_cccccc = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER,
                    WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]

    row7 = []  # 第7行的元素值用列表存储
    row7.append('成果成绩')
    row7.append(stu_defence.ach_grade)
    row7.append('答辩成绩')
    row7.append(stu_defence.defence_grade)
    row7.append('最终成绩')
    row7.append(stu_defence.final_grade)
    for cell, align, ele in zip(table.rows[6].cells, align_cccccc, row7):
        cell.paragraphs[0].add_run(ele)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
    table.rows[6].height = Cm(1)

    bz = word.add_paragraph('注：设计类型指产品设计、流程设计或方案设计。')
    bz.paragraph_format.line_spacing = Pt(15)
    bz.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    for run in bz.runs:
        run.font.size = Pt(10.5)

    word.save(f'media/download_files/{word_name}')
    return word_name


# 生成毕业设计答辩记录表
def generate_dbjlb(stu_no, inst_no):
    stu = UserInfo.objects.get(username=stu_no)
    inst = UserInfo.objects.get(username=inst_no)
    stu_project = GraduateProjectInfo.objects.get(stu=stu)
    stu_defence = DefenceInfo.objects.get(stu=stu)
    word_name = stu_no + "+" + stu_project.class_name + "+" + stu.last_name + stu.first_name + "+毕业设计答辩记录表.docx"
    word = Document()
    # 先对于文档英文为Arial，中文为宋体所有字体设置为小四，所有字体设置为小四，
    word.styles['Normal'].font.name = 'Arial'
    word.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    word.styles['Normal'].font.size = Pt(12)
    word.sections[0].left_margin = Cm(2.1)
    word.sections[0].right_margin = Cm(2.1)
    title = word.add_paragraph('湖南商务职业技术学院毕业设计答辩记录表')
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in title.runs:
        run.font.size = Pt(18)
        run.font.bold = True
    table = word.add_table(rows=7, cols=6, style='Table Grid')
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 表头前三行对齐格式统一
    align_cccccl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    align_clcl = [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    row1 = []    #第1行的元素值用列表存储
    row1.append('学生姓名')
    row1.append(stu.last_name + stu.first_name)
    row1.append('二级学院')
    row1.append(stu.dept_name)
    row1.append('班级名称')
    row1.append(stu_project.class_name)
    for cell, align, ele in zip(table.rows[0].cells, align_cccccl, row1):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row2 = []  # 第2行的元素值用列表存储
    row2.append('专业名称')
    row2.append(stu.major)
    row2.append('学      号')
    row2.append(stu_no)
    row2.append('指导教师')
    row2.append(stu_project.instructor)
    for cell, align, ele in zip(table.rows[1].cells, align_cccccl, row2):
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.paragraphs[0].add_run(ele)
    row3 = []  # 第3行的元素值用列表存储
    row3.append("选题名称")
    row3.append('')
    row3.append('')
    row3.append(stu_project.topic)
    row3.append("设计类型")
    row3.append(stu_defence.design_type)
    table.rows[2].cells[1].merge(table.rows[2].cells[3])
    for cell, align, ele in zip(table.rows[2].cells, (align_clcl*2)[:6], row3):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)

    row4 = []  # 第4行的元素值用列表存储
    row4.append("答辩时间")
    row4.append('')
    row4.append('')
    row4.append(stu_defence.defence_date)
    row4.append("答辩地点")
    row4.append(stu_defence.defence_location)
    table.rows[3].cells[1].merge(table.rows[3].cells[3])
    for cell, align, ele in zip(table.rows[3].cells, (align_clcl * 2)[:6], row4):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)

    row5 = []  # 第5行的元素值用列表存储
    row5.append("答辩组成员")
    row5.append('')
    row5.append('')
    row5.append('')
    row5.append('')
    inst_tmp = [stu_defence.def_inst1, stu_defence.def_inst2, stu_defence.def_inst3, stu_defence.def_inst4, stu_defence.def_inst5]
    inst_list = []
    inst_group = ''
    for i in inst_tmp:
        if i != 'nan':
            inst_list.append(i)
            inst_group = inst_group + i + "、"
    row5.append(inst_group.strip('、'))
    table.rows[4].cells[1].merge(table.rows[4].cells[5])
    for cell, align, ele in zip(table.rows[4].cells, (align_clcl * 2)[:6], row5):
        cell.paragraphs[0].paragraph_format.alignment = align
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        cell.paragraphs[0].add_run(ele)
    for i in range(5):
        table.rows[i].height = Cm(1)

    table.rows[5].cells[0].merge(table.rows[5].cells[5])
    table.rows[5].cells[0].paragraphs[0].add_run('一、学生网络答辩影像（附：答辩截屏图片或录屏文件）')
    tmp6 = table.rows[5].cells[0].add_paragraph().add_run()
    tmp6.add_picture(f'media/{stu_project.defence_image}', height=Cm(7))
    table.rows[5].cells[0].add_paragraph()
    table.rows[5].cells[0].add_paragraph('二、学生自述内容')
    table.rows[5].cells[0].add_paragraph(stu_project.self_report)
    table.rows[5].cells[0].add_paragraph()
    table.rows[5].cells[0].add_paragraph('三、提问与问答')
    table.rows[5].cells[0].add_paragraph(stu_project.quiz.replace('\r',''))

    table.rows[6].cells[0].merge(table.rows[6].cells[2])
    table.rows[6].cells[3].merge(table.rows[6].cells[5])
    table.rows[6].cells[0].paragraphs[0].add_run('记录人（签字）：')
    tmp7 = table.rows[6].cells[0].add_paragraph().add_run()
    tmp7.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    table.rows[6].cells[0].paragraphs[1].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.rows[6].cells[0].add_paragraph(stu_defence.defence_date).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    table.rows[6].cells[3].paragraphs[0].add_run('答辩小组成员（签字）：')
    tmp72 = table.rows[6].cells[3].add_paragraph().add_run()
    for item in inst_list:
# 获取对应老师的UserInfo对象，然后获取相应的签名保存地址
        tmp72.add_picture(f'media/{inst.sign}', width=Cm(1.8))
    table.rows[6].cells[3].paragraphs[1].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.rows[6].cells[3].add_paragraph(stu_defence.defence_date).paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    word.save(f'media/download_files/{word_name}')
    return word_name