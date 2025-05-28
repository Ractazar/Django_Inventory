from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("login/", views.login_usuario, name="login"),
    path("registro/", views.registro_usuario, name="registro"),
    path("logout/", views.logout_usuario, name="logout"),
    path("hardware-status/", views.hardware_status, name="hardware_status"),
    path("notebooks/", views.mostrar_notebooks, name="mostrar_notebooks"),
    path("smartphones/", views.mostrar_smartphones, name="mostrar_smartphones"),
    path("adicionar-notebook/", views.adicionar_notebook, name="adicionar_notebook"),
    path("adicionar-smartphone/", views.adicionar_smartphone, name="adicionar_smartphone"),
    path("deletar-notebook/<str:id_dispositivo>/", views.deletar_notebook, name="deletar_notebook"),
    path("deletar-smartphone/<str:numero_serie>/", views.deletar_smartphone, name="deletar_smartphone"),
    path("atualizar-emprestado-notebook/<str:id_dispositivo>/", views.atualizar_emprestado_notebook, name="atualizar_emprestado_notebook"),
    path("atualizar-emprestado-smartphone/<str:numero_serie>/", views.atualizar_emprestado_smartphone, name="atualizar_emprestado_smartphone"),
    path("office/", views.office, name="office"),
    path("atualizar_notebook/", views.atualizar_notebook, name="atualizar_notebook"),
    path("atualizar_smartphone/", views.atualizar_smartphone, name="atualizar_smartphone"),
    path('termos/', views.termos_view, name='termos'),
    path('media/terms.pdf', views.termos_pdf, name='termos_pdf'),
    path('termos/download/', views.termos_download, name='termos_download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)