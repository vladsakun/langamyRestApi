# Generated by Django 3.0.2 on 2020-03-18 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_merge_20200318_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
