from django.urls import path, include
from .api import RegisterAPI,LoginAPI,UserAPI,PasswordTokenCheckAPI,RequestPasswordResetEmail,SetNewPasswordAPI
from knox import views as knox_views


urlpatterns = [
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(),name='knox_logout'),
    path('api/auth', include('knox.urls')),
    path("request-reset-email/", RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name ="password-reset-confirm"),
    path('password-reset-complete/', SetNewPasswordAPI.as_view(), name = "password-reset-complete")
]