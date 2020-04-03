from django.urls import path

from api import views

urlpatterns = [

    path('translate/<str:from_lang>/<str:to_lang>/<str:mode>/', views.translate),

    path('finish/studyset/<int:pk>/<str:mode>/', views.finish_study_set),
    path('clone/studyset/<int:id>/<str:email>/', views.clone_studyset),
    path('get/studysetsnames/<str:user_email>/', views.GetStudySetsOfCurrentUser.as_view()),
    path('get/shared/studyset/<str:creator>/<int:pk>/', views.get_shared_studyset),

    path('create/dictation/', views.DictationView.as_view()),
    path('get/dictation/<int:code>/<str:mode>/', views.DictationView.as_view()),
    path('delete/dictation/<int:pk>/', views.DictationView.as_view()),
    path('get/dictationsnames/<str:user_email>/', views.GetDictationsOfCurrentUser.as_view()),
    path('get/dictation/marks/<int:dictation_id>/<str:mode>/', views.get_members_marks),
    path('get/user/completed/dictations/<str:email>/', views.get_user_completed_dictations),
    path('get/random/dictation/<str:creator>/', views.RandomDictation.as_view()),

    path('get/user/<str:email>/', views.User.as_view()),
    path('create/user/', views.CreateUser.as_view()),
    path('patch/user/mark/<str:email>/', views.update_user_mark),

    path('studyset/<int:pk>/', views.StudySetDetail.as_view()),
    path('create/studyset/', views.CreateStudySet.as_view()),
]
