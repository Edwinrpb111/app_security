from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from applications.security.models import User


class Command(BaseCommand):
    help = 'Crea el grupo User con permisos básicos'

    def handle(self, *args, **options):
        # Crear o obtener el grupo User
        user_group, created = Group.objects.get_or_create(name='User')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "User" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('El grupo "User" ya existe')
            )

        # Asignar permisos básicos al grupo User
        basic_permissions = [
            'change_userprofile',  # Cambiar su propio perfil
            'view_citamedica',     # Ver citas médicas
            'add_citamedica',      # Crear citas médicas
        ]

        # Agregar permisos si existen
        added_permissions = []
        for perm_codename in basic_permissions:
            try:
                permission = Permission.objects.get(codename=perm_codename)
                user_group.permissions.add(permission)
                added_permissions.append(perm_codename)
                self.stdout.write(f'Permiso "{perm_codename}" agregado al grupo User')
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Permiso "{perm_codename}" no encontrado')
                )

        if added_permissions:
            self.stdout.write(
                self.style.SUCCESS(f'Se agregaron {len(added_permissions)} permisos al grupo User')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Configuración del grupo User completada')
        )
