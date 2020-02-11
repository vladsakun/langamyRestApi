from rest_framework import serializers
from .models import *


class StudySetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name', 'words', 'creator', 'amount_of_words', 'id')


class StudySetsNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name', 'amount_of_words', 'id')


class SpecificDictationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dictation
        fields = ('creator', 'name', 'words', 'marked_words',
                  'amount_of_words', 'amount_of_words_for_dictation', 'type_of_questions', 'code')
