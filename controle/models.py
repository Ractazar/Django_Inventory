from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and returns a regular user with an email instead of a username."""
        if not email:
            raise ValueError("O email é obrigatório.")
        if not password:
            raise ValueError("A senha é obrigatória.")
        email = self.normalize_email(email)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and returns a superuser, ensuring proper permissions."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Set a default documento if not provided
        #if not extra_fields.get("documento"):
            #extra_fields["documento"] = ContentFile(b"SuperUser PDF", "default.pdf")
        
        return self.create_user(email, password, **extra_fields)  # No 'username' required

class Usuario(AbstractUser):
    
    username = None  # Remove the username field
    first_name = models.CharField(max_length=100, blank=False)
    documento = models.FileField(upload_to="documentos/", validators=[FileExtensionValidator(allowed_extensions=["pdf"])], default=None, null=True, blank=True)  # FileField for PDF   

    email = models.EmailField(unique=True)  # Keep email as the login field

    USERNAME_FIELD = "email"  # Set email as the unique identifier
    REQUIRED_FIELDS = ["first_name"]  # Customize required fields

    objects = UsuarioManager()

    class Meta:
        db_table = "usuarios"
    
class Notebooks(models.Model):

    ESCOLHAS_STATUS = [("Estoque", "Estoque"), ("Em Uso", "Em Uso"), ("Manutenção", "Manutenção")]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100) 
    processador = models.CharField(max_length=100)
    memoria_ram = models.CharField(max_length=100) 
    sistema_operacional = models.CharField(max_length=100) 
    memoria_interna = models.CharField(max_length=100) 
    id_dispositivo = models.CharField(max_length=100, unique=True) 
    id_produto = models.CharField(max_length=100) 
    numero_serie = models.CharField(max_length=100, unique=True)  
    status = models.CharField(max_length=10, choices=ESCOLHAS_STATUS)
    observacoes = models.TextField(null=True, blank=True)
    criado_por = models.CharField(max_length=100)  
    modificado_por = models.CharField(max_length=100, null=True, blank=True)  
    emprestado = models.CharField(max_length=100, default='Não')  
    ultimo_comeco_manutencao = models.DateTimeField(null=True, blank=True)  # Date - datetime
    ultimo_final_manutencao = models.DateTimeField(null=True, blank=True)  # Date - datetime
    visivel = models.BooleanField(default=True)

    def __str__(self):
        return self.id_dispositivo  # String representation of the model
    
class Smartphones(models.Model):

    ESCOLHAS_STATUS = [("Estoque", "Estoque"), ("Em Uso", "Em Uso"), ("Manutenção", "Manutenção")]
    POSSUI_PERIFERICO = [("Sim", "Sim"), ("Não", "Não")]

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100) 
    numero_serie = models.CharField(max_length=100, unique=True)
    numero_chip = models.CharField(max_length=100, null=True) 
    imei_1 = models.CharField(max_length=100, unique=True) 
    imei_2 = models.CharField(max_length=100, null=True)  
    status = models.CharField(max_length=10, choices=ESCOLHAS_STATUS)
    capa_protetora = models.CharField(max_length=3, choices=POSSUI_PERIFERICO)
    carregador = models.CharField(max_length=3, choices=POSSUI_PERIFERICO)
    criado_por = models.CharField(max_length=100)  
    modificado_por = models.CharField(max_length=100, null=True, blank=True)
    emprestado = models.CharField(max_length=100, default='Não')  
    ultimo_comeco_manutencao = models.DateTimeField(null=True, blank=True)  # Date - datetime
    ultimo_final_manutencao = models.DateTimeField(null=True, blank=True)  # Date - datetime
    visivel = models.BooleanField(default=True)

    def __str__(self):
        return self.numero_serie  # String representation of the model
    
class Office(models.Model):
    email = models.CharField(max_length=100, unique=True)  # Email - varchar(100) - Unique
    senha = models.CharField(max_length=100)  # Password - varchar(100)
    versao = models.CharField(max_length=100)
    data_renovacao = models.DateField()

    def __str__(self):
        return self.email  # String representation of the model