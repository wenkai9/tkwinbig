# Generated by Django 5.0.4 on 2024-05-31 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0005_rename_shop_indo_raidsysrule_shop_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
