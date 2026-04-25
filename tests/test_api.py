import importlib
import unittest


try:
    import django
    from django.conf import settings
except ImportError:
    django = None
    settings = None


@unittest.skipIf(django is None, "Django is required for AA Core Hub API smoke tests")
class PublicApiTests(unittest.TestCase):
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

    def test_public_api_exports_child_plugin_contract(self):
        api = importlib.import_module("aa_core_hub.api")

        expected_exports = {
            "DScan",
            "DScanItem",
            "EveConstellation",
            "EveRegion",
            "EveSolarSystem",
            "EveStargate",
            "SolarSystemCelestial",
            "Structure",
            "StructureTimer",
            "SystemIntel",
            "apply_type_defaults",
            "create_dscan",
            "create_enemy_structure",
            "create_or_update_structure",
            "create_structure_timer",
            "fetch_system_celestials",
            "fetch_system_geography",
            "get_neighbor_systems",
            "get_dscan_timeline_for_system",
            "get_defaults",
            "get_system_context",
            "get_war_timer_timeline",
            "parse_dscan",
            "sync_structure_status_from_timers",
            "upsert_constellation",
            "upsert_region",
            "upsert_solar_system",
            "upsert_stargate",
        }

        self.assertTrue(expected_exports.issubset(set(api.__all__)))
        for name in expected_exports:
            self.assertTrue(hasattr(api, name), name)
