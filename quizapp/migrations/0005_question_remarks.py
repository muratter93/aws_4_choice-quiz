# Generated by Django 5.1.2 on 2025-03-12 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_answerhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
