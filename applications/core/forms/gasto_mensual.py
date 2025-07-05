from django import forms
from applications.core.models import GastoMensual

class GastoMensualForm(forms.ModelForm):
    class Meta:
        model = GastoMensual
        fields = ['tipo_gasto', 'fecha', 'valor', 'observacion']
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'valor': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500', 'step': '0.01', 'min': '0'}),
            'observacion': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500', 'rows': 2}),
        }
