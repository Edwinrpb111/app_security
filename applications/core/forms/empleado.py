from django import forms
from applications.core.models import Empleado

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombres', 'apellidos', 'cedula_ecuatoriana', 'dni', 'fecha_nacimiento', 'cargo', 'sueldo', 'fecha_ingreso', 'direccion', 'foto', 'activo']
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'apellidos': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'cedula_ecuatoriana': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'dni': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'cargo': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'sueldo': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500', 'step': '0.01', 'min': '0'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'direccion': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500'}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded border-slate-300 text-indigo-600 focus:ring-indigo-500'}),
        }
