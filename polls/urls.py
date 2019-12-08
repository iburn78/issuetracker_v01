from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'), 
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('new/', views.QuestionCreateView.as_view(), name='question-create'), 
    path('new_choice/<int:pk>/', views.ChoiceCreateView.as_view(), name='choice-create'), 
    path('delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question-delete'), 
]

