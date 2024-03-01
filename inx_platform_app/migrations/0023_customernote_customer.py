# Generated by Django 4.2.4 on 2024-02-29 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0022_remove_customernote_author_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customernote",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="inx_platform_app.customer",
            ),
        ),
    ]
