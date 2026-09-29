"""
python manage.py seed_demo

Fills the database (Supabase) with sample data covering every ERD table so
you can click around the whole app right away. Safe to run more than once.

Demo logins (password for all: MedFind123!)
    admin@medfind.test     (Admin)
    user@medfind.test      (User)
    colon@medfind.test     (Pharmacy, approved)
    mabolo@medfind.test    (Pharmacy, approved)
    newpharm@medfind.test  (Pharmacy, pending -- to try the verification flow)
"""
from datetime import time
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from admin_app.models import Admin
from home_app.models import Favorite, Medicine, MedicineCategory, SearchHistory, User
from login_app.utils import log_activity
from pharmacy_app.models import Inventory, OperatingHours, Pharmacy, PharmacyVerification

PASSWORD = 'MedFind123!'

CATEGORIES = {
    'Pain relievers': 'Analgesics and anti-inflammatory medicines',
    'Antibiotics': 'Medicines that treat bacterial infections',
    'Allergy': 'Antihistamines and allergy relief',
    'Heart & blood pressure': 'Antihypertensives and cardiac medicines',
    'Diabetes': 'Blood sugar control',
    'Digestive health': 'Antacids and stomach medicines',
    'Respiratory': 'Asthma and cough/cold medicines',
}

# brand, generic, category, form, strength
MEDICINES = [
    ('Biogesic', 'Paracetamol', 'Pain relievers', 'Tablet', '500 mg'),
    ('Medicol Advance', 'Ibuprofen', 'Pain relievers', 'Softgel capsule', '200 mg'),
    ('Amoxil', 'Amoxicillin', 'Antibiotics', 'Capsule', '500 mg'),
    ('Zyrtec', 'Cetirizine', 'Allergy', 'Tablet', '10 mg'),
    ('Cozaar', 'Losartan', 'Heart & blood pressure', 'Tablet', '50 mg'),
    ('Glucophage', 'Metformin', 'Diabetes', 'Tablet', '500 mg'),
    ('Losec', 'Omeprazole', 'Digestive health', 'Capsule', '20 mg'),
    ('Imodium', 'Loperamide', 'Digestive health', 'Capsule', '2 mg'),
    ('Ventolin', 'Salbutamol', 'Respiratory', 'Inhaler', '100 mcg'),
]

# email, business name, phone, address, status
PHARMACIES = [
    ('colon@medfind.test', 'Colon Health Pharmacy', '032 255 0101', 'Colon Street, Cebu City', 'approved'),
    ('mabolo@medfind.test', 'Mabolo Wellness Drugstore', '032 255 0102', 'Mabolo, Cebu City', 'approved'),
    ('newpharm@medfind.test', 'Fresh Start Drugstore', '032 255 0103', 'Lahug, Cebu City', 'pending'),
]


class Command(BaseCommand):
    help = 'Seed demo data for every MedFind table.'

    def handle(self, *args, **options):
        admin, _ = Admin.objects.get_or_create(
            email='admin@medfind.test',
            defaults={'first_name': 'Ana', 'last_name': 'Admin', 'role': 'super_admin'})
        admin.set_password(PASSWORD)
        admin.save()

        user, _ = User.objects.get_or_create(
            email='user@medfind.test',
            defaults={'first_name': 'Juan', 'last_name': 'Dela Cruz', 'phone_number': '0917 000 0000'})
        user.set_password(PASSWORD)
        user.save()

        cats = {}
        for name, desc in CATEGORIES.items():
            cats[name], _ = MedicineCategory.objects.get_or_create(
                category_name=name, defaults={'description': desc})

        meds = []
        for brand, generic, cat, form, strength in MEDICINES:
            med, _ = Medicine.objects.get_or_create(
                medicine_name=brand, strength=strength,
                defaults={'generic_name': generic, 'category': cats[cat], 'form': form,
                          'description': f'{generic} {strength} {form.lower()}.'})
            meds.append(med)

        pharmacies = []
        for email, name, phone, address, status in PHARMACIES:
            ph, _ = Pharmacy.objects.get_or_create(email=email, defaults={
                'business_name': name, 'contact_number': phone, 'address': address,
                'verification_status': status})
            ph.set_password(PASSWORD)
            ph.save()
            pharmacies.append(ph)

            # Mon-Sat 8:00-20:00, Sunday closed
            for day in range(7):
                OperatingHours.objects.get_or_create(
                    pharmacy=ph, days_of_week=day,
                    defaults={'opening_time': None if day == 6 else time(8, 0),
                              'closing_time': None if day == 6 else time(20, 0),
                              'is_closed': day == 6})

            # verification records
            if not ph.verifications.exists():
                if status == 'approved':
                    PharmacyVerification.objects.create(
                        pharmacy=ph, reviewed_by=admin, status='approved',
                        document_path='verification_docs/sample_permit.pdf',
                        reviewed_at=timezone.now(), remarks='Documents verified.')
                else:
                    PharmacyVerification.objects.create(
                        pharmacy=ph, status='pending',
                        document_path='verification_docs/sample_permit.pdf')

        # inventory for the two approved pharmacies
        for p_index, ph in enumerate(pharmacies[:2]):
            for m_index, med in enumerate(meds):
                if (m_index + p_index) % 4 == 3:
                    continue  # not every pharmacy stocks everything
                stock = [0, 6, 40, 120][(m_index + p_index) % 4]
                status = 'out_of_stock' if stock == 0 else 'low_stock' if stock < 10 else 'available'
                Inventory.objects.get_or_create(
                    pharmacy=ph, medicine=med,
                    defaults={'price': Decimal(5 + m_index * 3 + p_index * 2) + Decimal('0.50'),
                              'stock_quantity': stock, 'availability_status': status})

        # favorites + search history for the demo user
        Favorite.objects.get_or_create(user=user, favorite_type='medicine', medicine=meds[0])
        Favorite.objects.get_or_create(user=user, favorite_type='pharmacy', pharmacy=pharmacies[0])
        for term in ('paracetamol', 'amoxicillin'):
            if not SearchHistory.objects.filter(user=user, search_term=term).exists():
                SearchHistory.objects.create(user=user, search_term=term)

        log_activity('admin', admin.pk, 'seed_demo', 'Demo data seeded.')
        self.stdout.write(self.style.SUCCESS('Demo data ready. Logins use password: ' + PASSWORD))
