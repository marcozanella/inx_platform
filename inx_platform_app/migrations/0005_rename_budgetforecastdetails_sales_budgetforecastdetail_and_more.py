# Generated by Django 4.2.4 on 2024-04-29 08:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inx_platform_app", "0004_alter_budfordetailline_detail_date_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BudgetForecastDetails_sales",
            new_name="BudgetForecastDetail",
        ),
        migrations.RenameModel(
            old_name="BudgetForecastDetails",
            new_name="BudgetForecastDetail_sales",
        ),
    ]
