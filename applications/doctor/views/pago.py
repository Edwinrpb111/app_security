from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import inlineformset_factory
from django.db.models import Q
from applications.doctor.models import Pago, DetallePago
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin

DetallePagoFormSet = inlineformset_factory(
    Pago, DetallePago,
    fields=['servicio_adicional', 'cantidad', 'precio_unitario', 'descuento_porcentaje', 'aplica_seguro', 'valor_seguro', 'descripcion_seguro'],
    extra=1, can_delete=True
)

class PagoListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/pago/list.html'
    model = Pago
    context_object_name = 'pagos'
    permission_required = 'view_pago'

    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        if q1:
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



from applications.doctor.forms.pago import PagoForm

class PagoCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'add_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['detalle_formset'] = DetallePagoFormSet(self.request.POST, self.request.FILES)
        else:
            context['detalle_formset'] = DetallePagoFormSet()
        context['grabar'] = 'Grabar Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if form.is_valid() and detalle_formset.is_valid():
            self.object = form.save()
            detalle_formset.instance = self.object
            detalle_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)



class PagoUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = Pago
    template_name = 'doctor/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('doctor:pago_list')
    permission_required = 'change_pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['detalle_formset'] = DetallePagoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['detalle_formset'] = DetallePagoFormSet(instance=self.object)
        context['grabar'] = 'Actualizar Pago'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if form.is_valid() and detalle_formset.is_valid():
            self.object = form.save()
            detalle_formset.instance = self.object
            detalle_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


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