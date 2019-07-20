from django.shortcuts import render,redirect
from django.contrib import messages
from django_tables2 import RequestConfig
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist



from .models import Question,Exam,ExamItem
from .tables import QuestionTable
import uuid
from django.contrib.auth import authenticate, login

# Create your views here.
from django.http import HttpResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from .views_latex import generate_question,del_question_dir,regen_jpg

def index(request):
    # return HttpResponse("Hello, world. You're at the questions index.")
    latest_question_list = Question.objects.order_by('-pub_date') # [:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'questions/index.html', context)

def new(request):
    question_table = QuestionTable(Question.objects.all())
    RequestConfig(request).configure(question_table)
    return render(request,'questions/new.html',{'question_table':question_table})

def detail(request,question_id):

    question = Question.objects.get(pk=question_id)
    if not request.POST:
        return render(request,'questions/questiondetail.html',{'question':question})
    else:
        question.question_text=request.POST['question_text']
        question.category=request.POST['category']
        question.grade   = request.POST['grade']
        question.rate   = request.POST['rate']
        question.save()
        messages.info(request, "Question: " + str(question_id) + ' is updated')
        return render(request,'questions/questiondetail.html',{'question':question})
    # else:
    #     return render(request,'questions/questiondetail.html')

def add(request):
    if not request.POST:
        # This is a get request, render a empty form for input
        return render(request,'questions/add.html')
    else: # POST request
        # Get the question id and redirect to the question
        question = Question.objects.create(workspace=uuid.uuid1(),
                                           question_text=request.POST['question_text'],
                                           category=request.POST['category'],
                                           grade=request.POST['grade'],
                                           rate=request.POST['rate'])

        # Do the real important thing here
        generate_question(question)
        question.save()
        return redirect(reverse('questions:detail' ,kwargs={'question_id':question.id}))

def delete(request,question_id):
    question = Question.objects.get(pk=question_id)
    question.delete()
    del_question_dir(question)
    # question.save()
    return redirect(reverse('questions:index'))

def addexam(request):
    if not request.POST:
        # This is a get request, render a empty form for input
        return render(request,'questions/examadd.html')
    else: # POST request
        # Get the question id and redirect to the question
        exam = Exam.objects.create(
            exam_name = request.POST['exam_name'],
            exam_title = request.POST['exam_title'],
            exam_subtitle = request.POST['exam_subtitle']
        )

        # Do the real important thing here
        # generate_question(question)
        exam.save()
        return redirect(reverse('questions:examdetail' ,kwargs={'exam_id':exam.id}))

@api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def examlist(request):
    latest_exam_list = Exam.objects.order_by('-create_date')[:10]
    context = {'latest_exam_list': latest_exam_list}
    return render(request,'questions/examlist.html',context)

def examdetail(request,exam_id):
    exam = Exam.objects.get(pk=exam_id)
    exam_items = exam.examitem_set.order_by('seq')
    questions = Question.objects.all()
    context = {'exam':exam,'exam_items':exam_items,'questions':questions}

    return render(request,'questions/examdetail.html',context)

def add_to_exam(request,exam_id,question_id):
    # messages.info(request, "exam: "+ str(exam_id) + "questiond id:" + str(question_id))
    # print(str(exam_id)+str(question_id))
    exam = Exam.objects.get(pk=exam_id)
    question = Question.objects.get(pk=question_id)

    try:

        item = ExamItem.objects.get(question = question_id,exam = exam_id)
        messages.error(request, 'The Question is already in the exam')
    except ObjectDoesNotExist as e:
        examItem = ExamItem.objects.create(exam=exam, question=question, seq=gen_item_no(exam))
        examItem.save()

    # try:
    #     examItem = ExamItem.objects.create(exam = exam,question = question,seq=gen_item_no(exam))
    #     examItem.save()
    # except IntegrityError as e:
    #     if 'UNIQUE constraint failed' in e.args[0]:
    #         messages.error(request, 'The Question is already in the exam')

    return redirect(reverse('questions:examdetail' ,kwargs={'exam_id':exam_id}))

def delete_from_exam(request,exam_id,examitem_id):
    ExamItem.objects.get(pk=examitem_id).delete()
    return redirect(reverse('questions:examdetail', kwargs={'exam_id': exam_id}))

def up(request,exam_id,examitem_id):
    orig = ExamItem.objects.get(pk=examitem_id)
    seq = orig.seq
    orig.seq = seq - 1
    try:
        replace = ExamItem.objects.get(exam = exam_id,seq=seq-1)
        replace.seq = seq
        orig.save()
        replace.save()
    except ObjectDoesNotExist as e:
        messages.info(request,'Already at the top of the exam')

    return redirect(reverse('questions:examdetail', kwargs={'exam_id': exam_id}))

def down(request,exam_id,examitem_id):
    orig = ExamItem.objects.get(pk=examitem_id)
    seq = orig.seq
    orig.seq = seq + 1
    try:
        replace = ExamItem.objects.get(exam = exam_id,seq=seq+1)
        replace.seq = seq
        orig.save()
        replace.save()
    except ObjectDoesNotExist as e:
        messages.info(request,'Already at the bottom of the exam')

    return redirect(reverse('questions:examdetail', kwargs={'exam_id': exam_id}))

def regen_jpg_view(request,question_id):
    question = Question.objects.get(pk=question_id)
    regen_jpg(question)
    return redirect(reverse('questions:detail', kwargs={'question_id': question_id}))

def gen_item_no(exam):
    if exam.examitem_set.count() > 0:
        return exam.examitem_set.order_by('-seq')[0].seq + 1
    else:
        return 1

def redirect2q(request,exam_id,question_id):
    if question_id:
        return redirect(reverse('questions:detail', kwargs={'question_id': question_id}))
    else:
        return redirect(reverse('questions:add'))


