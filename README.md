# AA Core Hub

AA Core Hub is the shared Core plugin for AllianceAuth 4.11.2 on MariaDB. It provides canonical storage models, minimal UI pages, and a stable child-plugin API for:

- Structures and standings
- Structure timers for war and defense planning
- D-Scan storage and parsing
- Lightweight system intel annotations
- Solar system celestial cache population via ESI

## Child Plugin API

Child plugins should import supported models and helpers from `aa_core_hub.api`.

```python
from aa_core_hub.api import (
    DScan,
    DScanItem,
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
    fetch_system_celestials,
    get_defaults,
    parse_dscan,
    sync_structure_status_from_timers,
)
```

`aa_core_hub.models` remains available for Django model discovery and internal framework use, but it is no longer the documented child-plugin import surface.

## Breaking Change

Version 1.3.1 makes `aa_core_hub/` the only source package and removes duplicate root-level modules, checked-in bytecode, and stale generated files. Existing database migrations remain under `aa_core_hub.migrations`; no data migration is required for this cleanup.

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

## Smoke Checks

Useful checks after install or upgrade:

```bash
python -m compileall aa_core_hub
python manage.py check
python manage.py migrate aa_core_hub --plan
```
