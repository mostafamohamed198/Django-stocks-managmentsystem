# Generated by Django 4.1.3 on 2023-01-05 21:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_watchlist_stocks'),
    ]

    operations = [
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('relatedstock', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stock.stock')),
            ],
        ),
    ]
