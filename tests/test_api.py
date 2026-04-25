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
            "SolarSystemCelestial",
            "Structure",
            "StructureTimer",
            "SystemIntel",
            "apply_type_defaults",
            "fetch_system_celestials",
            "get_defaults",
            "parse_dscan",
            "sync_structure_status_from_timers",
        }

        self.assertTrue(expected_exports.issubset(set(api.__all__)))
        for name in expected_exports:
            self.assertTrue(hasattr(api, name), name)
