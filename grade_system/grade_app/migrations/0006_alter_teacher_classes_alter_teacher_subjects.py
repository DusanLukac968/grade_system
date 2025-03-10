# Generated by Django 5.1.4 on 2024-12-18 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade_app', '0005_remove_subjects_teacher_alter_teacher_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='classes',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='subjects',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade_app.subjects', verbose_name='Subjecs'),
        ),
    ]
