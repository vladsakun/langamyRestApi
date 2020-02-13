from django.urls import path

from api import views

urlpatterns = [
    path('api/get/studyset/<int:pk>/', views.api_study_set_detail),
    path('api/get/dictation/<int:code>/<str:mode>/', views.get_dictation),
    path('api/get/studysetsnames/<str:user_email>/', views.GetStudySetsOfCurrentUser.as_view()),
    path('api/get/dictationsnames/<str:user_email>/', views.GetDictationsOfCurrentUser.as_view()),
    path('api/create/studyset/', views.create_study_set),
    path('api/create/dictation/', views.create_dictation),
]
