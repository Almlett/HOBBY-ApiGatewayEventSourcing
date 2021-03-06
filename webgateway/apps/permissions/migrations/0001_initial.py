# Generated by Django 3.1.2 on 2020-12-07 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apigateway', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('type', models.IntegerField(choices=[(0, 'Undefined'), (1, 'Get'), (2, 'List'), (3, 'Post'), (4, 'Put'), (5, 'Patch'), (6, 'Delete'), (7, 'Component')], default=0)),
                ('api', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apigateway.api')),
            ],
            options={
                'unique_together': {('name', 'key')},
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permissions.permission')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permissions.profile')),
            ],
        ),
    ]
