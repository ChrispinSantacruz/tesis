from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required
from .models import Thesis, Approval
from .serializers import ThesisSerializer, ApprovalSerializer
from .permissions import IsStudent, IsTeacher
from .forms import ThesisForm, ApprovalForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Thesis



@login_required
def rechazar_tesis(request, tesis_id):
    try:
        # Obtener la tesis específica por su ID
        tesis = Thesis.objects.get(id=tesis_id)
        # Realizar la lógica de rechazo aquí
        tesis.approved = False
        tesis.save()
        # Redirigir a una página de éxito o a donde sea apropiado después de rechazar la tesis
        return redirect('gestion_tesis')
    except Thesis.DoesNotExist:
        # Si la tesis no existe, manejar el error adecuadamente
        return render(request, 'error.html', {'message': 'La tesis no existe.'})


@login_required
def login_redirect(request):
    if request.user.groups.filter(name='teachers').exists():
        return redirect('gestion_tesis')  # Redirigir al docente a la página de gestión de tesis
    else:
        return redirect('subir_tesis')  # Redirigir al estudiante a la página de subir tesis


@login_required
def aprobar_tesis(request, tesis_id):
    try:
        # Obtener la tesis específica por su ID
        tesis = Thesis.objects.get(id=tesis_id)
        # Realizar la lógica de aprobación aquí
        tesis.approved = True
        tesis.save()
        # Redirigir a una página de éxito o a donde sea apropiado después de aprobar la tesis
        return redirect('gestion_tesis')
    except Thesis.DoesNotExist:
        # Si la tesis no existe, manejar el error adecuadamente
        return render(request, 'error.html', {'message': 'La tesis no existe.'})


@login_required
def subir_tesis(request):
    if request.method == 'POST':
        form = ThesisForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.student = request.user
            form.save()
            return redirect('index')  # Redirige a la página de inicio
    else:
        form = ThesisForm()
    return render(request, 'subir_tesis.html', {'form': form})


@login_required
def gestion_tesis(request):
    # Obtener todas las tesis
    tesis_list = Thesis.objects.all()

    return render(request, 'gestion_tesis.html', {
        'tesis_list': tesis_list,
    })


def login_view(request):
    error_message = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirigir según el rol del usuario
                if user.groups.filter(name='Docentes').exists():
                    return redirect('gestion_tesis')
                elif user.groups.filter(name='estudiantes').exists():
                    return redirect('subir_tesis')
                else:
                    return redirect('index')  # Redirigir a una página genérica si no tiene un rol definido
            else:
                error_message = "Usuario o contraseña incorrectos."
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

class IndexView(TemplateView):
    template_name = 'index.html'


class ThesisViewSet(viewsets.ModelViewSet):
    queryset = Thesis.objects.all()
    serializer_class = ThesisSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(approved_by=self.request.user)


@api_view(['GET'])
def get_role(request):
    if request.user.groups.filter(name='students').exists():
        return Response({'role': 'student'})
    elif request.user.groups.filter(name='teachers').exists():
        return Response({'role': 'teacher'})
    return Response({'role': 'unknown'})


class CustomTokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

def ver_tesis(request):
    # Obtener todas las tesis
    tesis_list = Thesis.objects.all()

    return render(request, 'ver_tesis.html', {'tesis_list': tesis_list})
