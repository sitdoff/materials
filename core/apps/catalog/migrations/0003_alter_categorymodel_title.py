# Generated by Django 5.1.3 on 2024-11-13 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_categorymodel_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Наименование категории'),
        ),
    ]
