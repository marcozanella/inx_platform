# Generated by Django 4.2.4 on 2024-12-17 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inx_platform_app', '0076_majorlabel_oem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDSRTFFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='sds_rtf_files/')),
                ('file_content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inx_platform_app.language')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inx_platform_app.product')),
            ],
            options={
                'db_table': 'sds_rtf_file',
            },
        ),
        migrations.AddConstraint(
            model_name='sdsrtffile',
            constraint=models.UniqueConstraint(fields=('product', 'language'), name='unique_product_language'),
        ),
    ]