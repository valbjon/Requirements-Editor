# Generated by Django 2.0.13 on 2019-10-28 12:32

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blocktype',
            name='guide',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='guide',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='textblock',
            name='guide',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]