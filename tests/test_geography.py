import unittest


try:
    import django
    from django.conf import settings
    from django.core.management import call_command
    from django.test import TestCase
except ImportError:
    django = None
    settings = None
    TestCase = unittest.TestCase


@unittest.skipIf(django is None, "Django is required for geography cache tests")
class GeographyTests(TestCase):
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

    def test_system_context_returns_region_constellation_and_neighbors(self):
        from aa_core_hub.api import (
            get_system_context,
            upsert_constellation,
            upsert_region,
            upsert_solar_system,
            upsert_stargate,
        )

        upsert_region(region_id=10000002, name="The Forge")
        upsert_constellation(
            constellation_id=20000020,
            name="Kimotoro",
            region_id=10000002,
        )
        upsert_solar_system(
            solar_system_id=30000142,
            name="Jita",
            constellation_id=20000020,
            region_id=10000002,
            security_status=0.9,
        )
        upsert_solar_system(
            solar_system_id=30000144,
            name="Perimeter",
            constellation_id=20000020,
            region_id=10000002,
            security_status=1.0,
        )
        upsert_stargate(
            stargate_id=50001234,
            source_system_id=30000142,
            destination_stargate_id=50005678,
            destination_system_id=30000144,
        )

        context = get_system_context(solar_system_id=30000142)

        self.assertEqual(context["system"].name, "Jita")
        self.assertEqual(context["constellation"].name, "Kimotoro")
        self.assertEqual(context["region"].name, "The Forge")
        self.assertEqual(context["neighbor_system_ids"], [30000144])
