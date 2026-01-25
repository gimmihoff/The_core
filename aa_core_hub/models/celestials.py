from django.db import models

class SolarSystemCelestial(models.Model):
    solar_system_id = models.IntegerField(db_index=True)
    solar_system_name = models.CharField(max_length=128, db_index=True)

    celestial_id = models.BigIntegerField(db_index=True)
    name = models.CharField(max_length=128)
    celestial_type = models.CharField(
        max_length=16,
        choices=(
            ("STAR","Star"),
            ("PLANET","Planet"),
            ("MOON","Moon"),
        ),
        db_index=True,
    )
    parent_planet_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    parent_planet_name = models.CharField(max_length=128, blank=True, default="")

    class Meta:
        indexes = [
            models.Index(fields=["solar_system_id","celestial_type"]),
        ]
        unique_together = ("celestial_id",)
