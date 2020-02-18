import json
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
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

        dictation_words_for_template = []
        dictation_words_len = len(dictation_words) - 1

        for i in range(0, dictation_words_len):
            dictation_words_copy = dictation_words.copy()
            three_random_values = get_random_dictation_words(dictation_words_copy, i)
            answers = [dictation_words[i]["translation"],
                       three_random_values[0],
                       three_random_values[1],
                       three_random_values[2]]
            random.shuffle(answers)
            dictation_words_for_template.append(
                {"term": dictation_words[i]["term"],
                 "translation": dictation_words[i]["translation"],
                 "mixed": answers})

        random.shuffle(dictation_words_for_template)
    except Dictation.DoesNotExist:
        return render(request, 'main/dictation.html', context={"error": "Dictation does not exist"})

    return render(request, 'main/dictation_test.html',
                  context={'dictation': dictation, 'dictation_words': dictation_words_for_template, })


def check_answers(request):
    # answers = json.loads(request.data)
    dictation = Dictation.objects.get(id=request.POST.get("dictation_id"))
    answers = request.POST.get('answers')
    dictation_words = json.loads(dictation.words)
    marked_words = json.loads(dictation.marked_words)

    for marked_word in marked_words:
        dictation_words.append(marked_word)

    # for answer in answers:
    #     answers[]
    return JsonResponse(request)


def get_random_dictation_words(all_words, forloop_counter):
    del all_words[forloop_counter]
    three_incorrect_values = []
    for i in range(0, 3):
        random_index = random.randrange(0, len(all_words))

        three_incorrect_values.append(all_words[random_index]["translation"])
        del all_words[random_index]
    return three_incorrect_values


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
