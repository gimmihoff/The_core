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


@unittest.skipIf(django is None, "Django is required for war timer tests")
class WarTimerTests(TestCase):
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

    def test_enemy_structure_timer_appears_in_war_timeline(self):
        from aa_core_hub.api import (
            create_enemy_structure,
            create_structure_timer,
            get_war_timer_timeline,
        )

        structure = create_enemy_structure(
            name="Hostile Astrahus",
            type_id=35832,
            solar_system_id=30000142,
            solar_system_name="Jita",
            fit_notes="[Astrahus, Example Fit]",
        )
        timer = create_structure_timer(
            structure=structure,
            phase="ARMOR",
            occurs_at=timezone.now() + timezone.timedelta(hours=2),
            is_confirmed=True,
            priority=1,
        )

        timeline = list(get_war_timer_timeline(solar_system_id=30000142))

        self.assertEqual(timeline, [timer])
        self.assertEqual(structure.standing, "HOSTILE")
        self.assertEqual(structure.fit_notes, "[Astrahus, Example Fit]")

    def test_enemy_structure_accepts_unknown_type_and_classifies_known_sov(self):
        from aa_core_hub.api import create_enemy_structure

        unknown = create_enemy_structure(
            name="Unrecognized Hostile Asset",
            type_id=999999,
            type_name="Future Structure Type",
        )
        sov = create_enemy_structure(
            name="Hostile IHub",
            type_name="Infrastructure Hub",
            structure_id=12345,
        )

        self.assertEqual(unknown.structure_category, "STRUCTURE")
        self.assertEqual(sov.structure_category, "SOV")

    def test_stargates_are_classified_as_flex_infrastructure(self):
        from aa_core_hub.api import create_or_update_structure

        structure = create_or_update_structure(name="Jita Stargate", type_name="Stargate")

        self.assertEqual(structure.structure_category, "FLEX")
