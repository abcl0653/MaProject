# Generated by Django 2.1.4 on 2018-12-20 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='uuid',
            new_name='workspace',
        ),
    ]