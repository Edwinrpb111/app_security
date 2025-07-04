from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.doctor.models import ServiciosAdicionales
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class ServiciosAdicionalesListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/servicios_adicionales/list.html'
    model = ServiciosAdicionales
    context_object_name = 'servicios_adicionales'
    permission_required = 'view_serviciosadicionales'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre_servicio__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:servicios_adicionales_create')
        return context


class ServiciosAdicionalesCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/form.html'
    fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'add_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Servicio Adicional'
        context['back_url'] = self.success_url
        return context


class ServiciosAdicionalesUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/form.html'
    fields = ['nombre_servicio', 'costo_servicio', 'descripcion', 'activo']
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'change_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Servicio Adicional'
        context['back_url'] = self.success_url
        return context


class ServiciosAdicionalesDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = ServiciosAdicionales
    template_name = 'doctor/servicios_adicionales/delete.html'
    success_url = reverse_lazy('doctor:servicios_adicionales_list')
    permission_required = 'delete_serviciosadicionales'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Servicio Adicional'
        context['description'] = f"¿Desea eliminar el servicio: {self.object.nombre_servicio}?"
        context['back_url'] = self.success_url
        return context
