from django.urls import include, path, reverse
from . import views,views_latex

urlpatterns = [
    path('', views.index, name='index'),
    path('exams/',views.examlist,name='examlist'),
    path('exams/<int:exam_id>/',views.examdetail,name="examdetail"),
    path('exams/<int:exam_id>/add_question/<int:question_id>',views.add_to_exam,name="add_to_exam"),
    path('exams/<int:exam_id>/delete_question/<int:examitem_id>',views.delete_from_exam,name="delete_from_exam"),
    path('exams/<int:exam_id>/up/<int:examitem_id>',views.up,name="up"),
    path('exams/<int:exam_id>/down/<int:examitem_id>',views.down,name="down"),
    path('new/',views.new,name='new'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/delete',views.delete,name='delete'),
    path('<int:question_id>/regen_jpg',views.regen_jpg_view,name='regen_jpg'),
    path('add/',views.add, name='add'),
    path('exams/add/',views.addexam, name='addexam'),
    path('exams/<int:exam_id>/preview/', views_latex.preview, name="preview"),

# redirect only
    path('exams/<int:exam_id>/questions/<int:question_id>', views.redirect2q,name="redirect2q"),
    path('exams/<int:exam_id>/new_question/',views.redirect2q,name="redirect2q")

]