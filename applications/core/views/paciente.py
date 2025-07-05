from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from applications.core.models import Paciente
from applications.core.forms.paciente import PacienteForm

"""  Vista para buscar pacientes mediante AJAX. Por nombres, apellidos, cédula o teléfono. """


@login_required
@require_http_methods(["GET"])
def paciente_find(request):
    try:
        # Obtener el parámetro de búsqueda
        query = request.GET.get('q', '').strip()
        print(f"🔍 Búsqueda recibida: '{query}'")

        # Validar que se proporcione al menos 3 caracteres
        if len(query) < 3:
            return JsonResponse({
                'success': False,
                'message': 'Debe proporcionar al menos 3 caracteres para la búsqueda',
                'pacientes': []
            })

        # Construir la consulta de búsqueda de forma más simple
        pacientes_query = Paciente.objects.filter(
            Q(activo=True) & (
                    Q(nombres__icontains=query) |
                    Q(apellidos__icontains=query) |
                    Q(cedula_ecuatoriana__icontains=query) |
                    Q(dni__icontains=query) |
                    Q(telefono__icontains=query)
            )
        ).select_related('tipo_sangre').order_by('apellidos', 'nombres')

        # Limitar resultados para mejorar rendimiento
        pacientes_query = pacientes_query[:20]
        print(f"📊 Encontrados: {pacientes_query.count()} pacientes")

        # Convertir a lista de diccionarios de forma más simple
        pacientes_data = []
        for paciente in pacientes_query:
            try:
                # Calcular edad de forma segura
                edad = paciente.edad if paciente.edad else 0

                paciente_dict = {
                    'id': paciente.id,
                    'nombres': paciente.nombres,
                    'apellidos': paciente.apellidos,
                    'cedula_ecuatoriana': paciente.cedula_ecuatoriana,
                    'dni': paciente.dni,
                    'fecha_nacimiento': paciente.fecha_nacimiento.isoformat() if paciente.fecha_nacimiento else None,
                    'edad': edad,
                    'telefono': paciente.telefono,
                    'email': paciente.email,
                    'sexo': paciente.sexo,
                    'estado_civil': paciente.estado_civil,
                    'direccion': paciente.direccion,
                    'latitud': float(paciente.latitud) if paciente.latitud else None,
                    'longitud': float(paciente.longitud) if paciente.longitud else None,
                    'tipo_sangre': paciente.tipo_sangre.tipo if paciente.tipo_sangre else None,
                    'foto_url': paciente.get_image,

                    # Historia clínica
                    'antecedentes_personales': paciente.antecedentes_personales,
                    'antecedentes_quirurgicos': paciente.antecedentes_quirurgicos,
                    'antecedentes_familiares': paciente.antecedentes_familiares,
                    'alergias': paciente.alergias,
                    'medicamentos_actuales': paciente.medicamentos_actuales,
                    'habitos_toxicos': paciente.habitos_toxicos,
                    'vacunas': paciente.vacunas,
                    'antecedentes_gineco_obstetricos': paciente.antecedentes_gineco_obstetricos,

                    # Atenciones simplificadas - solo contar por ahora
                    'atenciones': [],
                    'total_atenciones': 0
                }
                pacientes_data.append(paciente_dict)
                print(f"✅ Paciente procesado: {paciente.nombres} {paciente.apellidos}")
                
            except Exception as e:
                print(f"❌ Error procesando paciente {paciente.id}: {e}")
                continue

        print(f"📦 Enviando {len(pacientes_data)} pacientes")
        return JsonResponse({
            'success': True,
            'pacientes': pacientes_data,
            'total': len(pacientes_data),
            'query': query
        })

    except Exception as e:
        print(f"❌ Error en paciente_find: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error en la búsqueda: {str(e)}',
            'pacientes': []
        }, status=500)


from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from applications.core.models import Paciente
from applications.security.components.mixin_crud import PermissionMixin, ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from django.contrib import messages

class PacienteListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/pacientes/list.html'
    model = Paciente
    context_object_name = 'pacientes'
    permission_required = 'view_paciente'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        filters = Q()
        if query:
            filters |= Q(nombres__icontains=query)
            filters |= Q(apellidos__icontains=query)
            filters |= Q(cedula_ecuatoriana__icontains=query)
        return self.model.objects.filter(filters).order_by('apellidos', 'nombres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:paciente_create')
        return context


class PacienteCreateView(PermissionMixin, CreateViewMixin, CreateView):

    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'add_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Registrar Paciente'
        context['back_url'] = self.success_url
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class PacienteUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):

    model = Paciente
    template_name = 'core/pacientes/form.html'
    form_class = PacienteForm
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'change_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Paciente'
        context['back_url'] = self.success_url
        return context


class PacienteDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Paciente
    template_name = 'core/pacientes/delete.html'
    success_url = reverse_lazy('core:paciente_list')
    permission_required = 'delete_paciente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Paciente'
        context['description'] = f"¿Desea eliminar al paciente: {self.object.nombres} {self.object.apellidos}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        paciente_nombre = f"{self.object.nombres} {self.object.apellidos}"
        response = super().form_valid(form)
        messages.success(self.request, f"Éxito al eliminar al paciente {paciente_nombre}.")
        return response