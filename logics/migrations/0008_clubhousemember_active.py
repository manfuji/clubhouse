# Generated by Django 4.1.4 on 2023-06-01 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logics", "0007_requesttojoingroup_clubhousemember"),
    ]

    operations = [
        migrations.AddField(
            model_name="clubhousemember",
            name="active",
            field=models.BooleanField(default=False),
        ),
    ]