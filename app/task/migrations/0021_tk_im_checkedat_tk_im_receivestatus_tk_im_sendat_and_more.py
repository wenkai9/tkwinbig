# Generated by Django 4.2.14 on 2024-08-07 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0020_tk_invacation_receivestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='tk_im',
            name='checkedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tk_im',
            name='receivestatus',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tk_im',
            name='sendAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tk_im',
            name='userId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
