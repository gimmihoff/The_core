from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aa_core_hub", "0004_dscan_timeline_api"),
    ]

    operations = [
        migrations.CreateModel(
            name="EveRegion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("region_id", models.IntegerField(db_index=True, unique=True)),
                ("name", models.CharField(db_index=True, max_length=128)),
                ("description", models.TextField(blank=True, default="")),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="EveConstellation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("constellation_id", models.IntegerField(db_index=True, unique=True)),
                ("region_id_external", models.IntegerField(blank=True, db_index=True, null=True)),
                ("name", models.CharField(db_index=True, max_length=128)),
                ("region", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="constellations", to="aa_core_hub.everegion")),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="EveSolarSystem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("solar_system_id", models.IntegerField(db_index=True, unique=True)),
                ("constellation_id_external", models.IntegerField(blank=True, db_index=True, null=True)),
                ("region_id_external", models.IntegerField(blank=True, db_index=True, null=True)),
                ("name", models.CharField(db_index=True, max_length=128)),
                ("security_status", models.FloatField(blank=True, db_index=True, null=True)),
                ("position_x", models.FloatField(blank=True, null=True)),
                ("position_y", models.FloatField(blank=True, null=True)),
                ("position_z", models.FloatField(blank=True, null=True)),
                ("constellation", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="systems", to="aa_core_hub.eveconstellation")),
                ("region", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="systems", to="aa_core_hub.everegion")),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="EveStargate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("stargate_id", models.BigIntegerField(db_index=True, unique=True)),
                ("name", models.CharField(blank=True, db_index=True, default="", max_length=128)),
                ("source_system_id_external", models.IntegerField(db_index=True)),
                ("destination_stargate_id", models.BigIntegerField(blank=True, db_index=True, null=True)),
                ("destination_system_id_external", models.IntegerField(blank=True, db_index=True, null=True)),
                ("position_x", models.FloatField(blank=True, null=True)),
                ("position_y", models.FloatField(blank=True, null=True)),
                ("position_z", models.FloatField(blank=True, null=True)),
                ("destination_system", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="incoming_stargates", to="aa_core_hub.evesolarsystem")),
                ("source_system", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="outgoing_stargates", to="aa_core_hub.evesolarsystem")),
            ],
            options={"ordering": ("source_system_id_external", "name", "stargate_id")},
        ),
        migrations.AddIndex(
            model_name="eveconstellation",
            index=models.Index(fields=["region_id_external", "name"], name="aa_core_hub_region__9cf022_idx"),
        ),
        migrations.AddIndex(
            model_name="evesolarsystem",
            index=models.Index(fields=["region_id_external", "name"], name="aa_core_hub_region__7375e0_idx"),
        ),
        migrations.AddIndex(
            model_name="evesolarsystem",
            index=models.Index(fields=["constellation_id_external", "name"], name="aa_core_hub_constel_403a96_idx"),
        ),
        migrations.AddIndex(
            model_name="evesolarsystem",
            index=models.Index(fields=["security_status", "name"], name="aa_core_hub_securit_572a50_idx"),
        ),
        migrations.AddIndex(
            model_name="evestargate",
            index=models.Index(fields=["source_system_id_external", "destination_system_id_external"], name="aa_core_hub_source__27ceef_idx"),
        ),
        migrations.AddIndex(
            model_name="evestargate",
            index=models.Index(fields=["destination_system_id_external", "source_system_id_external"], name="aa_core_hub_destina_ef1135_idx"),
        ),
    ]
