# Generated by Django 4.2.4 on 2023-10-15 18:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_members", "0002_alter_user_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="sqlapp_id",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
