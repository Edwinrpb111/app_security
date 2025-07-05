from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

from applications.doctor.models import CitaMedica, HorarioAtencion
from applications.core.models import Doctor
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/cita_medica/list.html'
    model = CitaMedica
    context_object_name = 'citas_medica'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(estado__icontains=q1), Q.OR)
            self.query.add(Q(observaciones__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('paciente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_medica_create')
        return context


from applications.doctor.forms.cita import CitaMedicaForm

class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/cita_medica/form.html'
    success_url = reverse_lazy('doctor:cita_medica_list')
    permission_required = 'add_citamedica'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('fecha'):
            initial['fecha'] = self.request.GET.get('fecha')
        if self.request.GET.get('hora'):
            initial['hora_cita'] = self.request.GET.get('hora')
        if self.request.GET.get('doctor'):
            initial['doctor'] = self.request.GET.get('doctor')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Cita Médica'
        context['back_url'] = self.success_url
        return context


class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    form_class = CitaMedicaForm
    template_name = 'doctor/cita_medica/form.html'
    success_url = reverse_lazy('doctor:cita_medica_list')
    permission_required = 'change_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Cita Médica'
        context['back_url'] = self.success_url
        return context


class CitaMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/delete.html'
    success_url = reverse_lazy('doctor:cita_medica_list_view')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Cita Médica'
        context['description'] = f"¿Desea eliminar la cita de: {self.object.paciente} - {self.object.fecha}?"
        context['back_url'] = self.success_url
        return context


class CitaMedicaMainListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/cita_medica/calendar.html'
    model = CitaMedica
    context_object_name = 'citas_medica'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(estado__icontains=q1), Q.OR)
            self.query.add(Q(observaciones__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('paciente', 'doctor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_medica_create')
        context['doctores'] = Doctor.objects.filter(activo=True)
        return context
    
class CitaMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/cita_medica/list.html'
    model = CitaMedica
    context_object_name = 'citas_medica'
    permission_required = 'view_citamedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(estado__icontains=q1), Q.OR)
            self.query.add(Q(observaciones__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('paciente', 'doctor')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:cita_medica_create')
        context['doctores'] = Doctor.objects.filter(activo=True)
        return context



def calendario_eventos_api(request):
    """API para obtener eventos del calendario de citas"""
    doctor_id = request.GET.get('doctor_id')
    fecha_inicio = request.GET.get('start')
    fecha_fin = request.GET.get('end')
    # Normalizar fechas si vienen con hora y zona horaria
    if fecha_inicio and 'T' in fecha_inicio:
        fecha_inicio = fecha_inicio.split('T')[0]
    if fecha_fin and 'T' in fecha_fin:
        fecha_fin = fecha_fin.split('T')[0]
    citas = CitaMedica.objects.select_related('paciente', 'doctor')
    if doctor_id:
        citas = citas.filter(doctor_id=doctor_id)
    if fecha_inicio and fecha_fin:
        citas = citas.filter(fecha__range=[fecha_inicio, fecha_fin])
    
    # Obtener horarios disponibles del doctor
    eventos = []
    
    # Agregar citas existentes
    for cita in citas:
        color = {
            'programada': '#fbbf24',   # amarillo
            'confirmada': '#10b981',   # verde
            'cancelada': '#ef4444',    # rojo
            'completada': '#6366f1',   # azul
            'atendido': '#0ea5e9',     # celeste
            'ocupado': '#a21caf',      # morado
            'disponible': '#fde68a'    # amarillo claro
        }.get(cita.estado, '#6b7280')
        
        eventos.append({
            'id': cita.id,
            'title': f"{cita.paciente.nombres} {cita.paciente.apellidos}",
            'start': f"{cita.fecha}T{cita.hora_cita}",
            'color': color,
            'url': reverse_lazy('doctor:atencion_create_from_cita', args=[cita.id]),
            'extendedProps': {
                'tipo': 'cita',
                'estado': cita.estado,
                'paciente': str(cita.paciente),
                'doctor': str(cita.doctor) if cita.doctor else ''
            }
        })
    
    # Si hay doctor seleccionado, agregar horarios disponibles
    if doctor_id and fecha_inicio and fecha_fin:
        doctor = get_object_or_404(Doctor, id=doctor_id)
        horarios = HorarioAtencion.objects.filter(activo=True)
        
        # Generar slots disponibles basados en horarios
        fecha_actual = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_final = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        while fecha_actual <= fecha_final:
            dia_semana = fecha_actual.strftime('%A').lower()
            
            for horario in horarios.filter(dia_semana=dia_semana):
                # Verificar si ya hay cita en este horario
                cita_existente = citas.filter(
                    fecha=fecha_actual,
                    hora_cita=horario.hora_inicio
                ).exists()
                
                if not cita_existente:
                    eventos.append({
                        'id': f"disponible_{fecha_actual}_{horario.hora_inicio}",
                        'title': "Disponible",
                        'start': f"{fecha_actual}T{horario.hora_inicio}",
                        'color': '#fbbf24',  # amarillo para disponible
                        'url': f"{reverse_lazy('doctor:cita_medica_create')}?fecha={fecha_actual}&hora={horario.hora_inicio}&doctor={doctor_id}",
                        'extendedProps': {
                            'tipo': 'disponible',
                            'doctor': str(doctor)
                        }
                    })
            
            fecha_actual += timedelta(days=1)
    
    return JsonResponse(eventos, safe=False)
