# Generated by Django 4.2.6 on 2023-10-15 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redditapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Suggestion Text')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
