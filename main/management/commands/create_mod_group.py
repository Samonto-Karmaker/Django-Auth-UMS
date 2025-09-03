from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from main.models import Post

class Command(BaseCommand):
    help = 'Create mod group with permissions to add, view, delete posts and ban users'

    def handle(self, *args, **options):
        # Create the 'mod' group
        mod_group, created = Group.objects.get_or_create(name='mod')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created group: mod')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Group "mod" already exists, updating permissions...')
            )
        
        # Get content types
        post_content_type = ContentType.objects.get_for_model(Post)
        user_content_type = ContentType.objects.get(app_label='auth', model='user')
        
        # Define permissions for mod group
        mod_permissions = [
            # Post permissions
            ('add_post', post_content_type),
            ('view_post', post_content_type),
            ('delete_post', post_content_type),
            # User permissions (for banning users)
            ('change_user', user_content_type),  # Needed to modify user.is_active
            ('view_user', user_content_type),    # Needed to see users
        ]
        
        # Clear existing permissions and add new ones
        mod_group.permissions.clear()
        
        permissions_added = 0
        for perm_codename, content_type in mod_permissions:
            try:
                permission = Permission.objects.get(
                    codename=perm_codename,
                    content_type=content_type
                )
                mod_group.permissions.add(permission)
                permissions_added += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Added permission: {perm_codename}')
                )
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'  ✗ Permission {perm_codename} does not exist for {content_type}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nGroup "mod" setup complete!'
                f'\nTotal permissions added: {permissions_added}'
                f'\nMod group can now:'
                f'\n  - Add posts'
                f'\n  - View posts' 
                f'\n  - Delete posts'
                f'\n  - Ban/unban users (change user.is_active)'
            )
        )
        
        # Show current group members
        mod_users = User.objects.filter(groups=mod_group)
        if mod_users.exists():
            self.stdout.write(
                self.style.SUCCESS(f'\nCurrent mod group members:')
            )
            for user in mod_users:
                self.stdout.write(f'  - {user.username} ({user.email})')
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'\nNo users currently in mod group.'
                    f'\nTo add a user to mod group, use:'
                    f'\n  python manage.py shell'
                    f'\n  >>> from django.contrib.auth.models import User, Group'
                    f'\n  >>> user = User.objects.get(username="username")'
                    f'\n  >>> mod_group = Group.objects.get(name="mod")'
                    f'\n  >>> user.groups.add(mod_group)'
                )
            )
