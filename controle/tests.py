import tempfile
import shutil
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from controle.models import Usuario

#Model Tests
TEMP_MEDIA_ROOT0 = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT0)
class UsuarioManagerTests(TestCase):
    def test_create_user(self):
        user = Usuario.objects.create_user(email="test@example.com", password="securepassword")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepassword"))

    def test_create_superuser(self):
        superuser = Usuario.objects.create_superuser(email="admin@example.com", password="adminpass")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

TEMP_MEDIA_ROOT = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class LoginPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="login@example.com",
            password="StrongPass123",
            first_name="Test",
            documento=SimpleUploadedFile("doc.pdf", b"PDF", content_type="application/pdf")
        )

    def test_get_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    def test_successful_login(self):
        response = self.client.post(reverse("login"), {
            "email": "login@example.com",
            "senha": "StrongPass123"
        })
        self.assertRedirects(response, reverse("hardware_status"))

    def test_invalid_login(self):
        response = self.client.post(reverse("login"), {
            "email": "wrong@example.com",
            "senha": "wrongpass"
        })
        self.assertContains(response, "Usuário ou senha inválido.")

    def test_invalid_email(self):
        response = self.client.post(reverse("login"), {
            "email": "wrong@example.com",
            "senha": "StrongPass123"
        })
        self.assertContains(response, "Usuário ou senha inválido.")

    def test_invalid_senha(self):
        response = self.client.post(reverse("login"), {
            "email": "login@example.com",
            "senha": "wrongpass"
        })
        self.assertContains(response, "Usuário ou senha inválido.")

    def test_missing_fields(self):
        response = self.client.post(reverse("login"), {
            "email": "",
            "senha": ""
        })
        self.assertContains(response, "Este campo é obrigatório")

    def test_missing_email(self):
        response = self.client.post(reverse("login"), {
            "email": "",
            "senha": "StrongPass123"
        })
        self.assertContains(response, "Este campo é obrigatório")

    def test_missing_senha(self):
        response = self.client.post(reverse("login"), {
            "email": "login@example.com",
            "senha": ""
        })
        self.assertContains(response, "Este campo é obrigatório")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

TEMP_MEDIA_ROOT_2 = tempfile.mkdtemp()
@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT_2)
class RegistroPageTests(TestCase):

    def test_get_registration_page(self):
        response = self.client.get(reverse("registro"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registrar")
    
    def test_successful_registration(self):
        response = self.client.post(reverse("registro"), {
            "email": "newuser@example.com",
            "first_name": "Test",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        })
        self.assertRedirects(response, reverse("login"))
        self.assertTrue(get_user_model().objects.filter(email="newuser@example.com").exists())

    def test_missing_fields(self):
        response = self.client.post(reverse("registro"), {})
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_missing_email(self):
        response = self.client.post(reverse("registro"), {
            "first_name": "Test",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        })
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_missing_first_name(self):
        response = self.client.post(reverse("registro"), {
            "email": "newuser@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        })
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_missing_password(self):
        response = self.client.post(reverse("registro"), {
            "email": "newuser@example.com",
            "first_name": "Test",
            "confirm_password": "StrongPass123",
        })
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_missing_confirm_password(self):
        response = self.client.post(reverse("registro"), {
            "email": "newuser@example.com",
            "first_name": "Test",
            "password": "StrongPass123",
        })
        self.assertContains(response, "Este campo é obrigatório", status_code=200)

    def test_password_mismatch(self):
        response = self.client.post(reverse("registro"), {
            "email": "user2@example.com",
            "first_name": "Test",
            "password": "abc12345",
            "confirm_password": "different",
        })
        self.assertContains(response, "As senhas não coincidem.")

    def test_weak_short_password(self):
        response = self.client.post(reverse("registro"), {
            "email": "user3@example.com",
            "first_name": "Test",
            "password": "abc123",
            "confirm_password": "abc123",
        })
        self.assertContains(response, "This password is too short")

    def test_weak_numeric_password(self):
        response = self.client.post(reverse("registro"), {
            "email": "user3@example.com",
            "first_name": "Test",
            "password": "12345678",
            "confirm_password": "12345678",
        })
        self.assertContains(response, "Esta senha é inteiramente numérica")

    def test_weak_common_password(self):
        response = self.client.post(reverse("registro"), {
            "email": "user3@example.com",
            "first_name": "Test",
            "password": "password123",
            "confirm_password": "password123",
        })
        self.assertContains(response, "Esta senha é muito comum")

    def test_duplicate_email(self):
        _ = get_user_model().objects.create_user(email="dup@example.com", password="StrongPass123", first_name="Test", documento=SimpleUploadedFile("doc.pdf", b"PDF", content_type="application/pdf"))
        response = self.client.post(reverse("registro"), {
            "email": "dup@example.com",
            "first_name": "Test",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        })
        self.assertContains(response, "Usuário com este Email já existe", status_code=200)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT_2, ignore_errors=True)