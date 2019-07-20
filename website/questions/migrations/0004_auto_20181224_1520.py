# Generated by Django 2.2 on 2018-12-24 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20181223_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seq', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('question', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='questions.Question')),
            ],
        ),
        migrations.AlterField(
            model_name='exam',
            name='questions',
            field=models.ManyToManyField(to='questions.ExamItem'),
        ),
    ]