from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import Notebooks
from .models import Usuario
from .models import Smartphones
from .models import Office

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)
    email = forms.EmailField(
        error_messages={
            "unique": "Usuário com este Email já existe."
        }
    )

    class Meta:
        model = Usuario
        fields = ["email", "first_name"]
        labels = {"first_name": "Nome"}

    field_order = ["email", "first_name", "password", "confirm_password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)  # Validate the password using Django's validators
        except ValidationError as e:
            self.add_error("password", e)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "As senhas não coincidem.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class NotebooksForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Notebooks.ESCOLHAS_STATUS, widget=forms.Select)
    observacoes = forms.CharField(widget=forms.Textarea, required=False, label="Observações")

    class Meta:
        model = Notebooks
        fields = ["marca", "modelo", "processador", "memoria_ram", "sistema_operacional",
                  "memoria_interna", "id_dispositivo", "id_produto", "numero_serie",
                  "status", "observacoes"]
        labels = {"memoria_ram": "Memória ram", "memoria_interna": "Memória interna", "numero_serie": "Número de série"}
        
class SmartphonesForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Smartphones.ESCOLHAS_STATUS, widget=forms.Select)
    capa_protetora = forms.ChoiceField(choices=Smartphones.POSSUI_PERIFERICO, widget=forms.Select)
    carregador = forms.ChoiceField(choices=Smartphones.POSSUI_PERIFERICO, widget=forms.Select)
    numero_chip = forms.CharField(widget=forms.TextInput, required=False, label="Número do chip")
    imei_2 = forms.CharField(widget=forms.TextInput, required=False)

    class Meta:
        model = Smartphones
        fields = ["marca", "modelo", "numero_serie", "numero_chip", "imei_1",
                  "imei_2", "status", "capa_protetora", "carregador"]
        labels = {"numero_serie": "Número de série"}

class OfficeEntryForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ["senha", "versao", "data_renovacao"]
        
        widgets = {
            "senha": forms.PasswordInput(),
            "versao": forms.TextInput(),
            "data_renovacao": forms.DateInput(attrs={"type": "date"}), # ✅ Forces a date picker
        }

class DocumentoUploadForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['documento']
    documento = forms.FileField(label="Upload do documento assinado", required=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file = self.cleaned_data.get('documento')
        if uploaded_file:
            # Get the user's email and sanitize it for filenames
            email = instance.email.replace('@', '_at_').replace('.', '_')
            # Build new filename
            original_name = uploaded_file.name
            new_name = f"{email}_{original_name}"
            uploaded_file.name = new_name
            instance.documento = uploaded_file
        if commit:
            instance.save()
        return instance