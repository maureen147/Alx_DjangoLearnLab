from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book

class Command(BaseCommand):
    help = 'Creates default groups and assigns permissions'

    def handle(self, *args, **options):
        # Get content type for Book model
        content_type = ContentType.objects.get_for_model(Book)
        
        # Get all permissions for Book model
        book_permissions = Permission.objects.filter(content_type=content_type)
        
        # Create groups and assign permissions
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            view_perm = Permission.objects.get(codename='can_view_book', content_type=content_type)
            viewers_group.permissions.add(view_perm)
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            view_perm = Permission.objects.get(codename='can_view_book', content_type=content_type)
            create_perm = Permission.objects.get(codename='can_create_book', content_type=content_type)
            edit_perm = Permission.objects.get(codename='can_edit_book', content_type=content_type)
            editors_group.permissions.add(view_perm, create_perm, edit_perm)
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            # Admins get all permissions for Book model
            for perm in book_permissions:
                admins_group.permissions.add(perm)
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        
        self.stdout.write(self.style.SUCCESS('Successfully set up all groups and permissions'))
