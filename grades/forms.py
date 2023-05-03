from django import forms
from .models import GradesFiles

class FileFieldForm(forms.ModelForm):
    multiple_grades_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept':"application/vnd.ms-excel"}), help_text='支持多选，直接选择本人本学期 所有的 班级成绩单', label='学生成绩单（可多选，但仅限上传本人任课的成绩单）')
    class Meta:
        model = GradesFiles
        fields = ['multiple_grades_files', 'dept_name', 'major', 'template_id']