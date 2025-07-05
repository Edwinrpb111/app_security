from django import forms
from applications.core.models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'nombres', 'apellidos', 'ruc', 'fecha_nacimiento', 'direccion',
            'codigo_unico_doctor', 'especialidad', 'telefonos', 'email',
            'horario_atencion', 'duracion_atencion', 'foto', 'activo'
        ]
        widgets = {
            'especialidad': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }