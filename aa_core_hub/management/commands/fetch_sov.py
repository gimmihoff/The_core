from django.core.management.base import BaseCommand

from aa_core_hub.services.sov import (
    fetch_sovereignty_campaigns,
    fetch_sovereignty_map,
    fetch_sovereignty_structures,
)


class Command(BaseCommand):
    help = "Populate Core Hub sovereignty cache from ESI"

    def add_arguments(self, parser):
        parser.add_argument(
            "--scope",
            choices=("all", "map", "structures", "campaigns"),
            default="all",
        )

    def handle(self, *args, **opts):
        scope = opts["scope"]
        counts = {}
        if scope in ("all", "map"):
            counts["map"] = fetch_sovereignty_map()
        if scope in ("all", "structures"):
            counts["structures"] = fetch_sovereignty_structures()
        if scope in ("all", "campaigns"):
            counts["campaigns"] = fetch_sovereignty_campaigns()

        summary = ", ".join(f"{name}: {count}" for name, count in counts.items())
        self.stdout.write(self.style.SUCCESS(f"Sovereignty cache updated: {summary}"))
