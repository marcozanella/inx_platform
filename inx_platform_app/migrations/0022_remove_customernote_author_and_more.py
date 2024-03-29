# Generated by Django 4.2.4 on 2024-02-29 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0021_rename_job_postion_contact_job_position_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customernote",
            name="author",
        ),
        migrations.RemoveField(
            model_name="customernote",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="customernote",
            name="date",
        ),
        migrations.AddField(
            model_name="customernote",
            name="archived",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="customernote",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="customernote",
            name="note_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_by_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="customernote",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name="customernote",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="updated_by_notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
