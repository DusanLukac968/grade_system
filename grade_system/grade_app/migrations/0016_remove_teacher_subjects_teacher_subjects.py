# Generated by Django 5.1.4 on 2024-12-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade_app', '0015_remove_student_id_student_student_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='subjects',
        ),
        migrations.AddField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(to='grade_app.subjects', verbose_name='Subjecs'),
        ),
    ]
