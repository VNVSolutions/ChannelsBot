# Generated by Django 3.1.1 on 2024-07-04 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('main_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_channels', to='bot.mainchannel')),
            ],
        ),
        migrations.CreateModel(
            name='KeywordReplacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('replacement', models.CharField(max_length=255)),
                ('sub_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keyword_replacements', to='bot.subchannel')),
            ],
        ),
    ]
