# Generated by Django 3.0.3 on 2020-03-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200305_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictationmark',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
