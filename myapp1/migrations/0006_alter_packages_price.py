# Generated by Django 4.1.7 on 2023-04-03 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0005_alter_packages_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packages',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]