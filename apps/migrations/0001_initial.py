# Generated by Django 5.0.4 on 2024-05-06 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('res_mail', models.CharField(blank=True, max_length=100)),
                ('res_pwd', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
