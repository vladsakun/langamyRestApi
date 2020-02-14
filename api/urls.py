from django.urls import path

from api import views

urlpatterns = [

    path('api/get/studyset/<int:pk>/', views.study_set_detail),
    path('api/create/studyset/', views.create_study_set),
    path('api/delete/studyset/<int:pk>/', views.study_set_detail),
    path('api/patch/studyset/<int:pk>/', views.study_set_detail),
    path('api/get/studysetsnames/<str:user_email>/', views.GetStudySetsOfCurrentUser.as_view()),
    path('api/get/shared/studyset/<str:creator>/<int:pk>/', views.get_shared_studyset),

    path('api/create/dictation/', views.create_dictation),
    path('api/get/dictation/<int:code>/<str:mode>/', views.dictation),
    path('api/patch/dictation/members/<int:id>/<str:email>/', views.update_members),
    path('api/delete/dictation/<int:code>/<str:mode>/', views.dictation),
    path('api/patch/dictation/<int:code>/<str:mode>/', views.dictation),
    path('api/get/dictationsnames/<str:user_email>/', views.GetDictationsOfCurrentUser.as_view()),

    path('api/get/user/<str:email>/', views.user),
    path('api/create/user/', views.user),
    path('api/patch/user/mark/<str:email>/', views.update_user_mark),
]
