# Generated by Django 4.1 on 2022-08-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_rename_phone_customuser_phone_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(blank=True, max_length=40, unique=True),
        ),
    ]
