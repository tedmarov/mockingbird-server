# Generated by Django 3.1.7 on 2021-03-16 16:46

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
            name='VoiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voice_name', models.CharField(max_length=45)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('voice_text', models.CharField(max_length=3000)),
                ('last_edit', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.voicecategory')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_title', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField()),
                ('comment_detail', models.CharField(max_length=250)),
                ('last_edit', models.DateTimeField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.voice')),
            ],
        ),
        migrations.CreateModel(
            name='BirdieVoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birdie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.birdie')),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serverapi.voice')),
            ],
        ),
    ]