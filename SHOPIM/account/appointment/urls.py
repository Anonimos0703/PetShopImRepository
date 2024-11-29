# appointment/urls.py
from django.urls import path
from .views import appointment_view,admin_appointment_list,admin_appointment_update,admin_appointment_cancel

urlpatterns = [
    path('', appointment_view, name='appointment'),  
    path('admin/appointments/', admin_appointment_list, name='admin_appointment_list'),
    path('appointment/<int:appointment_id>/update/', admin_appointment_update, name='admin_appointment_update'),
    path('appointments/cancel/<int:appointment_id>/', admin_appointment_cancel, name='admin_appointment_cancel'),

]