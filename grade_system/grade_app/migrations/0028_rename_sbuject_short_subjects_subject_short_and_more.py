# Generated by Django 5.1.4 on 2025-01-03 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade_app', '0027_alter_subjects_sbuject_short_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subjects',
            old_name='sbuject_short',
            new_name='subject_short',
        ),
        migrations.AlterField(
            model_name='classes',
            name='class_name',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
