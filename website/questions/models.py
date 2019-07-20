from django.db import models
import time
import html

# Create your models here.



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    workspace = models.CharField(max_length=64)
    pub_date = models.DateTimeField('date published',auto_now=True)
    # exam_count = models.Aggregate(Exam)
    category = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    rate = models.IntegerField()
    # preview_photo = models.ImageField(upload_to=workspace)

    @property
    def jpg_url(self):
        return self.workspace + "/" + self.workspace+".jpg" # + str("?=") + str(time.time())
    @property
    def current_time(self):
        return str(time.time())
    @property
    def pdf_url(self):
        return self.workspace + "/" + self.workspace+".pdf"

    @property
    def abs_path(self):
        question_dir = '/Users/lincai/MaProject/website/questions/static/questions/workspaces/'
        return  question_dir + str(self.workspace) + '/' + str(self.workspace) + '.tex'



class Exam(models.Model):
    exam_name = models.CharField(max_length=20)
    exam_title = models.CharField(max_length=40)
    exam_subtitle = models.CharField(max_length=40)
    #questions = models.ManyToOneField(ExamItem)
    create_date = models.DateTimeField('date created',auto_now=True)

    @property
    def jpg_url(self):
        return self.exam_name + "/" + ".jpg"

    @property
    def pdf_url(self):
        return self.exam_name + "/" + ".pdf"

    @property
    def question_count(self):
        return self.examitem_set.all().count()
        # return self.questions.all().count()

    @property
    def abs_path(self):
        exam_dir = '/Users/lincai/MaProject/website/questions/static/questions/exams/'
        return  exam_dir + str(self.id) + '_' + self.exam_name + '.tex'

    def get_questions(self):
        return self.examitem_set.all()



class ExamItem(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    seq = models.IntegerField()
    # question = models.OneToOneField(Question,on_delete=models.SET_NULL,null=True)
    question = models.ForeignKey(Question,on_delete=models.SET_NULL,null=True)
    create_date = models.DateTimeField(auto_now=True)


