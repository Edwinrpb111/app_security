from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import TipoGasto
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class TipoGastoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/tipo_gasto/list.html'
    model = TipoGasto
    context_object_name = 'tipos_gasto'
    permission_required = 'view_tipogasto'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:tipo_gasto_create')
        return context


class TipoGastoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'add_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Tipo de Gasto'
        context['back_url'] = self.success_url
        return context


class TipoGastoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'change_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Tipo de Gasto'
        context['back_url'] = self.success_url
        return context


class TipoGastoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = TipoGasto
    template_name = 'core/tipo_gasto/delete.html'
    success_url = reverse_lazy('core:tipo_gasto_list')
    permission_required = 'delete_tipogasto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Tipo de Gasto'
        context['description'] = f"¿Desea eliminar el tipo de gasto: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context
