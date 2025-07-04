from django.urls import path
from applications.core.views.paciente import paciente_find, PacienteListView, PacienteCreateView, PacienteUpdateView, PacienteDeleteView
from applications.core.views.tipo_sangre import TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView
from applications.core.views.especialidad import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView
from applications.core.views.doctor import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView
from applications.core.views.medicamento import MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView
from applications.core.views.diagnostico import DiagnosticoListView, DiagnosticoCreateView, DiagnosticoUpdateView, DiagnosticoDeleteView
from applications.core.views.cargo import CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView
from applications.core.views.empleado import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView
from applications.core.views.tipo_medicamento import TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView
from applications.core.views.marca_medicamento import MarcaMedicamentoListView, MarcaMedicamentoCreateView, MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView
from applications.core.views.tipo_gasto import TipoGastoListView, TipoGastoCreateView, TipoGastoUpdateView, TipoGastoDeleteView
from applications.core.views.gasto_mensual import GastoMensualListView, GastoMensualCreateView, GastoMensualUpdateView, GastoMensualDeleteView


app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Pacientes
    #Paciente Main View Create, Update, Delete, List
    path('paciente_find/', paciente_find, name="paciente_find"),
    path('paciente/', PacienteListView.as_view(), name='paciente_list'),
    path('paciente/create/', PacienteCreateView.as_view(), name='paciente_create'),
    path('paciente/update/<int:pk>/', PacienteUpdateView.as_view(), name='paciente_update'),
    path('paciente/delete/<int:pk>/', PacienteDeleteView.as_view(), name='paciente_delete'),
    # Tipo Sangre
    path('tipo-sangre/', TipoSangreListView.as_view(), name='tipo_sangre_list'),
    path('tipo-sangre/create/', TipoSangreCreateView.as_view(), name='tipo_sangre_create'),
    path('tipo-sangre/update/<int:pk>/', TipoSangreUpdateView.as_view(), name='tipo_sangre_update'),
    path('tipo-sangre/delete/<int:pk>/', TipoSangreDeleteView.as_view(), name='tipo_sangre_delete'),
    
    # Especialidad
    path('especialidad/', EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidad/create/', EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidad/update/<int:pk>/', EspecialidadUpdateView.as_view(), name='especialidad_update'),
    path('especialidad/delete/<int:pk>/', EspecialidadDeleteView.as_view(), name='especialidad_delete'),
    
    # Doctor Revisar View Main
    path('doctor/', DoctorListView.as_view(), name='doctor_list'),
    path('doctor/create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('doctor/update/<int:pk>/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctor/delete/<int:pk>/', DoctorDeleteView.as_view(), name='doctor_delete'),
    
    # Medicamento revisar View que hay que integrar tipos de miedicamentos y marcas de medicamentos 22% chat
    path('medicamento/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamento/create/', MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamento/update/<int:pk>/', MedicamentoUpdateView.as_view(), name='medicamento_update'),
    path('medicamento/delete/<int:pk>/', MedicamentoDeleteView.as_view(), name='medicamento_delete'),
    
    # Diagnostico
    path('diagnostico/', DiagnosticoListView.as_view(), name='diagnostico_list'),
    path('diagnostico/create/', DiagnosticoCreateView.as_view(), name='diagnostico_create'),
    path('diagnostico/update/<int:pk>/', DiagnosticoUpdateView.as_view(), name='diagnostico_update'),
    path('diagnostico/delete/<int:pk>/', DiagnosticoDeleteView.as_view(), name='diagnostico_delete'),
    
    # Cargo
    path('cargo/', CargoListView.as_view(), name='cargo_list'),
    path('cargo/create/', CargoCreateView.as_view(), name='cargo_create'),
    path('cargo/update/<int:pk>/', CargoUpdateView.as_view(), name='cargo_update'),
    path('cargo/delete/<int:pk>/', CargoDeleteView.as_view(), name='cargo_delete'),
    
    # Empleado Main
    path('empleado/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/create/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),
    
    # Tipo Medicamento Main
    path('tipo-medicamento/', TipoMedicamentoListView.as_view(), name='tipo_medicamento_list'),
    path('tipo-medicamento/create/', TipoMedicamentoCreateView.as_view(), name='tipo_medicamento_create'),
    path('tipo-medicamento/update/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name='tipo_medicamento_update'),
    path('tipo-medicamento/delete/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name='tipo_medicamento_delete'),
    
    # Marca Medicamento
    path('marca-medicamento/', MarcaMedicamentoListView.as_view(), name='marca_medicamento_list'),
    path('marca-medicamento/create/', MarcaMedicamentoCreateView.as_view(), name='marca_medicamento_create'),
    path('marca-medicamento/update/<int:pk>/', MarcaMedicamentoUpdateView.as_view(), name='marca_medicamento_update'),
    path('marca-medicamento/delete/<int:pk>/', MarcaMedicamentoDeleteView.as_view(), name='marca_medicamento_delete'),
    
    # Tipo Gasto
    path('tipo-gasto/', TipoGastoListView.as_view(), name='tipo_gasto_list'),
    path('tipo-gasto/create/', TipoGastoCreateView.as_view(), name='tipo_gasto_create'),
    path('tipo-gasto/update/<int:pk>/', TipoGastoUpdateView.as_view(), name='tipo_gasto_update'),
    path('tipo-gasto/delete/<int:pk>/', TipoGastoDeleteView.as_view(), name='tipo_gasto_delete'),
    
    # Gasto Mensual Main 
    path('gasto-mensual/', GastoMensualListView.as_view(), name='gasto_mensual_list'),
    path('gasto-mensual/create/', GastoMensualCreateView.as_view(), name='gasto_mensual_create'),
    path('gasto-mensual/update/<int:pk>/', GastoMensualUpdateView.as_view(), name='gasto_mensual_update'),
    path('gasto-mensual/delete/<int:pk>/', GastoMensualDeleteView.as_view(), name='gasto_mensual_delete'),

]