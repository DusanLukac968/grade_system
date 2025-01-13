# Generated by Django 5.1.4 on 2024-12-18 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade_app', '0004_classes_subjects_alter_parent_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='teacher',
        ),
        migrations.AlterField(
            model_name='teacher',
            name='classes',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='grade_app.subjects', verbose_name='Subjecs'),
        ),
    ]
