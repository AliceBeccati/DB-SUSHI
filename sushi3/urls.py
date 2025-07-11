from django.urls import path
from . import views

urlpatterns = [
    path('piatti/', views.pagina_ordine_sushi, name='piatti'),
    path('invia-ordine/', views.invia_ordine, name='invia_ordine'),
    path('amministratore/', views.amministratore, name='amministratore'),
    path('aggiungi-prenotazione/', views.aggiungi_prenotazione, name='aggiungi_prenotazione'),
    path('aggiungi-piatto/', views.aggiungi_piatto, name='aggiungi_piatto'),
    path('aggiungi-dipendente/', views.aggiungi_dipendente, name='aggiungi_dipendente'),
    path('elimina-dipendente/<int:id_personale>/', views.elimina_dipendente, name='elimina_dipendente'),
    path('storico/', views.storico_ordini, name='storico_ordini'),
]

