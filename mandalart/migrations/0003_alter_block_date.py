# Generated by Django 3.2 on 2021-08-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandalart', '0002_rename_created_date_block_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='date',
            field=models.DateField(),
        ),
    ]
