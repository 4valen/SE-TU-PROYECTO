from django.urls import path
from . import views
from .views import generacion_view

urlpatterns = [
    path('index', views.index, name='index'),
    path('', views.index, name='index'),
    path('layout/', views.layout, name='layout'),
    path('categoria',views.categoria, name='categoria'),
    path('consejos',views.consejos, name='consejos'),
    path('generacion',views.generacion, name='generacion'),
    path('login',views.login, name='login'),
    path('Registro',views.Registro, name='Registro'),
    path('lista',views.lista, name='lista'),
    path('lista/<str:pk>/<str:action>/', views.lista, name='lista_action'),
    path('generacion/', generacion_view, name='generacion'),
    path('vida_saludable_form/', views.vida_saludable_form, name='vida_saludable_form'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.success_view, name='success'),  
    path('dashboard/', views.index, name='dashboard'),
    path('admin-vista/', views.admin_vista, name='admin_vista'),
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('cambiar-estado/<int:user_id>/', views.cambiar_estado_usuario, name='cambiar_estado'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
]
    