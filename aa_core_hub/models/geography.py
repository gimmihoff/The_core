from django.db import models


class EveRegion(models.Model):
    region_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class EveConstellation(models.Model):
    constellation_id = models.IntegerField(unique=True, db_index=True)
    region = models.ForeignKey(
        EveRegion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="constellations",
    )
    region_id_external = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=128, db_index=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["region_id_external", "name"]),
        ]

    def __str__(self) -> str:
        return self.name


class EveSolarSystem(models.Model):
    solar_system_id = models.IntegerField(unique=True, db_index=True)
    constellation = models.ForeignKey(
        EveConstellation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="systems",
    )
    constellation_id_external = models.IntegerField(null=True, blank=True, db_index=True)
    region = models.ForeignKey(
        EveRegion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="systems",
    )
    region_id_external = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=128, db_index=True)
    security_status = models.FloatField(null=True, blank=True, db_index=True)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    position_z = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["region_id_external", "name"]),
            models.Index(fields=["constellation_id_external", "name"]),
            models.Index(fields=["security_status", "name"]),
        ]

    def __str__(self) -> str:
        return self.name


class EveStargate(models.Model):
    stargate_id = models.BigIntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=128, blank=True, default="", db_index=True)
    source_system = models.ForeignKey(
        EveSolarSystem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="outgoing_stargates",
    )
    source_system_id_external = models.IntegerField(db_index=True)
    destination_stargate_id = models.BigIntegerField(null=True, blank=True, db_index=True)
    destination_system = models.ForeignKey(
        EveSolarSystem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="incoming_stargates",
    )
    destination_system_id_external = models.IntegerField(null=True, blank=True, db_index=True)
    position_x = models.FloatField(null=True, blank=True)
    position_y = models.FloatField(null=True, blank=True)
    position_z = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ("source_system_id_external", "name", "stargate_id")
        indexes = [
            models.Index(fields=["source_system_id_external", "destination_system_id_external"]),
            models.Index(fields=["destination_system_id_external", "source_system_id_external"]),
        ]

    def __str__(self) -> str:
        return self.name or str(self.stargate_id)
