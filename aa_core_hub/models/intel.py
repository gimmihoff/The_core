from django.db import models
from django.utils import timezone

class SystemIntel(models.Model):
    solar_system_id = models.IntegerField(db_index=True)
    solar_system_name = models.CharField(max_length=128, blank=True, default="", db_index=True)
    status = models.CharField(max_length=64, blank=True, default="", db_index=True)
    details = models.TextField(blank=True, default="")
    tags = models.JSONField(null=True, blank=True)
    updated_by_user_id = models.IntegerField(null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        unique_together = ("solar_system_id",)
        ordering = ("solar_system_name",)
