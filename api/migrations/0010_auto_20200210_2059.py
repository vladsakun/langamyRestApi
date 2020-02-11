# Generated by Django 3.0.2 on 2020-02-10 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_dictation'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictation',
            name='amount_of_words',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='dictation',
            name='amount_of_words_for_dictation',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='dictation',
            name='marked_words',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dictation',
            name='type_of_questions',
            field=models.CharField(default='quiz', max_length=256),
        ),
        migrations.AlterField(
            model_name='dictation',
            name='members',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
