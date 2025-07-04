# Generated by Django 5.1.7 on 2025-04-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("appetizers", "Appetizers"),
                            ("main_course", "Main Course"),
                            ("desserts", "Desserts"),
                            ("beverages", "Beverages"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="menu_items/"),
                ),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Menu Item",
                "verbose_name_plural": "Menu Items",
                "ordering": ["category", "name"],
            },
        ),
    ]
