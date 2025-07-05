from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from applications.core.models import Paciente, TipoSangre
import json

@csrf_exempt
@require_POST
def paciente_create_api(request):
    try:
        data = request.POST.dict()
        if not data:
            data = json.loads(request.body.decode())

        nombres = data.get('nombres', '').strip()
        apellidos = data.get('apellidos', '').strip()
        cedula_ecuatoriana = data.get('cedula_ecuatoriana', '').strip()
        dni = data.get('dni', '').strip() or None
        fecha_nacimiento = parse_date(data.get('fecha_nacimiento', ''))
        telefono = data.get('telefono', '').strip()
        email = data.get('email', '').strip() or None
        sexo = data.get('sexo', '').strip()
        estado_civil = data.get('estado_civil', '').strip()
        direccion = data.get('direccion', '').strip()
        latitud = data.get('latitud') or None
        longitud = data.get('longitud') or None
        tipo_sangre_val = data.get('tipo_sangre') or None

        tipo_sangre = None
        if tipo_sangre_val:
            tipo_sangre = TipoSangre.objects.filter(tipo=tipo_sangre_val).first()

        paciente = Paciente.objects.create(
            nombres=nombres,
            apellidos=apellidos,
            cedula_ecuatoriana=cedula_ecuatoriana,
            dni=dni,
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono,
            email=email,
            sexo=sexo,
            estado_civil=estado_civil,
            direccion=direccion,
            latitud=latitud or None,
            longitud=longitud or None,
            tipo_sangre=tipo_sangre
        )
        return JsonResponse({'success': True, 'id': paciente.id, 'message': 'Paciente creado'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
