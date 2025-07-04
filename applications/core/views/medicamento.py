from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Medicamento
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class MedicamentoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/medicamento/list.html'
    model = Medicamento
    context_object_name = 'medicamentos'
    permission_required = 'view_medicamento'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
            self.query.add(Q(tipo__nombre__icontains=q1), Q.OR)
            self.query.add(Q(marca_medicamento__nombre__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('tipo', 'marca_medicamento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:medicamento_create')
        return context


class MedicamentoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    fields = ['tipo', 'marca_medicamento', 'nombre', 'descripcion', 'concentracion', 
              'via_administracion', 'cantidad', 'precio', 'comercial', 'foto', 'activo']
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'add_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Medicamento'
        context['back_url'] = self.success_url
        return context


class MedicamentoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    fields = ['tipo', 'marca_medicamento', 'nombre', 'descripcion', 'concentracion', 
              'via_administracion', 'cantidad', 'precio', 'comercial', 'foto', 'activo']
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'change_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        return context


class MedicamentoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    template_name = 'core/medicamento/delete.html'
    success_url = reverse_lazy('core:medicamento_list')
    permission_required = 'delete_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Medicamento'
        context['description'] = f"¿Desea eliminar el medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context
