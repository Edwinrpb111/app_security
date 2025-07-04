'''
import json
from decimal import Decimal

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone

from applications.core.models import Paciente
from applications.doctor.forms.facturacion_medica import FacturacionMedicaForm
from applications.doctor.models import FacturacionMedica, Pago, DetallePago, ServiciosAdicionales, Atencion
from applications.security.components.mixin_crud import CreateViewMixin, DeleteViewMixin, ListViewMixin, \
    PermissionMixin, UpdateViewMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from proy_clinico.util import save_audit


class FacturacionMedicaListView(PermissionMixin, ListViewMixin, ListView):
    template_name = 'doctor/facturacion_medica/list.html'
    model = FacturacionMedica
    context_object_name = 'facturaciones'
    permission_required = 'view_facturacionmedica'

    def get_queryset(self):
        q1 = self.request.GET.get('q')

        if q1 is not None:
            self.query.add(Q(numero_factura__icontains=q1), Q.OR)
            self.query.add(Q(pago__atencion__paciente__nombres__icontains=q1), Q.OR)
            self.query.add(Q(pago__atencion__paciente__apellidos__icontains=q1), Q.OR)
            self.query.add(Q(pago__nombre_pagador__icontains=q1), Q.OR)
        
        return FacturacionMedica.objects.select_related(
            'pago__atencion__paciente'
        ).filter(self.query).order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('doctor:facturacion_medica_create')
        return context


class FacturacionMedicaCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = FacturacionMedica
    template_name = 'doctor/facturacion_medica/form.html'
    form_class = FacturacionMedicaForm
    success_url = reverse_lazy('doctor:facturacion_medica_list')
    permission_required = 'add_facturacionmedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Crear Facturación'
        context['back_url'] = self.success_url
        context['atenciones'] = Atencion.objects.select_related('paciente').filter(
            paciente__activo=True
        ).order_by('-fecha_atencion')[:50]
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True).order_by('nombre_servicio')
        context['pacientes'] = Paciente.objects.filter(activo=True).order_by('nombres', 'apellidos')
        
        context['servicios_json'] = json.dumps([
            {
                'id': servicio.id,
                'nombre': servicio.nombre_servicio,
                'costo': float(servicio.costo_servicio),
                'descripcion': servicio.descripcion or ''
            }
            for servicio in context['servicios']
        ])
        
        context['modo_edicion'] = False
        return context

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        
        pago_data = data.get('pago', {})
        servicios_data = data.get('servicios', [])
        facturacion_data = data.get('facturacion', {})

        def to_int(value):
            return int(value) if value is not None and value != '' else None

        def to_decimal(value):
            return Decimal(str(value)) if value is not None and value != '' else None

        try:
            with transaction.atomic():
                pago = Pago.objects.create(
                    atencion_id=to_int(pago_data.get('atencion')) if pago_data.get('atencion') else None,
                    metodo_pago=pago_data.get('metodo_pago'),
                    monto_total=Decimal('0'),
                    estado='pendiente',
                    nombre_pagador=pago_data.get('nombre_pagador'),
                    referencia_externa=pago_data.get('referencia_externa'),
                    observaciones=pago_data.get('observaciones'),
                    fecha_creacion=timezone.now()
                )

                total_facturacion = Decimal('0')

                for servicio_data in servicios_data:
                    detalle = DetallePago.objects.create(
                        pago=pago,
                        servicio_adicional_id=to_int(servicio_data.get('servicio_id')),
                        cantidad=to_int(servicio_data.get('cantidad', 1)),
                        precio_unitario=to_decimal(servicio_data.get('precio_unitario')),
                        descuento_porcentaje=to_decimal(servicio_data.get('descuento_porcentaje', 0)),
                        aplica_seguro=bool(servicio_data.get('aplica_seguro', False)),
                        valor_seguro=to_decimal(servicio_data.get('valor_seguro')) if servicio_data.get('valor_seguro') else None,
                        descripcion_seguro=servicio_data.get('descripcion_seguro')
                    )
                    total_facturacion += detalle.subtotal

                pago.monto_total = total_facturacion
                pago.save()

                facturacion = FacturacionMedica.objects.create(
                    pago=pago,
                    observaciones_facturacion=facturacion_data.get('observaciones_facturacion')
                )

                save_audit(request, facturacion, "ADICION")

                messages.success(request, f"Facturación #{facturacion.numero_factura} creada exitosamente")

                return JsonResponse({
                    "msg": "Facturación médica registrada exitosamente",
                    "id": facturacion.id,
                    "numero_factura": facturacion.numero_factura,
                    "monto_total": float(pago.monto_total)
                }, status=200)

        except Exception as e:
            messages.error(request, f"Error al crear la facturación médica")
            return JsonResponse({
                "msg": f"Error al crear la facturación médica: {str(e)}"
            }, status=500)


class FacturacionMedicaUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
    model = FacturacionMedica
    template_name = 'doctor/facturacion_medica/form.html'
    form_class = FacturacionMedicaForm
    success_url = reverse_lazy('doctor:facturacion_medica_list')
    permission_required = 'change_facturacionmedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Facturación'
        context['back_url'] = self.success_url

        facturacion = self.get_object()
        pago = facturacion.pago

        context['atenciones'] = Atencion.objects.select_related('paciente').filter(
            paciente__activo=True
        ).order_by('-fecha_atencion')[:50]
        context['servicios'] = ServiciosAdicionales.objects.filter(activo=True).order_by('nombre_servicio')
        context['pacientes'] = Paciente.objects.filter(activo=True).order_by('nombres', 'apellidos')
        
        context['servicios_json'] = json.dumps([
            {
                'id': servicio.id,
                'nombre': servicio.nombre_servicio,
                'costo': float(servicio.costo_servicio),
                'descripcion': servicio.descripcion or ''
            }
            for servicio in context['servicios']
        ])

        context['facturacion'] = facturacion
        context['pago'] = pago

        servicios_actuales = []
        for detalle in pago.detalles.select_related('servicio_adicional').all():
            servicio_dict = {
                'servicio_id': detalle.servicio_adicional.id,
                'nombre_servicio': detalle.servicio_adicional.nombre_servicio,
                'cantidad': detalle.cantidad,
                'precio_unitario': float(detalle.precio_unitario),
                'descuento_porcentaje': float(detalle.descuento_porcentaje),
                'aplica_seguro': detalle.aplica_seguro,
                'valor_seguro': float(detalle.valor_seguro) if detalle.valor_seguro else None,
                'descripcion_seguro': detalle.descripcion_seguro,
                'subtotal': float(detalle.subtotal)
            }
            servicios_actuales.append(servicio_dict)

        context['servicios_actuales_json'] = json.dumps(servicios_actuales)
        context['modo_edicion'] = True

        return context

    def post(self, request, *args, **kwargs):
        facturacion = self.get_object()
        pago = facturacion.pago
        
        data = json.loads(request.body)
        
        pago_data = data.get('pago', {})
        servicios_data = data.get('servicios', [])
        facturacion_data = data.get('facturacion', {})

        def to_int(value):
            return int(value) if value is not None and value != '' else None

        def to_decimal(value):
            return Decimal(str(value)) if value is not None and value != '' else None

        try:
            with transaction.atomic():
                pago.atencion_id = to_int(pago_data.get('atencion')) if pago_data.get('atencion') else None
                pago.metodo_pago = pago_data.get('metodo_pago')
                pago.nombre_pagador = pago_data.get('nombre_pagador')
                pago.referencia_externa = pago_data.get('referencia_externa')
                pago.observaciones = pago_data.get('observaciones')

                DetallePago.objects.filter(pago=pago).delete()

                total_facturacion = Decimal('0')

                for servicio_data in servicios_data:
                    detalle = DetallePago.objects.create(
                        pago=pago,
                        servicio_adicional_id=to_int(servicio_data.get('servicio_id')),
                        cantidad=to_int(servicio_data.get('cantidad', 1)),
                        precio_unitario=to_decimal(servicio_data.get('precio_unitario')),
                        descuento_porcentaje=to_decimal(servicio_data.get('descuento_porcentaje', 0)),
                        aplica_seguro=bool(servicio_data.get('aplica_seguro', False)),
                        valor_seguro=to_decimal(servicio_data.get('valor_seguro')) if servicio_data.get('valor_seguro') else None,
                        descripcion_seguro=servicio_data.get('descripcion_seguro')
                    )
                    total_facturacion += detalle.subtotal

                pago.monto_total = total_facturacion
                pago.save()

                facturacion.observaciones_facturacion = facturacion_data.get('observaciones_facturacion')
                facturacion.save()

                save_audit(request, facturacion, "MODIFICACION")

                messages.success(request, f"Facturación #{facturacion.numero_factura} actualizada exitosamente")

                return JsonResponse({
                    "msg": "Facturación médica actualizada exitosamente",
                    "id": facturacion.id,
                    "numero_factura": facturacion.numero_factura,
                    "monto_total": float(pago.monto_total)
                }, status=200)

        except Exception as e:
            messages.error(request, f"Error al actualizar la facturación médica")
            return JsonResponse({
                "msg": f"Error al actualizar la facturación médica: {str(e)}"
            }, status=500)


class FacturacionMedicaDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
    model = FacturacionMedica
    template_name = 'core/delete.html'
    success_url = reverse_lazy('doctor:facturacion_medica_list')
    permission_required = 'delete_facturacionmedica'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Facturación'
        context['description'] = f"¿Desea eliminar la facturación: {self.object.numero_factura}?"
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        numero_factura = self.object.numero_factura
        response = super().form_valid(form)
        messages.success(self.request, f"Facturación {numero_factura} eliminada exitosamente.")
        return response
'''