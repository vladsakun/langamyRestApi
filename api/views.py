import json

from django.http import JsonResponse
from rest_framework import status, mixins, generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex.Translater import Translater
from api.serializers import *
from .models import User as UserModel


def createUniquId():
    # 8-numeric
    return hash(str(uuid.uuid1())) % 100000000


class CreateStudySet(mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = StudySetsSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class StudySetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudySets.objects.all()
    serializer_class = StudySetsSerializer


class GetDictationsOfCurrentUser(generics.ListAPIView):
    serializer_class = DictationNamesSerializer

    def get_queryset(self, user_email=None):
        user_email = self.kwargs['user_email']
        return Dictation.objects.filter(creator=user_email).order_by('-updated_at')


class GetStudySetsOfCurrentUser(generics.ListAPIView):
    serializer_class = StudySetsSerializer

    def get_queryset(self, user_email=None):
        user_email = self.kwargs['user_email']
        return StudySets.objects.filter(creator=user_email).order_by('-updated_at')


class User(APIView):

    def get(self, request, email=None, format=None):
        lookup = {'email': email}
        vessel = get_object_or_404(UserModel, **lookup)
        serializer = UserSerializer(vessel, context={'request': request})
        return Response(serializer.data)


class CreateUser(mixins.CreateModelMixin,
                 generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DictationView(APIView):
    def get(self, request, code=None, mode=None, format=None):
        lookup = {'pk': code} if mode == 'id' else {'code': code}
        dictation = get_object_or_404(Dictation, **lookup)
        serializer = SpecificDictationSerializer(dictation, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SpecificDictationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(code=createUniquId())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        dictation = Dictation.objects.get(pk=pk)
        dictation.delete()
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
        dictation_marks = DictationMark.objects.filter(user=UserModel.objects.get(email=email)).order_by('-updated_at')[:20]
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


class RandomDictation(generics.GenericAPIView,
                      mixins.ListModelMixin):

    def get_queryset(self):
        creator_name = self.kwargs['creator']
        return Dictation.objects.exclude(creator=creator_name).order_by('?')[:1]

    serializer_class = SpecificDictationSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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

        words = json.loads(studyset.words)

        for word in words:
            word["firstStage"] = False
            word["secondStage"] = False
            word["thirdStage"] = False
            word["forthStage"] = False

        studyset.words = words

        studyset.creator = email
        studyset.save()

    return Response(studyset.pk, status=status.HTTP_200_OK)
