from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Doctor
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class DoctorListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/doctor/list.html'
    model = Doctor
    context_object_name = 'doctores'
    permission_required = 'view_doctor'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombres__icontains=q1), Q.OR)
            self.query.add(Q(apellidos__icontains=q1), Q.OR)
            self.query.add(Q(ruc__icontains=q1), Q.OR)
            self.query.add(Q(codigo_unico_doctor__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).prefetch_related('especialidad')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:doctor_create')
        return context


class DoctorCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    fields = ['nombres', 'apellidos', 'ruc', 'fecha_nacimiento', 'direccion', 
              'codigo_unico_doctor', 'especialidad', 'telefonos', 'email', 
              'horario_atencion', 'duracion_atencion', 'foto', 'activo']
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'add_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context


class DoctorUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    fields = ['nombres', 'apellidos', 'ruc', 'fecha_nacimiento', 'direccion', 
              'codigo_unico_doctor', 'especialidad', 'telefonos', 'email', 
              'horario_atencion', 'duracion_atencion', 'foto', 'activo']
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'change_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context


class DoctorDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Doctor
    template_name = 'core/doctor/delete.html'
    success_url = reverse_lazy('core:doctor_list')
    permission_required = 'delete_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar el doctor: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context
