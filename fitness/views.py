from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Datos, Genero
from .forms import VidaSaludableForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .avatars import generar_avatar_aleatorio, generar_avatar_para_usuario
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login ,logout
import python_avatars as pa
import base64


def perfil_usuario(request):
    avatar_svg = generar_avatar_para_usuario(request.user.username)
    
    return render(request, 'perfil.html', {'avatar_svg': avatar_svg})
# Agrega esta vista para cerrar sesión
@login_required
def logout_view(request):
    auth_logout(request)
    # messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')
def index(request):
    # Obtener el nombre completo del usuario si está autenticado
    nombre_completo = ""
    if request.user.is_authenticated:
        try:
            # Buscar los datos del usuario usando la relación
            datos_usuario = Datos.objects.get(user=request.user)
            nombre_completo = f"{datos_usuario.nombre} {datos_usuario.apellido_paterno}"
        except Datos.DoesNotExist:
            # Si no existe en Datos, usar el first_name del User
            nombre_completo = request.user.first_name or request.user.username
    
    context = {'nombre_completo': nombre_completo}
    return render(request, 'fitness/index.html', context)
@login_required
def layout(request):
    context = {}
    return render(request, 'fitness/layout.html', context)

@login_required(login_url="login")
def categoria(request):
    context = {}
    return render(request, 'fitness/categoria.html', context)
@login_required
def consejos(request):
    context = {}
    return render(request, 'fitness/consejos.html', context)
@login_required
def generacion(request):
    context = {}
    return render(request, 'fitness/generacion.html', context)

def generacion_view(request):
    if request.method == 'POST':
        fecha_nacimiento = request.POST.get('fechaNacimiento')
        if fecha_nacimiento:
            anio = int(fecha_nacimiento.split('-')[0])
            if 1946 <= anio <= 1964:
                generacion = "Baby Boomer"
            elif 1965 <= anio <= 1980:
                generacion = "Generación X"
            elif 1981 <= anio <= 1996:
                generacion = "Millennials"
            elif 1997 <= anio <= 2012:
                generacion = "Generación Z"
            else:
                generacion = "No definido"
            
            return JsonResponse({'generacion': generacion})
        else:
            return JsonResponse({'error': 'Fecha de nacimiento no proporcionada'}, status=400)
    return render(request, 'fitness/generacion.html')

def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Usuario recibido:", username)
        print("Contraseña recibida:", password)
        print("Intentando autenticar:", username, password)  # <- temporal
        #verificar al admin 
        if username == 'admin' and password == 'admin123':
            admin_user, created = User.objects.get_or_create(username='admin',defaults={'is_staff': True})
            if created:
                admin_user.set_password('admin123')
                admin_user.save()
                print("Usuario administrador creado.")
        #aum¿tenticamos al admin , al mero mero
            user = authenticate(request, username='admin', password='admin123')
            if user is not None:
                auth_login(request, user)
                messages.success(request, '¡Bienvenido Administrador Principal!')
                return redirect('admin_vista')
        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)
        print("Resultado de authenticate():", user)
        
        if user is not None:
            # Verificar que el usuario tenga un perfil Datos asociado
            try:
                datos_usuario = Datos.objects.get(user=user)
                if datos_usuario.activo == 1:  # Verificar que esté activo
                    auth_login(request, user)
                    messages.success(request, f'¡Bienvenido de nuevo, {datos_usuario.nombre}!')
                    return redirect('consejos')  # Redirigir a la página de consejos después del login
                else:
                    messages.warning(request, 'Tu cuenta está desactivada.')
            except Datos.DoesNotExist:
                messages.error(request, 'No tienes un perfil completo. Contacta al administrador.')
        else:
            messages.error(request, 'Credenciales inválidas. Verifica tu usuario y contraseña.')
    
    return render(request, 'fitness/login.html')
def Registro(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            rut = request.POST.get('rut')
            nombre = request.POST.get('nombre')
            apellido_paterno = request.POST.get('apellido_paterno')
            apellido_materno = request.POST.get('apellido_materno')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            id_genero = request.POST.get('id_genero')
            telefono = request.POST.get('telefono')
            peso = request.POST.get('peso')
            email = request.POST.get('email')
            direccion = request.POST.get('direccion')
            username = request.POST.get('username')
            password = request.POST.get('password')
            perfil = request.POST.get('perfil')

             # VALIDACIÓN: No permitir registro como 'admin'
            if username.lower() == 'admin':
                messages.error(request, 'Este nombre de usuario no está disponible.')
                generos = Genero.objects.all()
                context = {'generos': generos}
                return render(request, 'fitness/Registro.html', context)

            # Validar que se haya seleccionado un perfil
            if not perfil:
                messages.error(request, 'Debe seleccionar un perfil.')
                generos = Genero.objects.all()
                context = {'generos': generos}
                return render(request, 'fitness/Registro.html', context)

            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya existe.')
                return redirect('Registro')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'El email ya está registrado.')
                return redirect('Registro')

            # Crear usuario de Django
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=nombre,
                last_name=f"{apellido_paterno} {apellido_materno}"
            )

            # Crear registro en el modelo Datos con la relación al User
            datos = Datos(
                rut=rut,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                fecha_nacimiento=fecha_nacimiento,
                id_genero_id=id_genero,
                telefono=telefono,
                peso=peso,
                email=email,
                direccion=direccion,
                perfil=perfil,
                activo=1,
                user=user  # Relacionar con el usuario creado
            )
            datos.save()

            # Iniciar sesión automáticamente
            auth_login(request, user)

            messages.success(request, f'¡Registro exitoso! Has sido registrado como {perfil.capitalize()}.')
            return redirect('index')

        except Exception as e:
            messages.error(request, f'Error en el registro: {str(e)}')
            return redirect('Registro')

    # Si es GET, mostrar el formulario
    generos = Genero.objects.all()
    context = {'generos': generos}
    return render(request, 'fitness/Registro.html', context)
# VISTAS DE ADMINISTRACIÓN
@login_required
def admin_vista(request):
    """Panel de administración"""
    if not (request.user.username == 'admin' and request.user.check_password('admin123')):
        messages.error(request, 'Acceso denegado. Solo para administrador principal.')
        return redirect('consejos')
    
    # Estadísticas
    total_usuarios = User.objects.count()
    total_datos = Datos.objects.count()
    usuarios_activos = Datos.objects.filter(activo=1).count()
    usuarios_inactivos = Datos.objects.filter(activo=0).count()
    
    # Usuarios recientes (últimos 5)
    usuarios_recientes = User.objects.all().order_by('-date_joined')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_datos': total_datos,
        'usuarios_activos': usuarios_activos,
        'usuarios_inactivos': usuarios_inactivos,
        'usuarios_recientes': usuarios_recientes,
    }
    return render(request, 'fitness/admin_vista.html', context)
@login_required
def gestion_usuarios(request):
    # SOLO el admin principal puede acceder
    if not (request.user.username == 'admin' and request.user.check_password('admin123')):
        messages.error(request, 'Acceso denegado.')
        return redirect('consejos')
    
    usuarios = User.objects.all().select_related('datos')
    return render(request, 'fitness/gestion_usuarios.html', {'usuarios': usuarios})

@login_required
def cambiar_estado_usuario(request, user_id):
    if not (request.user.username == 'admin' and request.user.check_password('admin123')):
        messages.error(request, 'Acceso denegado.')
        return redirect('consejos')
    
    usuario = get_object_or_404(User, id=user_id)
    
    # No permitir modificar al admin principal
    if usuario.username == 'admin':
        messages.error(request, 'No se puede modificar el administrador principal')
        return redirect('gestion_usuarios')
    
    try:
        datos_usuario = Datos.objects.get(user=usuario)
        # Cambiar estado (activo/inactivo)
        datos_usuario.activo = 0 if datos_usuario.activo == 1 else 1
        datos_usuario.save()
        
        estado = "activado" if datos_usuario.activo == 1 else "desactivado"
        messages.success(request, f'Usuario {usuario.username} {estado} correctamente')
    
    except Datos.DoesNotExist:
        messages.error(request, f'El usuario {usuario.username} no tiene perfil completo')
    
    return redirect('gestion_usuarios')

@login_required
def eliminar_usuario(request, user_id):
    if not (request.user.username == 'admin' and request.user.check_password('admin123')):
        messages.error(request, 'Acceso denegado.')
        return redirect('consejos')
    
    usuario = get_object_or_404(User, id=user_id)
    
    # No permitir eliminar al admin principal
    if usuario.username == 'admin':
        messages.error(request, 'No se puede eliminar el administrador principal')
        return redirect('gestion_usuarios')
    
    username = usuario.username
    usuario.delete()
    messages.success(request, f'Usuario {username} eliminado correctamente')
    
    return redirect('gestion_usuarios')
def vida_saludable_form(request):
    if request.method == 'POST':
        form = VidaSaludableForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.fecha_nacimiento = request.POST.get('fecha_nacimiento')
            instance.save()
            return redirect('success')
    else:
        form = VidaSaludableForm()
    return render(request, 'fitness/vida_saludable_form.html', {'form': form})

def success_view(request):
    return render(request, 'success.html')
@login_required(login_url="login")
def lista(request, pk=None, action=None):
    if pk and action:
        objeto = get_object_or_404(Datos, pk=pk)
        if action == 'delete':
            if request.method == 'POST':
                objeto.delete()
                return redirect('lista')
            context = {
                "datos": Datos.objects.all(),
                "action": "delete",
                "objeto": objeto
            }
            return render(request, 'fitness/lista.html', context)
        elif action == 'edit':
            if request.method == 'POST':
                objeto.nombre = request.POST.get('nombre')
                objeto.peso = request.POST.get('peso')
                objeto.save()
                return redirect('lista')
            context = {
                "datos": Datos.objects.all(),
                "action": "edit",
                "objeto": objeto
            }
            return render(request, 'fitness/lista.html', context)
    elif action == 'add':
        if request.method == 'POST':
            nuevo_objeto = Datos(
                nombre=request.POST.get('nombre'),
                peso=request.POST.get('peso')
            )
            nuevo_objeto.save()
            return redirect('lista')
        context = {
            "datos": Datos.objects.all(),
            "action": "add"
        }
        return render(request, 'fitness/lista.html', context)
    else:
        datos = Datos.objects.all()
        context = {
            "datos": datos,
            "action": None
        }
        return render(request, 'fitness/lista.html', context)