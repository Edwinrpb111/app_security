from django.http import JsonResponse
from applications.doctor.models import ServiciosAdicionales

def servicio_info(request):
    servicio_id = request.GET.get('id')
    if not servicio_id:
        return JsonResponse({'error': 'No id provided'}, status=400)
    try:
        servicio = ServiciosAdicionales.objects.get(pk=servicio_id)
        return JsonResponse({
            'id': servicio.id,
            'nombre_servicio': servicio.nombre_servicio,
            'costo_servicio': float(servicio.costo_servicio),
            'descripcion': servicio.descripcion or ''
        })
    except ServiciosAdicionales.DoesNotExist:
        return JsonResponse({'error': 'Servicio not found'}, status=404)
