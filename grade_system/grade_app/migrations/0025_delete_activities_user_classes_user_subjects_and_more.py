# Generated by Django 5.1.4 on 2024-12-31 09:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grade_app', '0024_remove_parent_last_login_remove_parent_password_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Activities',
        ),
        migrations.AddField(
            model_name='user',
            name='classes',
            field=models.ManyToManyField(default='', to='grade_app.classes', verbose_name='Classes'),
        ),
        migrations.AddField(
            model_name='user',
            name='subjects',
            field=models.ManyToManyField(default='', to='grade_app.subjects', verbose_name='Subjecs'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]
