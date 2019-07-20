import django_tables2 as tables
from .models import Question

class QuestionTable(tables.Table):
    jpg_url = tables.Column('jpg_url',order_by='id')
    class Meta:
        model = Question
        template_name = 'django_tables2/bootstrap.html'
        sequence = 'id','jpg_url'