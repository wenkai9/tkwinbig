# Generated by Django 5.0.4 on 2024-05-31 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_alter_tk_im_message_alter_tk_im_reftaskid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='taskId',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
