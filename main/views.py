import json
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from api.models import *


@login_required(login_url='/login/')
def index(request):
    try:
        user = User.objects.get(email=request.user.email)
    except User.DoesNotExist:
        user = User(email=request.user.email)
        user.save()
    if request.method == 'POST':
        dictation_code = request.POST.get("dictation_code")
        return redirect('get/dictation/' + dictation_code + '/')
    return render(request, 'main/wrapper.html', context={"user_email": request.user.email})


@login_required(login_url='/login/')
def get_dictation(request, code):
    try:
        dictation = Dictation.objects.get(code=code)
        dictation_words = json.loads(dictation.words)
        marked_words = json.loads(dictation.marked_words)
        for marked_word in marked_words:
            dictation_words.append(marked_word)
    except Dictation.DoesNotExist:
        return render(request, 'main/dictation.html', context={"error": "Dictation does not exist"})
    return render(request, 'main/dictation.html', context={"dictation": dictation, "dictation_words": dictation_words})


@login_required(login_url='/login/')
def dictation(request, code):
    try:
        dictation = Dictation.objects.get(code=code)
        dictation_words = json.loads(dictation.words)
        marked_words = json.loads(dictation.marked_words)
        for marked_word in marked_words:
            dictation_words.append(marked_word)
    except Dictation.DoesNotExist:
        return render(request, 'main/dictation.html', context={"error": "Dictation does not exist"})

    dictation_words_objects = []
    for word in dictation_words:
        dictation_words_objects.append(DictationWord(word.term, word.translation))

    dictation_words_for_template = []



    return render(request, 'main/dictation_test.html',
                  context={"dictation": dictation, "dictation_words": dictation_words})


def get_random_values(words, forloop_counter):
    words.remove(forloop_counter)
    incorrect_values = []
    for word in words:
        random.randrange(0, len(words))

class DictationWord(object):

    def __init__(self, term, translation, first_incorrect_value, third_incorrect_value, second_incorrect_value):
        """Constructor"""
        self.term = term
        self.translation = translation
        self.first_incorrect_value = first_incorrect_value
        self.second_incorrect_value = second_incorrect_value
        self.third_incorrect_value = third_incorrect_value

    def get_term(self):
        return self.term

    def get_translation(self):
        return self.translation
