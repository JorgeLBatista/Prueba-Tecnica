# Generated by Django 5.0.4 on 2024-05-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0003_prestamo_devuelto_alter_prestamo_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
