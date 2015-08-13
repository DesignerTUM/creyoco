from django.core.management.base import BaseCommand
from django.conf import settings
from subprocess import call

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_arguments('output_path', type=open)

    def handle(self, *args, **options):
        dbsettings = settings.DATABASES['default']
        dbname = dbsettings['NAME']
        dbuser = dbsettings['USER']
        dbpassword = dbsettings['PASSWORD']

        output = open(args[0], 'w')
        call(['mysqldump', dbname, '-u', dbuser, "-p{}".format(dbpassword)], stdout=output)
