import django.db.models.deletion
import medfind_project.session_auth
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
            bases=(medfind_project.session_auth.PasswordMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MedicineCategory',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('category_name', models.TextField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'medicine categories',
                'ordering': ['category_name'],
            },
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('medicine_name', models.CharField(max_length=255)),
                ('generic_name', models.CharField(max_length=255)),
                ('form', models.CharField(max_length=100)),
                ('strength', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medicines', to='home_app.medicinecategory')),
            ],
            options={
                'ordering': ['medicine_name'],
            },
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('search_id', models.AutoField(primary_key=True, serialize=False)),
                ('search_term', models.CharField(max_length=255)),
                ('searched_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_history', to='home_app.user')),
            ],
            options={
                'verbose_name_plural': 'search history',
                'ordering': ['-searched_at'],
            },
        ),
    ]
