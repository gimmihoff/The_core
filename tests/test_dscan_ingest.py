import unittest


try:
    import django
    from django.conf import settings
    from django.core.management import call_command
    from django.test import TestCase
    from django.utils import timezone
except ImportError:
    django = None
    settings = None
    TestCase = unittest.TestCase


@unittest.skipIf(django is None, "Django is required for D-scan ingestion tests")
class DScanIngestTests(TestCase):
    @classmethod
    def setUpClass(cls):
        if not settings.configured:
            settings.configure(
                DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
                INSTALLED_APPS=["aa_core_hub"],
                SECRET_KEY="test",
                USE_TZ=True,
                DATABASES={
                    "default": {
                        "ENGINE": "django.db.backends.sqlite3",
                        "NAME": ":memory:",
                    },
                },
            )
        django.setup()
        call_command("migrate", "aa_core_hub", verbosity=0)
        super().setUpClass()

    def test_create_dscan_links_system_and_normalizes_items(self):
        from aa_core_hub.api import create_dscan

        scanned_at = timezone.now()
        dscan = create_dscan(
            raw_text="Astrahus\tUpwell Structure\t1,000 km\nProbe\tCombat Scanner Probe\t2 AU",
            solar_system_id=30000142,
            solar_system_name="Jita",
            source="UPLOAD_APP",
            created_by_user_id=123,
            scanned_at=scanned_at,
        )

        self.assertEqual(dscan.solar_system_id, 30000142)
        self.assertEqual(dscan.solar_system_name, "Jita")
        self.assertEqual(dscan.scanned_at, scanned_at)
        self.assertEqual(dscan.items.count(), 2)
        self.assertEqual(dscan.items.order_by("id").first().category, "STRUCTURE")

    def test_timeline_filters_by_system(self):
        from aa_core_hub.api import create_dscan, get_dscan_timeline_for_system

        create_dscan(raw_text="A\tAstrahus\t1 km", solar_system_id=1, solar_system_name="One")
        create_dscan(raw_text="B\tAstrahus\t1 km", solar_system_id=2, solar_system_name="Two")

        timeline = list(get_dscan_timeline_for_system(solar_system_id=1))

        self.assertEqual(len(timeline), 1)
        self.assertEqual(timeline[0].solar_system_id, 1)
