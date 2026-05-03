## Install

1. Install or place the `aa_core_hub` package in your AllianceAuth project environment.
2. Add `aa_core_hub` to `INSTALLED_APPS`.
3. Add the Core Hub URLs:

```python
path("core/", include("aa_core_hub.urls"))
```

4. Run migrations:

```bash
python manage.py migrate aa_core_hub
```

5. Run smoke checks:

```bash
python manage.py check
python manage.py migrate aa_core_hub --plan
```

## Child Plugins

Child plugins should import the stable public API from `aa_core_hub.api`.

```python
from aa_core_hub.api import Structure, StructureTimer, DScan
```

Imports from `aa_core_hub.models` still work for Django internals, but new child-plugin code should not depend on that module as the public contract.

For D-scan upload and inspection workflows, use `create_dscan` and `get_dscan_timeline_for_system` from `aa_core_hub.api` so system linkage, parsed rows, and timeline ordering are consistent across child apps.

Use `DScan.public_id` and `get_dscan_by_public_id` for shareable D-scan permalinks instead of exposing database IDs.

For strategic planning workflows, use `get_system_context`, `get_neighbor_systems`, and the geography models from `aa_core_hub.api`. Populate Core's cache with `python manage.py fetch_geography --system-id <system_id>`.

For bulk geography population, use `python manage.py fetch_geography --constellation-id <constellation_id>` or `python manage.py fetch_geography --region-id <region_id>`. Add `--no-stargates` when you only need systems for search/dropdowns.

For hostile structure and timer workflows, use `create_enemy_structure`, `create_structure_timer`, and `get_war_timer_timeline` from `aa_core_hub.api`.

For sovereignty-aware war planning, run `python manage.py fetch_sov --scope all` and use `get_sov_context` plus the `SovereigntySystem`, `SovereigntyStructure`, and `SovereigntyCampaign` models from `aa_core_hub.api`.
