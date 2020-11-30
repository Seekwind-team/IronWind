# Generated by Django 3.1.3 on 2020-11-30 18:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareSpace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(help_text='Headline of this Care-Space Entry', max_length=255)),
                ('header_image', models.ImageField(blank=True, help_text='Header Image of this Care-Space item', null=True, upload_to='static/carespacecontent/headerimages/')),
                ('body', models.TextField(blank=True, help_text='Body-Text of this Care-Space item')),
                ('author', models.CharField(blank=True, help_text='Author of this Care-Space item', max_length=255)),
                ('favicon_publisher', models.ImageField(blank=True, help_text='Publisher Icon of this Care-Space item', null=True, upload_to='static/carespacecontent/icons/')),
                ('publisher', models.CharField(blank=True, help_text='Publisher of this Care-Space item', max_length=255, null=True)),
                ('paid', models.BooleanField(default=False, help_text='is this paid item?')),
                ('rich_text', models.BooleanField(default=False, help_text='Rich text item?')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, help_text='User creation DateTime')),
            ],
        ),
    ]
