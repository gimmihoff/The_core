import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_core_hub", "0003_rename_aa_core_hu_type_n_idx_aa_core_hub_type_na_72d917_idx_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dscan",
            name="scanned_at",
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterModelOptions(
            name="dscan",
            options={"ordering": ("-scanned_at", "-created_at")},
        ),
        migrations.AddIndex(
            model_name="dscan",
            index=models.Index(fields=["solar_system_id", "scanned_at"], name="aa_core_hub_dscan__0fbe59_idx"),
        ),
        migrations.AddIndex(
            model_name="dscan",
            index=models.Index(fields=["solar_system_name", "scanned_at"], name="aa_core_hub_dscan__16123d_idx"),
        ),
        migrations.AddIndex(
            model_name="dscan",
            index=models.Index(fields=["source", "scanned_at"], name="aa_core_hub_dscan__592d4b_idx"),
        ),
    ]
