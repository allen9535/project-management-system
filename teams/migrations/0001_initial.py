# Generated by Django 4.2.7 on 2023-11-19 06:40
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='팀명')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
            ],
        ),
    ]
