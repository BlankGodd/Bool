# Generated by Django 3.2.7 on 2021-10-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_alter_student_public_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='public_id',
            field=models.CharField(default='fadd718f-86a7-4fa5-a7a6-c7a0f6c7a06b', max_length=300),
        ),
    ]
