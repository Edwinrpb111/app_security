from django import forms
from applications.core.models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'apellidos': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'cedula_ecuatoriana': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'dni': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'telefono': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'sexo': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'estado_civil': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'direccion': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'latitud': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': 'any'}),
            'longitud': forms.NumberInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'step': 'any'}),
            'tipo_sangre': forms.Select(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'antecedentes_personales': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'antecedentes_quirurgicos': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'antecedentes_familiares': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'alergias': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'medicamentos_actuales': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'habitos_toxicos': forms.TextInput(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500'}),
            'vacunas': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'antecedentes_gineco_obstetricos': forms.Textarea(attrs={'class': 'block w-full rounded-xl border-slate-300 focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500', 'rows': 2}),
            'activo': forms.CheckboxInput(attrs={'class': 'rounded border-slate-300 text-emerald-600 focus:ring-emerald-500'}),
        }
