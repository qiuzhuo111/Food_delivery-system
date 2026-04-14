from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_rider_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="rider_note",
            field=models.CharField(blank=True, max_length=200, verbose_name="骑手备注"),
        ),
    ]
