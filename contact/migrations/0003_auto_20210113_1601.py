# Generated by Django 3.1.5 on 2021-01-13 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_auto_20210113_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettercontact',
            name='ip_address',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
