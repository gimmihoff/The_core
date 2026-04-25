import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aa_core_hub", "0006_sov_cache_structure_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="dscan",
            name="public_id",
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AddIndex(
            model_name="dscan",
            index=models.Index(fields=["public_id", "created_at"], name="aa_core_hub_public__1d8b98_idx"),
        ),
    ]
