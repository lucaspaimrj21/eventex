# Generated by Django 4.2.1 on 2023-12-08 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_course_abc_to_mti'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CourseOld',
        ),
    ]
