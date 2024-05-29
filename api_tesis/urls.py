from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_tesis.views import ThesisViewSet, ApprovalViewSet, get_role
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import ThesisViewSet, ApprovalViewSet, get_role, IndexView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import aprobar_tesis, rechazar_tesis
from .views import ver_tesis

router = DefaultRouter()
router.register(r'theses', ThesisViewSet)
router.register(r'approvals', ApprovalViewSet)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/role/', get_role, name='get_role'),  # Corregí la coma innecesaria aquí
    path('subir_tesis/', views.subir_tesis, name='subir_tesis'),
    path('login/', views.login_view, name='login'),
    path('gestion_tesis/', views.gestion_tesis, name='gestion_tesis'), 
    path('ver_tesis/', views.ver_tesis, name='ver_tesis'), 
    path('aprobar_tesis/<int:tesis_id>/', aprobar_tesis, name='aprobar_tesis'),
    path('rechazar_tesis/<int:tesis_id>/', rechazar_tesis, name='rechazar_tesis'), # Define la URL con el nombre 'gestion_tesis'
]
