from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hasaba-almak/', views.register_view, name='register'),
    path('giris/', views.login_view, name='login'),
    path('cykys/', views.logout_view, name='logout'),
    path('dolandyrys-paneli/', views.dashboard, name='dashboard'),
    path('trafik-analizi/', views.traffic_analysis, name='traffic_analysis'),
    path('ai-model/', views.ai_model_management, name='ai_model'),
    path('duyduryslar/', views.alerts_view, name='alerts'),
    path('ulanyjylar/', views.user_management, name='user_management'),
    path('ulanyjylar/<int:pk>/uytget/', views.user_edit, name='user_edit'),
    path('hasabatlar/', views.reports_view, name='reports'),
    path('sazlamalar/', views.settings_view, name='settings_page'),
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/detect/', views.api_detect, name='api_detect'),
    path('api/token/', views.api_token, name='api_token'),
]
