from django.core.management.base import BaseCommand

from aa_core_hub.services.geography import fetch_system_geography


class Command(BaseCommand):
    help = "Populate Core Hub map cache for one solar system and its outgoing stargates"

    def add_arguments(self, parser):
        parser.add_argument("--system-id", type=int, required=True, help="EVE solar system ID")

    def handle(self, *args, **opts):
        system = fetch_system_geography(system_id=opts["system_id"])
        self.stdout.write(self.style.SUCCESS(f"Geography cache updated: {system.name}"))
