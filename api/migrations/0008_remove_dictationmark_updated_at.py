# Generated by Django 3.0.3 on 2020-03-05 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_dictationmark_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictationmark',
            name='updated_at',
        ),
    ]