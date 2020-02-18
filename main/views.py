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

        all_dictation_words = json.loads(dictation.words)
        other_words = all_dictation_words.copy()
        marked_words = json.loads(dictation.marked_words)

        amount_of_questions = dictation.amount_of_words_for_dictation
        amount_of_other_words = amount_of_questions - len(marked_words)

        for marked_word in marked_words:
            all_dictation_words.append(marked_word)

        dictation_words_for_template = []

        for n in range(0, len(marked_words)):
            three_random_values = get_random_dictation_words(all_dictation_words.copy(), marked_words[n])
            answers = [marked_words[n]["translation"],
                       three_random_values[0],
                       three_random_values[1],
                       three_random_values[2]]

            random.shuffle(answers)

            dictation_words_for_template.append(
                {"term": marked_words[n]["term"],
                 "mixed": answers})

        random.shuffle(other_words)

        for i in range(0, amount_of_other_words):
            three_random_values = get_random_dictation_words(all_dictation_words.copy(), other_words[i])
            answers = [other_words[i]["translation"],
                       three_random_values[0],
                       three_random_values[1],
                       three_random_values[2]]

            random.shuffle(answers)

            dictation_words_for_template.append(
                {"term": other_words[i]["term"],
                 "mixed": answers})

        random.shuffle(dictation_words_for_template)
    except Dictation.DoesNotExist:
        return render(request, 'main/dictation.html', context={"error": "Dictation does not exist"})

    return render(request, 'main/dictation_test.html',
                  context={'dictation': dictation, 'dictation_words': dictation_words_for_template, })


def check_answers(request):
    mark = 0

    dictation = Dictation.objects.get(id=request.POST.get("dictation_id"))

    answers = json.loads(request.POST.get('answers'))
    dictation_words = json.loads(dictation.words)
    marked_words = json.loads(dictation.marked_words)

    for marked_word in marked_words:
        dictation_words.append(marked_word)

    prepared_dictation_words = {}

    for dictation_word in dictation_words:
        prepared_dictation_words[dictation_word["term"]] = dictation_word["translation"]

    sorted_words_keys = sorted(prepared_dictation_words.keys(), key=lambda x: x.lower())
    sorted_answers_keys = sorted(answers.keys(), key=lambda x: x.lower())

    sorted_answers = {}
    sorted_words = {}

    for key in sorted_words_keys:
        sorted_words.update({key: prepared_dictation_words[key]})

    for key in sorted_answers_keys:
        sorted_answers.update({key: answers[key]})

    for answer_key in sorted_answers.keys():
        if answers[answer_key] == sorted_words[answer_key]:
            mark = mark + 1
        else:
            continue

    user = User.objects.get(email=request.user.email)
    try:

        dictation_mark = DictationMark.objects.get(user=user, dictation=dictation)
        dictation_mark.mark = mark

    except DictationMark.DoesNotExist:

        dictation_mark = DictationMark(user=user, dictation=dictation, mark=mark)

    dictation_mark.save()
    response_data = {
        "data": {
            "mark": mark
        }
    }
    return JsonResponse(response_data, safe=False)


def get_random_dictation_words(all_words, forloop_object):
    all_words.pop(all_words.index(forloop_object))
    for word in all_words:
        print(word["term"])
    print("-" * 20)
    three_incorrect_values = []
    for i in range(0, 3):
        random_index = random.randrange(len(all_words))

        three_incorrect_values.append(all_words[random_index]["translation"])
        del all_words[random_index]
    return three_incorrect_values
