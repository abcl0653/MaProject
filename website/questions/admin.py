from django.contrib import admin
from .models import Question,Exam,ExamItem
# Register your models here.
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(ExamItem)
