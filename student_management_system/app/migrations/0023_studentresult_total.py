# Generated by Django 4.1.6 on 2023-02-22 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_parents_admin_remove_parents_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentresult',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
