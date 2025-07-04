from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import GastoMensual
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class GastoMensualListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/gasto_mensual/list.html'
    model = GastoMensual
    context_object_name = 'gastos_mensual'
    permission_required = 'view_gastomensual'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(tipo_gasto__nombre__icontains=q1), Q.OR)
            self.query.add(Q(observacion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('tipo_gasto')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:gasto_mensual_create')
        return context


class GastoMensualCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/form.html'
    fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'add_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Gasto Mensual'
        context['back_url'] = self.success_url
        return context


class GastoMensualUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/form.html'
    fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'change_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Gasto Mensual'
        context['back_url'] = self.success_url
        return context


class GastoMensualDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = GastoMensual
    template_name = 'core/gasto_mensual/delete.html'
    success_url = reverse_lazy('core:gasto_mensual_list')
    permission_required = 'delete_gastomensual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Gasto Mensual'
        context['description'] = f"¿Desea eliminar el gasto: {self.object.tipo_gasto} - ${self.object.valor}?"
        context['back_url'] = self.success_url
        return context
