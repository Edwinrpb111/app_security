from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Empleado
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from applications.core.forms.empleado import EmpleadoForm


class EmpleadoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/empleado/list.html'
    model = Empleado
    context_object_name = 'empleados'
    permission_required = 'view_empleado'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        query = Q()
        if q1:
            query |= Q(nombres__icontains=q1)
            query |= Q(apellidos__icontains=q1)
            query |= Q(cedula_ecuatoriana__icontains=q1)
            query |= Q(cargo__nombre__icontains=q1)
        from applications.core.models import Empleado
        return Empleado.objects.filter(query).select_related('cargo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:empleado_create')
        return context


class EmpleadoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'add_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context


class EmpleadoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'change_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context


class EmpleadoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    template_name = 'core/empleado/delete.html'
    success_url = reverse_lazy('core:empleado_list')
    permission_required = 'delete_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar el empleado: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context
