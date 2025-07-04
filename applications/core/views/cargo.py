from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from applications.core.models import Cargo
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class CargoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'core/cargo/list.html'
    model = Cargo
    context_object_name = 'cargos'
    permission_required = 'view_cargo'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            self.query.add(Q(descripcion__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:cargo_create')
        return context


class CargoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'add_cargo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Cargo'
        context['back_url'] = self.success_url
        return context


class CargoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Cargo
    template_name = 'core/cargo/form.html'
    fields = ['nombre', 'descripcion', 'activo']
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'change_cargo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Cargo'
        context['back_url'] = self.success_url
        return context


class CargoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Cargo
    template_name = 'core/cargo/delete.html'
    success_url = reverse_lazy('core:cargo_list')
    permission_required = 'delete_cargo'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Cargo'
        context['description'] = f"¿Desea eliminar el cargo: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context
