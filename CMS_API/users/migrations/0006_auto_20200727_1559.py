# Generated by Django 3.0.8 on 2020-07-27 10:29

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200727_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='document',
            field=models.FileField(upload_to='upload_content_doc/', validators=[users.models.ValidateFileExtension]),
        ),
    ]
