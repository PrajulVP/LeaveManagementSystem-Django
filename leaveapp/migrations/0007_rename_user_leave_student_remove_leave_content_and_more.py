# Generated by Django 5.0.1 on 2024-02-08 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaveapp', '0006_student_address_student_department_teacher_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='user',
            new_name='student',
        ),
        migrations.RemoveField(
            model_name='leave',
            name='content',
        ),
        migrations.AddField(
            model_name='leave',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='leave',
            name='reason',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
    ]