# Generated by Django 3.0.4 on 2020-04-04 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200404_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryservices',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category_service', to='dashboard.ClinicServices'),
        ),
    ]