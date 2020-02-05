from rest_framework import serializers
from .models import *


class StudySetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name', 'words', 'creator', 'amount_of_words', 'id')


class StudySetsNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySets
        fields = ('name','amount_of_words', 'id')
