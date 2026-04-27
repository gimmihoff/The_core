import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_core_hub", "0005_geography_cache"),
    ]

    operations = [
        migrations.AddField(
            model_name="structure",
            name="structure_category",
            field=models.CharField(
                choices=[
                    ("STRUCTURE", "Structure"),
                    ("SOV", "Sovereignty"),
                    ("FLEX", "Flex"),
                    ("CUSTOMS_OFFICE", "Customs Office"),
                    ("SKYHOOK", "Skyhook"),
                    ("MOON_DRILL", "Moon Drill"),
                    ("MERCENARY_DEN", "Mercenary Den"),
                    ("UNKNOWN", "Unknown"),
                ],
                db_index=True,
                default="UNKNOWN",
                max_length=32,
            ),
        ),
        migrations.AddIndex(
            model_name="structure",
            index=models.Index(fields=["structure_category", "standing"], name="aa_core_hub_structu_e1a149_idx"),
        ),
        migrations.CreateModel(
            name="SovereigntySystem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("solar_system_id", models.IntegerField(db_index=True, unique=True)),
                ("alliance_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("corporation_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("faction_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("raw_payload", models.JSONField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
            options={"ordering": ("solar_system_id",)},
        ),
        migrations.CreateModel(
            name="SovereigntyStructure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("structure_id", models.BigIntegerField(db_index=True, unique=True)),
                ("structure_type_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("solar_system_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("alliance_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("vulnerability_occupancy_level", models.FloatField(blank=True, db_index=True, null=True)),
                ("vulnerable_start_time", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("vulnerable_end_time", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("raw_payload", models.JSONField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
            options={"ordering": ("solar_system_id", "structure_id")},
        ),
        migrations.CreateModel(
            name="SovereigntyCampaign",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("campaign_id", models.BigIntegerField(db_index=True, unique=True)),
                ("solar_system_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("constellation_id", models.IntegerField(blank=True, db_index=True, null=True)),
                ("structure_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("event_type", models.CharField(blank=True, db_index=True, default="", max_length=64)),
                ("defender_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("defender_score", models.FloatField(blank=True, null=True)),
                ("attackers_score", models.FloatField(blank=True, null=True)),
                ("start_time", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("raw_payload", models.JSONField(blank=True, null=True)),
                ("updated_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
            ],
            options={"ordering": ("start_time", "solar_system_id")},
        ),
        migrations.AddIndex(
            model_name="sovereigntysystem",
            index=models.Index(fields=["alliance_id", "solar_system_id"], name="aa_core_hub_allianc_27848c_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntysystem",
            index=models.Index(fields=["corporation_id", "solar_system_id"], name="aa_core_hub_corpora_37f992_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntysystem",
            index=models.Index(fields=["faction_id", "solar_system_id"], name="aa_core_hub_faction_248998_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntystructure",
            index=models.Index(fields=["solar_system_id", "structure_type_id"], name="aa_core_hub_solar_s_1b6ffe_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntystructure",
            index=models.Index(fields=["alliance_id", "solar_system_id"], name="aa_core_hub_allianc_e7caa8_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntystructure",
            index=models.Index(fields=["vulnerable_start_time", "vulnerable_end_time"], name="aa_core_hub_vulnera_d5a753_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntycampaign",
            index=models.Index(fields=["solar_system_id", "start_time"], name="aa_core_hub_solar_s_9aefea_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntycampaign",
            index=models.Index(fields=["constellation_id", "start_time"], name="aa_core_hub_constel_a30d9c_idx"),
        ),
        migrations.AddIndex(
            model_name="sovereigntycampaign",
            index=models.Index(fields=["defender_id", "start_time"], name="aa_core_hub_defende_08ddb8_idx"),
        ),
    ]
