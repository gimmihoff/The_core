## Install
1) Put `aa_core_hub` into your AA project root.
2) Add `aa_core_hub` to `INSTALLED_APPS`.
3) Add `path("core/", include("aa_core_hub.urls"))` to urls.py
4) Run: `python manage.py migrate aa_core_hub`
