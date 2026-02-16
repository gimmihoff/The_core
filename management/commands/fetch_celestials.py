from django.core.management.base import BaseCommand
from aa_core_hub.services.celestial_fetch import fetch_system_celestials

class Command(BaseCommand):
    help = "Populate celestial cache (planets/moons/star) for a solar system"

    def add_arguments(self, parser):
        parser.add_argument("--system-id", type=int, required=True, help="EVE solar system ID")
        parser.add_argument("--name", type=str, required=True, help="Solar system name (for display)")
        parser.add_argument("--no-overwrite", action="store_true", help="Do not delete existing cache first")

    def handle(self, *args, **opts):
        count = fetch_system_celestials(
            system_id=opts["system_id"],
            system_name=opts["name"],
            overwrite=not opts["no_overwrite"],
        )
        self.stdout.write(self.style.SUCCESS(f"Celestial cache updated: {count} entries"))
