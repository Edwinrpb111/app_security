from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from applications.doctor.models import Pago
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin


class PagoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/pago/list.html'
    model = Pago
    context_object_name = 'pagos'
    permission_required = 'view_pago'

    def get_queryset(self):
        q1 = self.request.GET.get('q')
        if q1 is not None:
            self.query.add(Q(atencion__paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(atencion__paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(metodo_pago__icontains=q1), Q.OR)
            self.query.add(Q(estado__icontains=q1), Q.OR)
            self.query.add(Q(nombre_pagador__icontains=q1), Q.OR)
        return self.model.objects.filter(self.query).select_related('atencion__paciente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:pago_create')
        return context


class PagoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    fields = ['atencion', 'metodo_pago', 'monto_total', 'estado', 'nombre_pagador', 
              'referencia_externa', 'evidencia_pago', 'observaciones', 'activo']
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Pago'
        context['back_url'] = self.success_url
        return context


class PagoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    fields = ['atencion', 'metodo_pago', 'monto_total', 'estado', 'nombre_pagador', 
              'referencia_externa', 'evidencia_pago', 'observaciones', 'activo']
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'change_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Pago'
        context['back_url'] = self.success_url
        return context


class PagoDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = Pago
    template_name = 'doctor/pago/delete.html'
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'delete_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Pago'
        context['description'] = f"¿Desea eliminar el pago: ${self.object.monto_total} - {self.object.metodo_pago}?"
        context['back_url'] = self.success_url
        return context
