from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("aa_core_hub", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolarSystemCelestial",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("solar_system_id", models.IntegerField(db_index=True)),
                ("solar_system_name", models.CharField(max_length=128, db_index=True)),
                ("celestial_id", models.BigIntegerField(db_index=True)),
                ("name", models.CharField(max_length=128)),
                ("celestial_type", models.CharField(
                    max_length=16,
                    choices=[("STAR","Star"),("PLANET","Planet"),("MOON","Moon")],
                    db_index=True,
                )),
                ("parent_planet_id", models.BigIntegerField(null=True, blank=True, db_index=True)),
                ("parent_planet_name", models.CharField(max_length=128, blank=True, default="")),
            ],
            options={
                "unique_together": {("celestial_id",)},
            },
        ),
        migrations.AddIndex(
            model_name="solarsystemcelestial",
            index=models.Index(fields=["solar_system_id","celestial_type"], name="aa_core_cel_sys_type_idx"),
        ),
    ]
