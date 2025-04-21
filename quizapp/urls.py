from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz, name='index'),
    path('<int:question_id>/', views.quiz, name='quiz'),  # クイズのページ
    path('categories/', views.category_list, name='category_list'),  # カテゴリ一覧ページ
    path('categories/<str:category>/', views.category_questions, name='category_questions'),  # 特定カテゴリの問題ページ
    path('random/', views.random_quiz, name='random_quiz'),  # ランダム問題ページ
]