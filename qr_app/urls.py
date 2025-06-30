from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/login/', views.login_employee),
    path('api/attendance/', views.get_attendance),
    path('api/generate_qr/', views.generate_qr),
    path('api/cancel_qr/', views.cancel_qr),
    path('api/mark_attendance/', views.mark_attendance),
   
   # for QR screen
    path('', views.live_qr_display),
    path('api/reset_password/', auth_views.PasswordResetView.as_view(
        email_template_name='qr_app/password_reset_email.html',
        success_url='/reset-sent/'
    )),
    path('api/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url='/reset-complete/'
    ), name='password_reset_confirm'),
]
