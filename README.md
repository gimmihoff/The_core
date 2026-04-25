# AA Core Hub

AA Core Hub is the shared Core plugin for AllianceAuth 4.11.2 on MariaDB. It provides canonical storage models, minimal UI pages, and a stable child-plugin API for:

- Structures and standings
- Structure timers for war and defense planning
- D-Scan storage and parsing
- Lightweight system intel annotations
- Solar system celestial cache population via ESI
- Strategic geography cache for regions, constellations, systems, and stargates

## Child Plugin API

Child plugins should import supported models and helpers from `aa_core_hub.api`.

```python
from aa_core_hub.api import (
    DScan,
    DScanItem,
    EveConstellation,
    EveRegion,
    EveSolarSystem,
    EveStargate,
    SolarSystemCelestial,
    Structure,
    StructureTimer,
    SystemIntel,
)
```

The API module also exports:

```python
from aa_core_hub.api import (
    apply_type_defaults,
    create_dscan,
    fetch_system_celestials,
    fetch_system_geography,
    get_neighbor_systems,
    get_dscan_timeline_for_system,
    get_defaults,
    get_system_context,
    parse_dscan,
    sync_structure_status_from_timers,
)
```

`aa_core_hub.models` remains available for Django model discovery and internal framework use, but it is no longer the documented child-plugin import surface.

## Breaking Change

Version 1.3.3 makes `aa_core_hub/` the only source package and removes duplicate root-level modules, checked-in bytecode, and stale generated files. Existing database migrations remain under `aa_core_hub.migrations`; no data migration is required for this cleanup.

Child plugins should update imports from:

```python
from aa_core_hub.models import Structure
```

to:

```python
from aa_core_hub.api import Structure
```

## Permissions

This app registers standard Django model permissions:

- `aa_core_hub.view_structure`, `aa_core_hub.change_structure`, and related structure permissions
- `aa_core_hub.view_dscan`, `aa_core_hub.change_dscan`, and related D-Scan permissions
- default Django permissions for the remaining Core Hub models

Grant these permissions through AllianceAuth Group Management.

## Celestial Cache

Populate a system's celestial cache with:

```bash
python manage.py fetch_celestials --system-id 30000142 --name Jita
```

Use `--no-overwrite` to keep existing rows and add only missing entries.

## Strategic Geography Cache

War-planning and overview child apps should use Core's geography cache for map topology:

```python
from aa_core_hub.api import get_neighbor_systems, get_system_context

context = get_system_context(solar_system_id=30000142)
neighbors = get_neighbor_systems(solar_system_id=30000142)
```

Populate a system, its region, constellation, and outgoing stargates from ESI with:

```bash
python manage.py fetch_geography --system-id 30000142
```

## D-Scan Ingestion

Upload child apps should create D-scans through Core so raw text, parsed JSON, normalized item rows, system linkage, and timestamps stay consistent:

```python
from aa_core_hub.api import create_dscan

dscan = create_dscan(
    raw_text=raw_text,
    solar_system_id=30000142,
    solar_system_name="Jita",
    source="UPLOAD_APP",
    created_by_user_id=request.user.id,
    scanned_at=scanned_at,
)
```

Inspection child apps can build system timelines from Core:

```python
from aa_core_hub.api import get_dscan_timeline_for_system

timeline = get_dscan_timeline_for_system(solar_system_id=30000142, limit=100)
```

## Smoke Checks

Useful checks after install or upgrade:

```bash
python -m compileall aa_core_hub
python manage.py check
python manage.py migrate aa_core_hub --plan
```
