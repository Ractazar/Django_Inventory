from django.contrib import admin

# Register your models here.
from .models import Usuario,Notebooks,Smartphones,Office
admin.site.register(Usuario)
admin.site.register(Office)

class NotebooksAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Info", {"fields": ("marca", "modelo")}),
        ("Hardware", {"fields": ("processador", "memoria_ram", "sistema_operacional", "memoria_interna", "status")}),
        ("Identification", {"fields": ("id_dispositivo", "id_produto", "numero_serie")}),
        ("Miscellaneous", {"fields": ("visivel","criado_por","modificado_por","emprestado","observacoes","ultimo_comeco_manutencao","ultimo_final_manutencao")}),
    )

admin.site.register(Notebooks, NotebooksAdmin)

class SmartphonesAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Info", {"fields": ("marca", "modelo")}),
        ("Hardware", {"fields": ("carregador", "capa_protetora", "status")}),
        ("Identification", {"fields": ("imei_2","imei_1", "numero_chip", "numero_serie")}),
        ("Miscellaneous", {"fields": ("visivel","criado_por","modificado_por","emprestado","ultimo_comeco_manutencao","ultimo_final_manutencao")}),
    )

admin.site.register(Smartphones, SmartphonesAdmin)