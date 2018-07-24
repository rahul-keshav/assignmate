# Generated by Django 2.0.1 on 2018-05-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0004_assignment_answered_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=20)),
                ('discription', models.CharField(max_length=500)),
                ('document', models.FileField(upload_to='documents//%Y/%m/%d/')),
                ('uploaded_at', models.DateField(auto_now=True)),
            ],
        ),
    ]