# Generated by Django 5.1.3 on 2024-11-14 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_documentmodel_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentmodel',
            options={'verbose_name': 'Документ', 'verbose_name_plural': 'Документы'},
        ),
    ]
