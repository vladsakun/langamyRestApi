# Generated by Django 3.0.3 on 2020-02-29 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_studysets_marked_words'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studysets',
            name='marked_words',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]