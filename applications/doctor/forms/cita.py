
from django import forms
from applications.doctor.models import CitaMedica

class CitaMedicaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_input = 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 transition duration-150 ease-in-out'
        base_select = 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 transition duration-150 ease-in-out'
        base_textarea = 'block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 transition duration-150 ease-in-out'
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs['class'] = base_input
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = base_select
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = base_textarea
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = base_input
                field.widget.input_type = 'date'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = base_input
                field.widget.input_type = 'time'
            else:
                field.widget.attrs['class'] = base_input
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'doctor', 'fecha', 'hora_cita', 'estado', 'observaciones']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora_cita': forms.TimeInput(attrs={'type': 'time'}),
            'estado': forms.Select(),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].widget.format = '%Y-%m-%d'
