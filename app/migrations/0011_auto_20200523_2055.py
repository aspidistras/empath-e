# Generated by Django 2.2.12 on 2020-05-23 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200523_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='awareness_user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='raise_awareness_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
