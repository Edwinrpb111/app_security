from django import forms
from applications.doctor.models import Pago, DetallePago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'atencion', 'metodo_pago', 'monto_total', 'estado', 'fecha_pago', 'nombre_pagador',
            'referencia_externa', 'evidencia_pago', 'observaciones', 'activo'
        ]
        widgets = {
            'atencion': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'metodo_pago': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'monto_total': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': '0.01', 'min': '0'}),
            'estado': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'fecha_pago': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'nombre_pagador': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'referencia_externa': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'evidencia_pago': forms.ClearableFileInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'observaciones': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded border-slate-300 text-emerald-600 focus:ring-emerald-500'}),
        }

class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'servicio_adicional', 'cantidad', 'precio_unitario', 'descuento_porcentaje',
            'aplica_seguro', 'valor_seguro', 'descripcion_seguro'
        ]
        widgets = {
            'servicio_adicional': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'cantidad': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': '0.01', 'min': '0'}),
            'descuento_porcentaje': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': '0.01', 'min': '0', 'max': '100'}),
            'aplica_seguro': forms.CheckboxInput(attrs={'class': 'rounded border-slate-300 text-emerald-600 focus:ring-emerald-500'}),
            'valor_seguro': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': '0.01', 'min': '0'}),
            'descripcion_seguro': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
        }
