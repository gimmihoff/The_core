# AA Core Hub v1.2.1 – Celestial Populators

Adds:
- Management command to populate SolarSystemCelestial cache via ESI

Usage:
python manage.py fetch_celestials --system-id 30000142 --name Jita

Options:
--no-overwrite   Keep existing entries and only add missing ones
