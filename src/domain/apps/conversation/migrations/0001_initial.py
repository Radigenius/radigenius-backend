# Generated by Django 4.2.18 on 2025-03-29 09:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chat",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ("-created_date",),
                "get_latest_by": "created_date",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("content", models.TextField(blank=True, null=True)),
                (
                    "author_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                (
                    "author_type",
                    models.ForeignKey(
                        limit_choices_to={"model__in": ["user", "model"]},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "chat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="messages",
                        to="conversation.chat",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="conversation.message",
                    ),
                ),
            ],
            options={
                "ordering": ("created_date",),
                "get_latest_by": "created_date",
                "abstract": False,
            },
        ),
    ]
