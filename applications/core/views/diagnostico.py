from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Diagnostico
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class DiagnosticoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/diagnostico/list.html'
    model = Diagnostico
    context_object_name = 'diagnosticos'
    permission_required = 'view_diagnostico'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(codigo__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
            self.query.add(Q(datos_adicionales__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:diagnostico_create')
        return context


class DiagnosticoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    fields = ['codigo', 'descripcion', 'datos_adicionales', 'activo']
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'add_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Diagnóstico'
        context['back_url'] = self.success_url
        return context


class DiagnosticoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    fields = ['codigo', 'descripcion', 'datos_adicionales', 'activo']
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'change_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Diagnóstico'
        context['back_url'] = self.success_url
        return context


class DiagnosticoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    template_name = 'core/diagnostico/delete.html'
    success_url = reverse_lazy('core:diagnostico_list')
    permission_required = 'delete_diagnostico'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Diagnóstico'
        context['description'] = f"¿Desea eliminar el diagnóstico: {self.object.codigo} - {self.object.descripcion}?"
        context['back_url'] = self.success_url
        return context
