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


@unittest.skipIf(django is None, "Django is required for sovereignty tests")
class SovereigntyTests(TestCase):
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

    def test_sov_context_groups_system_structures_and_campaigns(self):
        from aa_core_hub.api import (
            get_sov_context,
            upsert_sov_campaign,
            upsert_sov_structure,
            upsert_sov_system,
        )

        upsert_sov_system({"system_id": 30000142, "alliance_id": 99000001})
        upsert_sov_structure(
            {
                "structure_id": 1001,
                "structure_type_id": 32458,
                "solar_system_id": 30000142,
                "alliance_id": 99000001,
            }
        )
        upsert_sov_campaign(
            {
                "campaign_id": 2001,
                "event_type": "tcu_defense",
                "solar_system_id": 30000142,
                "defender_id": 99000001,
            }
        )

        context = get_sov_context(solar_system_id=30000142)

        self.assertEqual(context["system"].alliance_id, 99000001)
        self.assertEqual(len(context["structures"]), 1)
        self.assertEqual(len(context["campaigns"]), 1)
