from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from django.views import View

from applications.doctor.models import HorarioAtencion
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class HorariosDoctorAPIView(View):
    def get(self, request):
        doctor_id = request.GET.get('doctor_id')
        if not doctor_id:
            return JsonResponse({'horarios': []})
        
        try:
            horarios = HorarioAtencion.objects.filter(
                doctor_id=doctor_id,
                activo=True
            ).values(
                'dia_semana',
                'hora_inicio',
                'hora_fin',
                'intervalo_desde',
                'intervalo_hasta'
            )
            
            horarios_list = []
            for horario in horarios:
                horarios_list.append({
                    'dia_semana': horario['dia_semana'],
                    'hora_inicio': horario['hora_inicio'].strftime('%H:%M') if horario['hora_inicio'] else None,
                    'hora_fin': horario['hora_fin'].strftime('%H:%M') if horario['hora_fin'] else None,
                    'intervalo_desde': horario['intervalo_desde'].strftime('%H:%M') if horario['intervalo_desde'] else None,
                    'intervalo_hasta': horario['intervalo_hasta'].strftime('%H:%M') if horario['intervalo_hasta'] else None,
                })
            
            return JsonResponse({'horarios': horarios_list})
        except Exception as e:
            return JsonResponse({'horarios': []})


class DiasOcupadosAPIView(View):
    def get(self, request):
        doctor_id = request.GET.get('doctor_id')
        if not doctor_id:
            return JsonResponse({'dias_ocupados': []})
        
        try:
            # Obtener todos los días ya ocupados por este doctor
            dias_ocupados = HorarioAtencion.objects.filter(
                doctor_id=doctor_id,
                activo=True
            ).values_list('dia_semana', flat=True).distinct()
            
            return JsonResponse({
                'dias_ocupados': list(dias_ocupados)
            })
        except Exception as e:
            return JsonResponse({'dias_ocupados': []})


class HorarioAtencionListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/horario_atencion/list.html'
    model = HorarioAtencion
    context_object_name = 'horarios_atencion'
    permission_required = 'view_horarioatencion'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(dia_semana__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:horario_atencion_create')
        return context



from applications.doctor.forms.horarioAtencion import HorarioAtencionForm

class HorarioAtencionCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    form_class = HorarioAtencionForm
    template_name = 'doctor/horario_atencion/form.html'
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'add_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Horario de Atención'
        context['back_url'] = self.success_url
        return context


class HorarioAtencionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    form_class = HorarioAtencionForm
    template_name = 'doctor/horario_atencion/form.html'
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'change_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Horario de Atención'
        context['back_url'] = self.success_url
        return context


class HorarioAtencionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    template_name = 'doctor/horario_atencion/delete.html'
    success_url = reverse_lazy('doctor:horario_atencion_list')
    permission_required = 'delete_horarioatencion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Horario de Atención'
        context['description'] = f"¿Desea eliminar el horario: {self.object.dia_semana} {self.object.hora_inicio}-{self.object.hora_fin}?"
        context['back_url'] = self.success_url
        return context
