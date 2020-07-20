# Generated by Django 3.0.8 on 2020-07-20 13:18

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200720_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=15, validators=[users.validators.UppercaseValidator, users.validators.LowercaseValidator]),
        ),
    ]
