from rest_framework import serializers
from .models import *


class StudySetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name', 'words', 'creator', 'amount_of_words', 'id', 'language_to', 'language_from')


class StudySetsNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name', 'amount_of_words', 'id')


class DictationNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictation
        fields = ('code', 'name', 'amount_of_words', 'id')


class SpecificDictationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictation
        fields = ('creator', 'name', 'words', 'marked_words',
                  'amount_of_words', 'amount_of_words_for_dictation', 'type_of_questions', 'members', 'id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'marks')
