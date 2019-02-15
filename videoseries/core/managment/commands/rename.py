import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Rename django project'

    def add_arguments(self, parser):
        parser.add_arguments('new_project_name', type=str, help='New project name')

    def handle(self, *args, **kwargs):
        new_project_name=kwargs['new_project_name']

        files_to_rename = ['videoseries/settings/base.py', 'videoseries/wsgi.py', 'manage.py']
        folder_to_rename = 'videoseries'
        old_file_name = 'videoseries'

        for f in files_to_rename:
            with open(f, 'r') as file:
                filedata = file.read()

            filedata = filedata.replace(old_file_name, new_project_name)

            with open(f, 'w') as file:
                file.write(filedata)
        
        os.rename(folder_to_rename, new_project_name)

        self.stdout.write(self.style.SUCCESS('Project has been successfuly renamed to %s' % new_project_name))