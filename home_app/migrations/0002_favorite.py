import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_app', '0001_initial'),
        ('pharmacy_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('favorite_id', models.AutoField(primary_key=True, serialize=False)),
                ('favorite_type', models.CharField(choices=[('medicine', 'Medicine'), ('pharmacy', 'Pharmacy')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='home_app.medicine')),
                ('pharmacy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='pharmacy_app.pharmacy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='home_app.user')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
