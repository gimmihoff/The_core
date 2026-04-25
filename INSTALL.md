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
