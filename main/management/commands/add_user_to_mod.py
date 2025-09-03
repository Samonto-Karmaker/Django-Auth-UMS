from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = 'Add a user to the mod group'

    def add_arguments(self, parser):
        parser.add_argument(
            'username',
            type=str,
            help='Username of the user to add to mod group'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            # Get the user
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User "{username}" does not exist.')
        
        try:
            # Get the mod group
            mod_group = Group.objects.get(name='mod')
        except Group.DoesNotExist:
            raise CommandError(
                'Mod group does not exist. Please run "python manage.py create_mod_group" first.'
            )
        
        # Check if user is already in the group
        if user.groups.filter(name='mod').exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" is already in the mod group.')
            )
        else:
            # Add user to mod group
            user.groups.add(mod_group)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added "{username}" to mod group.')
            )
        
        # Show user's current groups
        user_groups = user.groups.all()
        if user_groups:
            self.stdout.write(f'\n{username} is now member of these groups:')
            for group in user_groups:
                self.stdout.write(f'  - {group.name}')
        else:
            self.stdout.write(f'\n{username} is not member of any groups.')
