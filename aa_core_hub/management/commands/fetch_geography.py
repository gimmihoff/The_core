from django.core.management.base import BaseCommand

from aa_core_hub.services.geography import (
    fetch_constellation_geography,
    fetch_region_geography,
    fetch_system_geography,
)


class Command(BaseCommand):
    help = "Populate Core Hub map cache from ESI"

    def add_arguments(self, parser):
        scope = parser.add_mutually_exclusive_group(required=True)
        scope.add_argument("--system-id", type=int, help="EVE solar system ID")
        scope.add_argument("--constellation-id", type=int, help="EVE constellation ID")
        scope.add_argument("--region-id", type=int, help="EVE region ID")
        parser.add_argument(
            "--no-stargates",
            action="store_true",
            help="Skip stargate detail calls for faster system-only population",
        )

    def handle(self, *args, **opts):
        include_stargates = not opts["no_stargates"]
        if opts["system_id"]:
            system = fetch_system_geography(system_id=opts["system_id"])
            self.stdout.write(self.style.SUCCESS(f"Geography cache updated: {system.name}"))
            return

        if opts["constellation_id"]:
            result = fetch_constellation_geography(
                opts["constellation_id"],
                include_stargates=include_stargates,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "Geography cache updated: "
                    f"{result['constellation_name']} "
                    f"({len(result['systems'])} systems)"
                )
            )
            return

        result = fetch_region_geography(
            opts["region_id"],
            include_stargates=include_stargates,
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Geography cache updated: "
                f"{result['region_name']} "
                f"({len(result['constellations'])} constellations, "
                f"{result['system_count']} systems)"
            )
        )
