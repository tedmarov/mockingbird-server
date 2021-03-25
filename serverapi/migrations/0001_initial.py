# Generated by Django 3.1.7 on 2021-03-25 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Birdie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=250)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_label', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_title', models.CharField(max_length=50)),
                ('edited_on', models.DateTimeField(auto_now=True)),
                ('text_body', models.CharField(max_length=250)),
                ('text_source', models.CharField(max_length=250)),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
            ],
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_name', models.CharField(max_length=45)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('voice_recording', models.CharField(max_length=3000)),
                ('voice_edited', models.DateField(auto_now_add=True)),
                ('privacy', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.category')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.text')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_title', models.CharField(max_length=50)),
                ('edited_on', models.DateTimeField(auto_now=True)),
                ('comment_detail', models.CharField(max_length=250)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.voice')),
            ],
        ),
        migrations.CreateModel(
            name='BirdieText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birdie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
                ('text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.text')),
            ],
        ),
    ]
