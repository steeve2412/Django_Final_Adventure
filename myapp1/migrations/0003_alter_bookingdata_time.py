# Generated by Django 4.1.7 on 2023-04-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0002_contactusdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdata',
            name='time',
            field=models.CharField(choices=[('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'), ('01 PM', '01 PM'), ('02 PM', '02 PM'), ('03 PM', '03 AM'), ('04 PM', '04 PM'), ('05 PM', '05 PM'), ('06 PM', '06 PM'), ('07 PM', '07 PM'), ('08 PM', '08 PM'), ('09 PM', '09 PM')], default='9 AM', max_length=10),
        ),
    ]
