# Generated by Django 3.2.7 on 2021-09-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_blogmodel_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='content',
            field=models.TextField(),
        ),
    ]
