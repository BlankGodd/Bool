# Generated by Django 3.2.7 on 2021-10-22 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0004_auto_20211021_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='public_id',
            field=models.CharField(default='7417ea85-8066-49c4-9551-7a14c5604046', max_length=300),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='public_id',
            field=models.CharField(default='35527ceb-d64b-4718-91de-8229cff1c212', max_length=300),
        ),
    ]
