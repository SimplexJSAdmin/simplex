from django.urls import path
from . import views

urlpatterns = [
    path('home', views.inicio, name='inicio'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('reportes', views.obtener_reportes_opciones, name='home_reportes'),
    path('reportes/resultado', views.obtener_reportes_final, name='reportes_result'),
    path('preprocesamiento', views.preprocesamiento_home, name='preprocesamiento'),
    path('preprocesamiento/result', views.preprocesamiento_result, name='preprocesamiento_result'),
    path('liquidaciones', views.liquidaciones_home, name='liquidaciones'),
    path('parametros', views.parametros_home, name='parametros'),
    path('parametros/<str:parameter_type>', views.parametros_list, name='parametros_list'),
    path('conceptos', views.conceptos_home, name='conceptos'),
    path('conceptos-internos', views.conceptos_internos_home, name='conceptos_internos_home'),
    path('conceptos-internos/crear', views.conceptos_internos_crear, name='conceptos_internos_crear'),
    path('informes', views.informes_home, name='informes'),
    path('logs', views.logs_home, name='logs'),
    path('empresas', views.empresas_home, name='empresas'),
    path('empresas/crear', views.empresas_crear, name='empresa_crear')
]
