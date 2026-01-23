from django.db import models
from django.utils import timezone

class DScan(models.Model):
    """Stores raw + parsed D-Scan data for downstream intel tooling."""
    source = models.CharField(max_length=32, default="MANUAL", db_index=True)  # MANUAL, URL, API, etc.
    solar_system_id = models.IntegerField(null=True, blank=True, db_index=True)
    solar_system_name = models.CharField(max_length=128, blank=True, default="", db_index=True)

    # Raw text (can be big but typically manageable)
    raw_text = models.TextField()

    # Optional structured payload (MariaDB supports JSON on modern versions, but keep nullable)
    parsed_json = models.JSONField(null=True, blank=True)

    # Link back to user / character (optional, can be extended later)
    created_by_user_id = models.IntegerField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        sys = self.solar_system_name or self.solar_system_id or "Unknown"
        return f"DScan {self.id} @ {sys}"

class DScanItem(models.Model):
    """Optional normalized scan rows for fast queries."""
    dscan = models.ForeignKey(DScan, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=255, db_index=True)
    type_name = models.CharField(max_length=255, blank=True, default="", db_index=True)
    distance = models.CharField(max_length=64, blank=True, default="")  # keep string for AU/km formats
    category = models.CharField(max_length=64, blank=True, default="", db_index=True)

    class Meta:
        indexes = [models.Index(fields=["type_name", "category"])]

    def __str__(self) -> str:
        return self.name
