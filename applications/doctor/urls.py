from django.urls import path

from applications.doctor.views.atencion_medica import AtencionListView, AtencionCreateView, AtencionUpdateView, AtencionDeleteView
from applications.doctor.views.cita_medica import CitaMedicaListView, CitaMedicaCreateView, CitaMedicaUpdateView, CitaMedicaDeleteView
from applications.doctor.views.horario_atencion import HorarioAtencionListView, HorarioAtencionCreateView, HorarioAtencionUpdateView, HorarioAtencionDeleteView
from applications.doctor.views.servicios_adicionales import ServiciosAdicionalesListView, ServiciosAdicionalesCreateView, ServiciosAdicionalesUpdateView, ServiciosAdicionalesDeleteView
from applications.doctor.views.pago import PagoListView, PagoCreateView, PagoUpdateView, PagoDeleteView
#from applications.doctor.views.facturacion_medica import FacturacionMedicaListView, FacturacionMedicaCreateView, FacturacionMedicaUpdateView, FacturacionMedicaDeleteView

app_name='doctor' # define un espacio de nombre para la aplicacion
urlpatterns = [
    # Rutas  para vistas relacionadas con Doctor
    path('atencion_list/', AtencionListView.as_view(), name="atencion_list"),
    path('atencion_create/', AtencionCreateView.as_view(), name="atencion_create"),
    path('atencion_update/<int:pk>/', AtencionUpdateView.as_view(), name="atencion_update"),
    path('atencion_delete/<int:pk>/', AtencionDeleteView.as_view(), name="atencion_delete"),

    # Citas Médicas
    path('cita-medica/', CitaMedicaListView.as_view(), name='cita_medica_list'),
    path('cita-medica/create/', CitaMedicaCreateView.as_view(), name='cita_medica_create'),
    path('cita-medica/update/<int:pk>/', CitaMedicaUpdateView.as_view(), name='cita_medica_update'),
    path('cita-medica/delete/<int:pk>/', CitaMedicaDeleteView.as_view(), name='cita_medica_delete'),
    
    # Horarios de Atención
    path('horario-atencion/', HorarioAtencionListView.as_view(), name='horario_atencion_list'),
    path('horario-atencion/create/', HorarioAtencionCreateView.as_view(), name='horario_atencion_create'),
    path('horario-atencion/update/<int:pk>/', HorarioAtencionUpdateView.as_view(), name='horario_atencion_update'),
    path('horario-atencion/delete/<int:pk>/', HorarioAtencionDeleteView.as_view(), name='horario_atencion_delete'),
    
    # Servicios Adicionales
    path('servicios-adicionales/', ServiciosAdicionalesListView.as_view(), name='servicios_adicionales_list'),
    path('servicios-adicionales/create/', ServiciosAdicionalesCreateView.as_view(), name='servicios_adicionales_create'),
    path('servicios-adicionales/update/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(), name='servicios_adicionales_update'),
    path('servicios-adicionales/delete/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(), name='servicios_adicionales_delete'),
    
    # Pagos
    path('pago/', PagoListView.as_view(), name='pago_list'),
    path('pago/create/', PagoCreateView.as_view(), name='pago_create'),
    path('pago/update/<int:pk>/', PagoUpdateView.as_view(), name='pago_update'),
    path('pago/delete/<int:pk>/', PagoDeleteView.as_view(), name='pago_delete'),
    
    
    # Facturación Médica  ver si se hace detalle pago 
    #path('facturacion-medica/', FacturacionMedicaListView.as_view(), name='facturacion_medica_list'),
    #path('facturacion-medica/create/', FacturacionMedicaCreateView.as_view(), name='facturacion_medica_create'),
    #path('facturacion-medica/update/<int:pk>/', FacturacionMedicaUpdateView.as_view(), name='facturacion_medica_update'),
    #path('facturacion-medica/delete/<int:pk>/', FacturacionMedicaDeleteView.as_view(), name='facturacion_medica_delete'),
    
]