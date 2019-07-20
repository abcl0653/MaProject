from django.shortcuts import render,redirect
from django.contrib import messages
from django_tables2 import RequestConfig
from django.urls import reverse
from django.db import IntegrityError

from .models import Question,Exam,ExamItem
from .tables import QuestionTable
from django.contrib.auth import authenticate, login

# Create your views here.
from django.http import HttpResponse

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from subprocess import call
from django.contrib.staticfiles.templatetags.staticfiles import static
from pdf2image import convert_from_path

exam_dir = '/Users/lincai/MaProject/website/questions/static/questions/exams/'
workspaces_dir = '/Users/lincai/MaProject/website/questions/static/questions/workspaces/'
question_artifact = workspaces_dir+'question_artifact.tex'

anchor_start  = '%%% -------- Anchor Start -------- %%%\n'
anchor_end    = '%%% -------- Anchor End ---------- %%%\n'

import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def generate_question(question):
    question_dir = workspaces_dir+str(question.workspace)+'/'
    createFolder(question_dir)
    question_tex = workspaces_dir+str(question.workspace)+'/'+str(question.workspace)+'.tex'
    question_pdf = workspaces_dir+str(question.workspace)+'/'+str(question.workspace)+'.pdf'
    question_jpg = workspaces_dir+str(question.workspace)+'/'+str(question.workspace)+'.jpg'
    f_artifact_tex = open(question_artifact,'r')
    f_question_tex = open(question_tex,'w')
    f_question_tex.writelines(f_artifact_tex.readlines())
    f_artifact_tex.close()
    f_question_tex.close()

    call(["xelatex", "-output-directory",question_dir,question_tex])

    images = convert_from_path(question_pdf)
    images[0].save(question_jpg)

def regen_jpg(question):
    question_pdf = workspaces_dir + str(question.workspace) + '/' + str(question.workspace) + '.pdf'
    question_jpg = workspaces_dir + str(question.workspace) + '/' + str(question.workspace) + '.jpg'
    images = convert_from_path(question_pdf)
    images[0].save(question_jpg)

def del_question_dir(question):
    question_dir = workspaces_dir + str(question.workspace)
    call(["rm","-r",question_dir])

def preview(request,exam_id):
    exam = Exam.objects.get(pk=exam_id)
    exam_pdf_url = generate_exam(exam)
    return redirect(static(exam_pdf_url))


def generate_exam(exam):
    # exam.get_questions()

    exam_tex = exam_dir + str(exam.id) + '_' + exam.exam_name + '.tex'
    exam_pdf = exam_dir + str(exam.id) + '_' + exam.exam_name + '.pdf'
    exam_pdf_url = 'questions/exams/'+str(exam.id) + '_' + exam.exam_name + '.pdf'


    # call(["touch",exam_tex])
    exam_tex_file = open(exam_tex, 'w')  # Write
    header = open(exam_dir+'exam_header.tex','r')
    exam_tex_file.writelines(header.readlines())
    header.close()

    items = exam.examitem_set.order_by('seq')

    for item in items:
        fill = False
        question_tex_trim = []
        question_tex = open(workspaces_dir+(item.question.workspace)+'/'+str(item.question.workspace)+'.tex','r')
        # print(question_tex.readlines())

        for question_tex_line in question_tex.readlines():
            print(question_tex_line)
            if fill == True:
                question_tex_trim.append(question_tex_line)

            if question_tex_line == anchor_start:
                fill = True
            if question_tex_line == anchor_end:
                fill = False
        if question_tex_trim:
            exam_tex_file.write('\question')
            exam_tex_file.write('%% Question ID: '+str(item.question.workspace))
            exam_tex_file.writelines(question_tex_trim)
        question_tex.close()


    footer = open(exam_dir + 'exam_footer.tex', 'r')
    exam_tex_file.writelines(footer.readlines())
    footer.close()
    exam_tex_file.close()
    #call(["xelatex", "-output-directory",question_dir,question_tex])
    call(["xelatex","-output-directory",exam_dir,exam_tex])
    return exam_pdf_url

