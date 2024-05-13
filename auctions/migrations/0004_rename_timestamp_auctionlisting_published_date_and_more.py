# Generated by Django 5.0.6 on 2024-05-13 10:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_alter_auctionlisting_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="auctionlisting",
            old_name="timestamp",
            new_name="published_date",
        ),
        migrations.RenameField(
            model_name="auctionlisting",
            old_name="name",
            new_name="title",
        ),
        migrations.AddField(
            model_name="auctionlisting",
            name="category",
            field=models.CharField(
                choices=[
                    ("FAS", "Fashion"),
                    ("ELE", "Electronics"),
                    ("FOO", "Food"),
                    ("DIY", "DIY & Hardware"),
                    ("MUS", "Music Instruments"),
                    ("MOT", "Motors"),
                    ("BOK", "Books"),
                ],
                default="BOK",
                max_length=3,
            ),
        ),
        migrations.AddField(
            model_name="auctionlisting",
            name="seller",
            field=models.ForeignKey(
                default="seller",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="auctionlisting",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=11),
        ),
    ]
