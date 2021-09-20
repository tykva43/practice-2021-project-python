# Generated by Django 3.2.2 on 2021-08-16 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_limit', models.FloatField(verbose_name='Лимит суммы')),
                ('criterion', models.CharField(choices=[('gt', 'больше'), ('lt', 'меньше')], max_length=2, verbose_name='Критерий')),
                ('color', models.CharField(max_length=7, verbose_name='Цвет (hex)')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='budget.transactioncategory', verbose_name='Категория')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
                ('validity', models.DurationField(choices=[('1 day, 0:00:00', '1 день'), ('7 days, 0:00:00', '7 дней'), ('30 days, 0:00:00', '30 дней')], default='7 days 0:00:00', verbose_name='Срок действия')),
            ],
            options={
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
            },
        ),
    ]
