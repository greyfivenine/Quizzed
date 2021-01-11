from django.urls import path
from .views import *

urlpatterns = [
    path('change_password/', ChangePassword.as_view(), name = 'change_pwd'),
    path('change_email/', ChangeEmail.as_view(), name = 'change_email'),
    path('profile/', Profile.as_view(), name = 'profile'),
    path('signup/', sign_up, name = 'signup'),
    path('login/', log_in, name = 'login'),
    path('logout/', log_out, name = 'logout'),
]
