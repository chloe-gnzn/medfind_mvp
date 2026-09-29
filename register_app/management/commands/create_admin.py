from django.core.management.base import BaseCommand, CommandError

from admin_app.models import Admin


class Command(BaseCommand):
    help = 'Create (or reset the password of) a MedFind Admin account.'

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('password')
        parser.add_argument('--first-name', default='Admin')
        parser.add_argument('--last-name', default='User')
        parser.add_argument('--role', default='admin', choices=['admin', 'super_admin'])

    def handle(self, *args, **opts):
        email = opts['email'].strip().lower()
        if len(opts['password']) < 8:
            raise CommandError('Password must be at least 8 characters.')
        admin, created = Admin.objects.get_or_create(email=email, defaults={
            'first_name': opts['first_name'],
            'last_name': opts['last_name'],
            'role': opts['role'],
        })
        admin.set_password(opts['password'])
        admin.save()
        self.stdout.write(self.style.SUCCESS(
            f'{"Created" if created else "Updated"} admin {email}'))
