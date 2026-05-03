from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_core_hub", "0007_dscan_public_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="structure",
            name="fit_notes",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="structure",
            name="status",
            field=models.CharField(
                choices=[
                    ("ONLINE", "Online"),
                    ("ANCHORING", "Anchoring"),
                    ("LOW_POWER", "Low Power"),
                    ("ABANDONED", "Abandoned"),
                    ("ATTACKED", "Attacked"),
                    ("REINFORCED", "Reinforced"),
                    ("CONTESTED", "Contested"),
                    ("REMOVED", "Removed / Not Present"),
                    ("DESTROYED", "Destroyed"),
                    ("UNKNOWN", "Unknown"),
                ],
                db_index=True,
                default="UNKNOWN",
                max_length=16,
            ),
        ),
    ]
