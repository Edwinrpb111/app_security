import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proy_clinico.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from applications.security.models import GroupModulePermission, Menu, Module
from applications.doctor.models import ServiciosAdicionales

def load_facturacion_data():
    print("Cargando datos de facturación médica...")
    
    # 1. Crear servicios adicionales de ejemplo
    servicios = [
        {
            'nombre_servicio': 'Consulta General',
            'costo_servicio': 25.00,
            'descripcion': 'Consulta médica general básica'
        },
        {
            'nombre_servicio': 'Consulta Especializada',
            'costo_servicio': 45.00,
            'descripcion': 'Consulta con médico especialista'
        },
        {
            'nombre_servicio': 'Radiografía',
            'costo_servicio': 35.00,
            'descripcion': 'Examen radiográfico'
        },
        {
            'nombre_servicio': 'Laboratorio Clínico',
            'costo_servicio': 15.00,
            'descripcion': 'Exámenes de laboratorio básicos'
        },
        {
            'nombre_servicio': 'Electrocardiograma',
            'costo_servicio': 20.00,
            'descripcion': 'Examen electrocardiográfico'
        },
        {
            'nombre_servicio': 'Curaciones',
            'costo_servicio': 10.00,
            'descripcion': 'Curación de heridas menores'
        },
        {
            'nombre_servicio': 'Inyecciones',
            'costo_servicio': 5.00,
            'descripcion': 'Aplicación de medicamentos inyectables'
        }
    ]
    
    for servicio_data in servicios:
        servicio, created = ServiciosAdicionales.objects.get_or_create(
            nombre_servicio=servicio_data['nombre_servicio'],
            defaults={
                'costo_servicio': servicio_data['costo_servicio'],
                'descripcion': servicio_data['descripcion'],
                'activo': True
            }
        )
        if created:
            print(f"✓ Servicio creado: {servicio.nombre_servicio}")
        else:
            print(f"○ Servicio ya existe: {servicio.nombre_servicio}")
    
    # 2. Verificar o crear el módulo de facturación si no existe
    try:
        menu_consultas = Menu.objects.get(name='Consultas')
        module_facturacion, created = Module.objects.get_or_create(
            url='doctor:facturacion_medica_list',
            defaults={
                'name': 'Facturación Médica',
                'menu': menu_consultas,
                'description': 'Sistema completo de facturación médica',
                'icon': 'bi bi-receipt',
                'order': 4
            }
        )
        if created:
            print(f"✓ Módulo creado: {module_facturacion.name}")
        else:
            print(f"○ Módulo ya existe: {module_facturacion.name}")
    except Menu.DoesNotExist:
        print("⚠ Menú 'Consultas' no encontrado. Se omite la creación del módulo.")
        return
    
    # 3. Crear permisos de facturación si no existen
    try:
        facturacion_ct = ContentType.objects.get(app_label='doctor', model='facturacionmedica')
        
        permisos = [
            ('view_facturacionmedica', 'Can view Facturación Médica'),
            ('add_facturacionmedica', 'Can add Facturación Médica'),
            ('change_facturacionmedica', 'Can change Facturación Médica'),
            ('delete_facturacionmedica', 'Can delete Facturación Médica')
        ]
        
        permisos_creados = []
        for codename, name in permisos:
            permiso, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=facturacion_ct,
                defaults={'name': name}
            )
            permisos_creados.append(permiso)
            if created:
                print(f"✓ Permiso creado: {name}")
            else:
                print(f"○ Permiso ya existe: {name}")
        
        # 4. Asignar permisos al módulo
        module_facturacion.permissions.add(*permisos_creados)
        print(f"✓ Permisos asignados al módulo de facturación")
        
        # 5. Crear permisos para grupos si existen
        try:
            group_medicos = Group.objects.get(name='Médicos')
            gmp_medicos, created = GroupModulePermission.objects.get_or_create(
                group=group_medicos,
                module=module_facturacion
            )
            gmp_medicos.permissions.add(*permisos_creados)
            if created:
                print(f"✓ Permisos asignados al grupo Médicos")
            else:
                print(f"○ Permisos ya asignados al grupo Médicos")
        except Group.DoesNotExist:
            print("⚠ Grupo 'Médicos' no encontrado")
        
        try:
            group_asistentes = Group.objects.get(name='Asistentes')
            gmp_asistentes, created = GroupModulePermission.objects.get_or_create(
                group=group_asistentes,
                module=module_facturacion
            )
            # Solo permisos de ver y agregar para asistentes
            gmp_asistentes.permissions.add(permisos_creados[0], permisos_creados[1])  # view y add
            if created:
                print(f"✓ Permisos limitados asignados al grupo Asistentes")
            else:
                print(f"○ Permisos ya asignados al grupo Asistentes")
        except Group.DoesNotExist:
            print("⚠ Grupo 'Asistentes' no encontrado")
            
    except ContentType.DoesNotExist:
        print("⚠ ContentType para FacturacionMedica no encontrado. ¿Se ejecutaron las migraciones?")
    
    print("\n✅ Carga de datos de facturación médica completada!")

if __name__ == '__main__':
    load_facturacion_data()
