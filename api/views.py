import json
import os
import uuid

from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex.Translater import Translater

from api.models import *
from api.serializers import *


def createUniquId():
    # 8-numeric
    return hash(str(uuid.uuid1())) % 100000000


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def study_set_detail(request, pk):
    study_set = StudySets.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = StudySetsSerializer(study_set)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = StudySetsSerializer(study_set, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        study_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PATCH', 'DELETE', 'POST'])
def dictation(request, code, mode):
    global dictation
    if mode == "id":
        dictation = Dictation.objects.get(id=code)
    elif mode == "code":
        dictation = Dictation.objects.get(code=code)
    if request.method == 'GET':
        serializer = SpecificDictationSerializer(dictation)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = SpecificDictationSerializer(dictation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dictation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE', 'POST'])
def user(request, email="default"):
    if request.method == 'GET':
        user = User.objects.get(email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT' or request.method == 'PATCH':
        user = User.objects.get(email=email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user = User.objects.get(email=email)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_members_marks(request, dictation_id, mode):
    global dictation
    if mode == "id":
        dictation = Dictation.objects.get(id=dictation_id)
    elif mode == "code":
        dictation = Dictation.objects.get(code=dictation_id)
    if request.method == 'GET':
        members_marks = []
        dictation_marks = DictationMark.objects.filter(dictation=dictation)
        for dictation_mark in dictation_marks:
            members_marks.append({"email": dictation_mark.user.email, "mark": dictation_mark.mark})

        return JsonResponse(members_marks, safe=False)


@api_view(['PATCH'])
def update_user_mark(request, email):
    import json

    data = json.loads(request.data)
    dictationId = data["dictation_id"]
    mark = data["mark"]
    user = User.objects.get(email=email)
    dictation = Dictation.objects.get(id=dictationId)

    try:
        currentMark = DictationMark.objects.get(user=user, dictation=dictation)
        currentMark.mark = mark
    except DictationMark.DoesNotExist:
        currentMark = DictationMark(user=user, dictation=dictation, mark=mark)

    currentMark.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_completed_dictations(request, email):
    if request.method == 'GET':
        dictation_marks = DictationMark.objects.filter(user=User.objects.get(email=email)).order_by('-updated_at')[:20]
        member_marks = []
        for dictation_mark in dictation_marks:
            member_marks.append({"code": dictation_mark.dictation.code,
                                 "name": dictation_mark.dictation.name})

        return JsonResponse(member_marks, safe=False)


@api_view(['GET'])
def get_shared_studyset(request, creator, pk):
    study_set = StudySets.objects.get(creator=creator, pk=pk)
    if request.method == 'GET':
        serializer = StudySetsSerializer(study_set)
        return Response(serializer.data)


class GetDictationsOfCurrentUser(generics.ListAPIView):
    serializer_class = DictationNamesSerializer

    def get_queryset(self, user_email=None):
        user_email = self.kwargs['user_email']
        return Dictation.objects.filter(creator=user_email).order_by('-updated_at')


@api_view(['POST'])
def create_study_set(request):
    global serializer
    if request.method == 'POST':
        serializer = StudySetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_dictation(request):
    global serializer
    if request.method == 'POST':
        serializer = SpecificDictationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(code=createUniquId())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetStudySetsOfCurrentUser(generics.ListAPIView):
    serializer_class = StudySetsSerializer

    def get_queryset(self, user_email=None):
        user_email = self.kwargs['user_email']
        return StudySets.objects.filter(creator=user_email)


@api_view(['POST', 'GET'])
def translate(request, from_lang, to_lang, mode='one'):
    translater = Translater()

    translater.set_key('trnsl.1.1.20200120T150252Z.3a85fe4899fc30b8.cb6bb06d018c3bb040233c26b981ba5b5e447520')
    translater.set_from_lang(from_lang)
    translater.set_to_lang(to_lang)

    string_to_translate = request.data.get('nameValuePairs').get('words')

    if mode == 'one':

        translater.set_text(string_to_translate)

        response = {
            "translation": translater.translate()
        }

    elif mode == 'many':

        translater.set_text(string_to_translate)

        response = {'translation': translater.translate().replace(',', ';')}

    return JsonResponse(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def finish_study_set(request, pk, mode):
    study_set = StudySets.objects.get(pk=pk)

    if mode == 'marked':
        study_set_words = json.loads(study_set.marked_words)
    else:
        study_set_words = json.loads(study_set.words)

    for study_set_word in study_set_words:
        study_set_word["firstStage"] = True
        study_set_word["secondStage"] = False
        study_set_word["thirdStage"] = False
        study_set_word["forthStage"] = False

    if mode == 'marked':
        study_set.marked_words = study_set_words
    else:
        study_set.words = study_set_words

    study_set.studied = True

    study_set.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def clone_studyset(request, id, email):
    studyset = StudySets.objects.get(pk=id)

    cloned_studyset = StudySets.objects.filter(creator=email, words=studyset.words,
                                               language_from=studyset.language_from,
                                               language_to=studyset.language_to,
                                               amount_of_words=studyset.amount_of_words,
                                               name=studyset.name)

    if cloned_studyset.exists():
        return Response(cloned_studyset[0].pk, status=status.HTTP_200_OK)

    if not studyset.creator == email and not cloned_studyset.exists():
        studyset.pk = None
        studyset.creator = email
        studyset.save()

    return Response(studyset.pk, status=status.HTTP_200_OK)
