from django.urls import path

from api import views

urlpatterns = [

    path('translate/<str:from_lang>/<str:to_lang>/<str:mode>/', views.translate),

    path('get/studyset/<int:pk>/', views.study_set_detail),
    path('create/studyset/', views.create_study_set),
    path('finish/studyset/<int:pk>/', views.finish_study_set),
    path('delete/studyset/<int:pk>/', views.study_set_detail),
    path('patch/studyset/<int:pk>/', views.study_set_detail),
    path('get/studysetsnames/<str:user_email>/', views.GetStudySetsOfCurrentUser.as_view()),
    path('get/shared/studyset/<str:creator>/<int:pk>/', views.get_shared_studyset),

    path('create/dictation/', views.create_dictation),
    path('get/dictation/<int:code>/<str:mode>/', views.dictation),
    path('get/dictation/marks/<int:dictation_id>/<str:mode>/', views.get_members_marks),
    path('delete/dictation/<int:code>/<str:mode>/', views.dictation),
    path('patch/dictation/<int:code>/<str:mode>/', views.dictation),
    path('get/dictationsnames/<str:user_email>/', views.GetDictationsOfCurrentUser.as_view()),

    path('get/user/<str:email>/', views.user),
    path('create/user/', views.user),
    path('patch/user/mark/<str:email>/', views.update_user_mark),
]
