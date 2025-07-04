from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.doctor.models import CitaMedica
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


class CitaMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/form.html'
    fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
    success_url = reverse_lazy('doctor:cita_medica_list')
    permission_required = 'add_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Cita Médica'
        context['back_url'] = self.success_url
        return context


class CitaMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = CitaMedica
    template_name = 'doctor/cita_medica/form.html'
    fields = ['paciente', 'fecha', 'hora_cita', 'estado', 'observaciones']
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
    success_url = reverse_lazy('doctor:cita_medica_list')
    permission_required = 'delete_citamedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Cita Médica'
        context['description'] = f"¿Desea eliminar la cita de: {self.object.paciente} - {self.object.fecha}?"
        context['back_url'] = self.success_url
        return context
