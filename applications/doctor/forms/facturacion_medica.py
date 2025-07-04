from django import forms
from django.forms import ModelForm
from applications.doctor.models import FacturacionMedica, Pago, DetallePago, ServiciosAdicionales
from applications.core.models import Paciente
from applications.doctor.utils.pago import MetodoPagoChoices, EstadoPagoChoices


class FacturacionMedicaForm(ModelForm):
    class Meta:
        model = FacturacionMedica
        fields = ['observaciones_facturacion']
        
        widgets = {
            'observaciones_facturacion': forms.Textarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Observaciones adicionales sobre la facturación...'
            }),
        }


class PagoFacturacionForm(ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion', 'metodo_pago', 'nombre_pagador', 
            'referencia_externa', 'evidencia_pago', 'observaciones'
        ]
        
        widgets = {
            'atencion': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'nombre_pagador': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Nombre de quien realiza el pago'
            }),
            'referencia_externa': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'ID de transacción o referencia'
            }),
            'evidencia_pago': forms.FileInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'accept': 'image/*'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-textarea w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'rows': 3,
                'placeholder': 'Observaciones del pago...'
            }),
        }


class DetallePagoForm(ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'servicio_adicional', 'cantidad', 'precio_unitario', 
            'descuento_porcentaje', 'aplica_seguro', 'valor_seguro', 'descripcion_seguro'
        ]
        
        widgets = {
            'servicio_adicional': forms.Select(attrs={
                'class': 'form-select w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'min': '1',
                'value': '1'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'step': '0.01',
                'min': '0'
            }),
            'descuento_porcentaje': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'value': '0'
            }),
            'aplica_seguro': forms.CheckboxInput(attrs={
                'class': 'form-checkbox rounded border-gray-300 text-blue-600 focus:ring focus:ring-blue-200'
            }),
            'valor_seguro': forms.NumberInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'step': '0.01',
                'min': '0'
            }),
            'descripcion_seguro': forms.TextInput(attrs={
                'class': 'form-input w-full rounded-lg border-gray-300 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: Saludsa Nivel 2'
            }),
        }
