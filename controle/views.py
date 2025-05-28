import json
from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.db.models import Case, When, Value, CharField
from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, localtime
import locale
locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")
import os

from .forms import LoginForm
from .forms import RegisterForm
from .forms import NotebooksForm
from .forms import SmartphonesForm
from .forms import OfficeEntryForm
from .forms import DocumentoUploadForm

from .models import Notebooks
from .models import Smartphones
from .models import Office

M = 'Manutenção'
MUDA_DATA = "%d de %B de %Y às %H:%M"
TERMOS = 'terms.pdf'

# Create your views here.
def login_usuario(request):
    error_message = None

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            senha = form.cleaned_data["senha"]

            usuario = authenticate(email=email, password=senha)
            if usuario:
                login(request, usuario)  # Log the user in
                return redirect("hardware_status")  # Redirect to a protected page
            else:
                error_message = "Usuário ou senha inválido."
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form, "error_message": error_message})

def registro_usuario(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to the login page after successful registration
    else:
        form = RegisterForm()
    return render(request, "registro.html", {"form": form})

def logout_usuario(request):
    logout(request)  # Logs out the user
    return redirect("login")  # Redirect them to the login page

@login_required
def hardware_status(request):
    if request.method == "GET":

        query = """SELECT 'Em Uso' as status, (SELECT COUNT(*) from controle_notebooks where status='Em Uso') as notebooks, (SELECT COUNT(*) from controle_smartphones where status='Em Uso') as smartphones
            union
            SELECT 'Estoque' as status, (SELECT COUNT(*) from controle_notebooks where status='Estoque') as notebooks, (SELECT COUNT(*) from controle_smartphones where status='Estoque') as smartphones
            union
            SELECT 'Manutenção' as status, (SELECT COUNT(*) from controle_notebooks where status='Manutenção') as notebooks, (SELECT COUNT(*) from controle_smartphones where status='Manutenção') as smartphones"""

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

    return render(request, "hardware_status.html", {"status": results})

@login_required
def mostrar_notebooks(request):
    notebooks = Notebooks.objects.filter(visivel=True)

    # Process the 'emprestado' field
    user_email = request.user.email
    for notebook in notebooks:
        if notebook.emprestado != "Não" and notebook.emprestado != user_email:
            notebook.emprestado = "Yes"  # Replace with "Yes" if not "Não" or the user's email

    # Extract unique values for dropdown filters
    unique_marca = notebooks.values_list('marca', flat=True).distinct()
    unique_modelo = notebooks.values_list('modelo', flat=True).distinct()
    unique_processador = notebooks.values_list('processador', flat=True).distinct()
    unique_memoria_ram = notebooks.values_list('memoria_ram', flat=True).distinct()
    unique_sistema_operacional = notebooks.values_list('sistema_operacional', flat=True).distinct()
    unique_memoria_interna = notebooks.values_list('memoria_interna', flat=True).distinct()
    unique_id_dispositivo = notebooks.values_list('id_dispositivo', flat=True).distinct()
    unique_id_produto = notebooks.values_list('id_produto', flat=True).distinct()
    unique_numero_serie = notebooks.values_list('numero_serie', flat=True).distinct()
    unique_status = notebooks.values_list('status', flat=True).distinct()
    unique_criado_por = notebooks.values_list('criado_por', flat=True).distinct()
    unique_modificado_por = notebooks.values_list('modificado_por', flat=True).distinct()
    
    # Process unique_emprestado values
    unique_emprestado = notebooks.values_list('emprestado', flat=True).distinct()
    processed_unique_emprestado = []
    for emprestado in unique_emprestado:
        if emprestado != "Não" and emprestado != user_email:
            processed_unique_emprestado.append("Yes")
        else:
            processed_unique_emprestado.append(emprestado)
    processed_unique_emprestado = list(set(processed_unique_emprestado))  # Ensure unique values

    return render(request, "tabela_notebooks.html", {
        "data": notebooks,
        "unique_marca": unique_marca,
        "unique_modelo": unique_modelo,
        "unique_processador": unique_processador,
        "unique_memoria_ram": unique_memoria_ram,
        "unique_sistema_operacional": unique_sistema_operacional,
        "unique_memoria_interna": unique_memoria_interna,
        "unique_id_dispositivo": unique_id_dispositivo,
        "unique_id_produto": unique_id_produto,
        "unique_numero_serie": unique_numero_serie,
        "unique_status": unique_status,
        "unique_criado_por": unique_criado_por,
        "unique_modificado_por": unique_modificado_por,
        "unique_emprestado": processed_unique_emprestado,
    })

@login_required
def mostrar_smartphones(request):
    # Fetch all smartphones
    smartphones = Smartphones.objects.filter(visivel=True)

    # Process the 'emprestado' field for each smartphone
    user_email = request.user.email
    for smartphone in smartphones:
        if smartphone.emprestado != "Não" and smartphone.emprestado != user_email:
            smartphone.emprestado = "Yes"  # Replace with "Yes" if not "Não" or the user's email

    # Extract unique values for dropdown filters
    unique_marca = smartphones.values_list('marca', flat=True).distinct()
    unique_modelo = smartphones.values_list('modelo', flat=True).distinct()
    unique_numero_serie = smartphones.values_list('numero_serie', flat=True).distinct()
    unique_numero_chip = smartphones.values_list('numero_chip', flat=True).distinct()
    unique_imei_1 = smartphones.values_list('imei_1', flat=True).distinct()
    unique_imei_2 = smartphones.values_list('imei_2', flat=True).distinct()
    unique_status = smartphones.values_list('status', flat=True).distinct()
    unique_capa_protetora = smartphones.values_list('capa_protetora', flat=True).distinct()
    unique_carregador = smartphones.values_list('carregador', flat=True).distinct()
    unique_criado_por = smartphones.values_list('criado_por', flat=True).distinct()
    unique_modificado_por = smartphones.values_list('modificado_por', flat=True).distinct()

    # Process unique_emprestado values
    unique_emprestado = smartphones.values_list('emprestado', flat=True).distinct()
    processed_unique_emprestado = []
    for emprestado in unique_emprestado:
        if emprestado != "Não" and emprestado != user_email:
            processed_unique_emprestado.append("Yes")
        else:
            processed_unique_emprestado.append(emprestado)
    processed_unique_emprestado = list(set(processed_unique_emprestado))  # Ensure unique values

    return render(request, "tabela_smartphones.html", {
        "data": smartphones,
        "unique_marca": unique_marca,
        "unique_modelo": unique_modelo,
        "unique_numero_serie": unique_numero_serie,
        "unique_numero_chip": unique_numero_chip,
        "unique_imei_1": unique_imei_1,
        "unique_imei_2": unique_imei_2,
        "unique_status": unique_status,
        "unique_capa_protetora": unique_capa_protetora,
        "unique_carregador": unique_carregador,
        "unique_criado_por": unique_criado_por,
        "unique_modificado_por": unique_modificado_por,
        "unique_emprestado": processed_unique_emprestado,
    })

@login_required
def adicionar_notebook(request):
    if request.method == "POST":
        form = NotebooksForm(request.POST)
        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.criado_por = request.user.email  # Set created_by
            notebook.emprestado = "Não"  # Always 'Não'

            if notebook.status == M:
                notebook.ultimo_comeco_manutencao = now() 
            
            notebook.save()
            messages.success(request, "Notebook adicionado com sucesso!")
            form = NotebooksForm()
    else:
        form = NotebooksForm()

    return render(request, "adicionar_notebook.html", {"form": form})

@login_required
def adicionar_smartphone(request):
    if request.method == "POST":
        form = SmartphonesForm(request.POST)
        if form.is_valid():
            smartphone = form.save(commit=False)
            smartphone.criado_por = request.user.email  # Set created_by
            smartphone.emprestado = "Não"  # Always 'Não'

            if smartphone.status == M:
                smartphone.ultimo_comeco_manutencao = now() 
            
            smartphone.save()
            messages.success(request, "Smartphone adicionado com sucesso!")
            form = SmartphonesForm()

    else:
        form = SmartphonesForm()

    return render(request, "adicionar_smartphone.html", {"form": form})

@login_required
def deletar_notebook(_,id_dispositivo):
    notebook = get_object_or_404(Notebooks, id_dispositivo=id_dispositivo)
    notebook.visivel = False  # Soft delete
    notebook.save()
    
    return JsonResponse({"success": True})  # Return JSON response for frontend

@login_required
def deletar_smartphone(_,numero_serie):
    smartphone = get_object_or_404(Smartphones, numero_serie=numero_serie)
    smartphone.visivel = False  # Soft delete
    smartphone.save()
    
    return JsonResponse({"success": True})  # Return JSON response for frontend

@login_required
def atualizar_emprestado_notebook(request, id_dispositivo):
    if request.method == "POST":
        try:
            notebook = Notebooks.objects.get(id_dispositivo=id_dispositivo)
            data = json.loads(request.body)
            notebook.emprestado = data.get("emprestado", "")
            notebook.save()
            return JsonResponse({"success": True})
        except Notebooks.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notebook não encontrado"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
def atualizar_emprestado_smartphone(request, numero_serie):
    if request.method == "POST":
        try:
            smartphone = Smartphones.objects.get(numero_serie=numero_serie)
            data = json.loads(request.body)
            smartphone.emprestado = data.get("emprestado", "")
            smartphone.save()
            return JsonResponse({"success": True})
        except Smartphones.DoesNotExist:
            return JsonResponse({"success": False, "error": "Smartphone não encontrado"})
    return JsonResponse({"success": False, "error": "Invalid request"})

@login_required
def atualizar_notebook(request):
    def format_manutencao_date(dt):
        if not dt:
            return None
        formatted = localtime(dt).strftime(MUDA_DATA)
        formatted = formatted[:6] + formatted[6:].capitalize()
        if formatted[0] == "0":
            formatted = formatted[1:]
        return formatted

    def update_manutencao_fields(notebook, column, value, ultimo_comeco, ultimo_final):
        if column == "status":
            if value == M and ultimo_comeco:
                notebook.ultimo_comeco_manutencao = now()
            elif value != M and ultimo_final:
                notebook.ultimo_final_manutencao = now()

    if request.method == "POST":
        data = json.loads(request.body)
        notebook_id = data.get("id")
        column = data.get("column")
        value = data.get("value")
        modificado_por = data.get("modificado_por")
        ultimo_comeco_manutencao = data.get("ultimo_comeco_manutencao")
        ultimo_final_manutencao = data.get("ultimo_final_manutencao")

        try:
            notebook = Notebooks.objects.get(id_dispositivo=notebook_id)
            setattr(notebook, column, value)
            notebook.modificado_por = modificado_por

            update_manutencao_fields(
                notebook, column, value, ultimo_comeco_manutencao, ultimo_final_manutencao
            )

            notebook.save()

            return JsonResponse({
                "success": True,
                "modificado_por": notebook.modificado_por,
                "ultimo_comeco_manutencao": format_manutencao_date(notebook.ultimo_comeco_manutencao),
                "ultimo_final_manutencao": format_manutencao_date(notebook.ultimo_final_manutencao),
            })
        except Notebooks.DoesNotExist:
            return JsonResponse({"success": False, "error": "Notebook not found."})
    return JsonResponse({"success": False, "error": "Invalid request method."})

@login_required
def atualizar_smartphone(request):
    def format_manutencao_date(dt):
        if not dt:
            return None
        formatted = localtime(dt).strftime(MUDA_DATA)
        formatted = formatted[:6] + formatted[6:].capitalize()
        if formatted[0] == "0":
            formatted = formatted[1:]
        return formatted

    def update_manutencao_fields(smartphone, column, value, ultimo_comeco, ultimo_final):
        if column == "status":
            if value == M and ultimo_comeco:
                smartphone.ultimo_comeco_manutencao = now()
            elif value != M and ultimo_final:
                smartphone.ultimo_final_manutencao = now()

    if request.method == "POST":      

        data = json.loads(request.body)
        smartphone_id = data.get("id")
        column = data.get("column")
        value = data.get("value")
        modificado_por = data.get("modificado_por")
        ultimo_comeco_manutencao = data.get("ultimo_comeco_manutencao")
        ultimo_final_manutencao = data.get("ultimo_final_manutencao")

        try:
            smartphone = Smartphones.objects.get(numero_serie=smartphone_id)
            setattr(smartphone, column, value)
            smartphone.modificado_por = modificado_por

            update_manutencao_fields(
                smartphone, column, value, ultimo_comeco_manutencao, ultimo_final_manutencao
            )

            smartphone.save()

            return JsonResponse({
                "success": True,
                "modificado_por": smartphone.modificado_por,
                "ultimo_comeco_manutencao": format_manutencao_date(smartphone.ultimo_comeco_manutencao),
                "ultimo_final_manutencao": format_manutencao_date(smartphone.ultimo_final_manutencao),
            })
        except Smartphones.DoesNotExist:
            return JsonResponse({"success": False, "error": "Smartphone not found."})
        
    return JsonResponse({"success": False, "error": "Invalid request method."})

@login_required
def office(request):
    email = request.user.email  # Get the logged-in user's email
    office_entries = Office.objects.filter(email=email).annotate(
        status=Case(
            When(data_renovacao__gt=now().date(), then=Value("Ativado")),
            default=Value("Desativado"),
            output_field=CharField()
        )
    )

    if request.method == "POST":
        form = OfficeEntryForm(request.POST)
        if form.is_valid():
            _, _ = Office.objects.update_or_create(
                email=email,  # Find the existing entry by email
                defaults={  # Update these fields
                    "senha": form.cleaned_data["senha"],  # Ensure hashing if needed
                    "versao": form.cleaned_data["versao"],
                    "data_renovacao": form.cleaned_data["data_renovacao"],
                }
            )

    return render(request, "office.html", {"form": OfficeEntryForm(), "office_entries": office_entries})

@login_required
def termos_view(request):
    user = request.user
    upload_success = False

    if request.method == "POST":
        form = DocumentoUploadForm(request.POST, request.FILES, instance=user)
        # Only save if a new file was uploaded
        if form.is_valid() and request.FILES.get('documento'):
            form.save()
            upload_success = True
    else:
        form = DocumentoUploadForm(instance=user)

    return render(request, "termos.html", {
        "form": form,
        "upload_success": upload_success,
    })

@xframe_options_exempt
def termos_pdf(_):
    pdf_path = os.path.join(settings.MEDIA_ROOT, TERMOS)
    if not os.path.exists(pdf_path):
        raise Http404("Arquivo não encontrado")
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')

@login_required
def termos_download(_):
    terms_file = os.path.join(settings.MEDIA_ROOT, TERMOS)
    if not os.path.exists(terms_file):
        raise Http404("Terms file not found.")
    return FileResponse(open(terms_file, 'rb'), as_attachment=True, filename=TERMOS)