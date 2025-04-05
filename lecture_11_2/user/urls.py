from django.urls import path
from .views import login_page_view, register_page_view, handle_logout, forgot_password_view, reset_password_view, settings_page_view

urlpatterns = [
    path('login/', login_page_view, name='login_page'),
    path('register/', register_page_view, name='register_page'),
    path('settings/', settings_page_view, name='settings_page'),
    path('logout/', handle_logout, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password_page'),
    path('reset-password/<slug:token>', reset_password_view, name='reset_password_page')
]
