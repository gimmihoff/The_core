# Install (AllianceAuth 4.11.2 + MariaDB)

1) Copy plugin into your AllianceAuth project (same level as `manage.py`):

```bash
unzip aa_core_hub-v1.0.0-aa4.11.2-mariadb.zip
mv aa_core_hub /home/allianceserver/myauth/
```

2) Add app to `INSTALLED_APPS` (in your AA project settings):

```python
INSTALLED_APPS += ["aa_core_hub"]
```

3) Install python deps:

```bash
pip install -r aa_core_hub/requirements.txt
```

4) Migrate & collect static:

```bash
python manage.py makemigrations aa_core_hub
python manage.py migrate
python manage.py collectstatic
```

5) Restart services:

```bash
sudo supervisorctl restart all
```

6) Permissions:
Use AllianceAuth **Group Management** to grant permissions like:
- `aa_core_hub.view_structure`
- `aa_core_hub.view_dscan`
to the groups that should have access.

## URL wiring

Add to your main `urls.py`:

```python
path("core/", include("aa_core_hub.urls")),
```

Then visit:

- `/core/` (dashboard)
- `/core/structures/`
- `/core/dscan/`

