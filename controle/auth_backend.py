from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            usuario = Usuario.objects.get(email=username)  # Match by email
            if check_password(password, usuario.password):  # Verify hashed password
                return usuario  # Return user object if authentication succeeds
        except Usuario.DoesNotExist:
            return None  # No user found

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None