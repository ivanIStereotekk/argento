from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import environ
import os
from pathlib import Path


env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



class Command(BaseCommand):
    """Command - Creating Super User

    Args:
        BaseCommand (_type_): 
    """
    help = "Create superuser command "
    
    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the superuser')
        parser.add_argument('--email', type=str, help='Email for the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')
    

    def handle(self, *args, **options):
        username = env('DJANGO_SUPERUSER_NAME')
        email = env('DJANGO_SUPERUSER_EMAIL')
        password = env('DJANGO_SUPERUSER_PASS')
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Superuser already exists'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

       