# AA Core Hub (v1.0.0)

This is the shared **Core** plugin intended to be installed into AllianceAuth **4.11.2** (MariaDB supported).
It provides canonical storage models and minimal UI pages for:

- Structures (friendly/neutral/hostile classification)
- Structure timers (war / defense planning)
- D-Scan storage (raw + optional normalized rows)
- Lightweight system intel annotations

Child plugins should import models from `aa_core_hub.models`.

## Stable API Contract for Child Plugins

```python
from aa_core_hub.models import Structure, StructureTimer, DScan, DScanItem, SystemIntel
```

## Permissions

This app registers standard Django model permissions:
- `aa_core_hub.view_structure`, `aa_core_hub.change_structure`, etc.
- `aa_core_hub.view_dscan`, `aa_core_hub.change_dscan`, etc.

Grant via AllianceAuth Group Management.


# AA Core Hub v1.1.0 (AA 4.11.2 + MariaDB)


# AA Core Hub v1.2.0 – Celestial Cache
Adds:
⦁	SolarSystemCelestial cache (STAR / PLANET / MOON)
⦁	ESI-backed fetcher to populate per-system bodies
Used by Recon for:
⦁	Nearest dropdowns
⦁	Planet-only / moon-only enforcement


# AA Core Hub v1.2.1 – Celestial Populators

Adds:
- Management command to populate SolarSystemCelestial cache via ESI

Usage:
python manage.py fetch_celestials --system-id 30000142 --name Jita

Options:
--no-overwrite   Keep existing entries and only add missing ones
