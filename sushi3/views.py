# views.py

from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Max
from django.conf import settings
import os

from .models import (
    Piatto, Tavolo, Ordine, Composizione,
    Cliente, Prenotazione, PrenotaT,
    Personale
)


def visualizza_piatti(request):
    piatti = Piatto.objects.all()
    return render(request, 'sushi3/piatti.html', {
        'piatti': piatti,
        'MEDIA_URL': settings.MEDIA_URL
    })


def pagina_ordine_sushi(request):
    if 'carrello' not in request.session:
        request.session['carrello'] = []

    if request.method == 'POST':
        if request.POST.get('action_type') == 'aggiungi':
            piatto_id = request.POST.get('piatto_id')
            if piatto_id:
                carrello = request.session['carrello']
                carrello.append(piatto_id)
                request.session['carrello'] = carrello
                request.session.modified = True
        return redirect('piatti')

    piatti = Piatto.objects.all()
    counts = Counter(request.session.get('carrello', []))
    carrello = [
        {'piatto': Piatto.objects.get(nome_piatto=nome), 'quantita': qty}
        for nome, qty in counts.items()
    ]

    return render(request, 'sushi3/piatti.html', {
        'piatti': piatti,
        'carrello': carrello
    })

def invia_ordine(request):
    carrello = request.session.get('carrello', [])
    if not carrello:
        return redirect('ordina_sushi')

    tavolo = Tavolo.objects.first()
    if not tavolo:
        return HttpResponse("❌ Nessun tavolo disponibile")

    try:
        tavolo_1 = Tavolo.objects.get(pk=1)
    except Tavolo.DoesNotExist:
        return HttpResponse("❌ Tavolo 1 non trovato")

    counts = Counter(carrello)
    npiatti = sum(counts.values())

    max_id = Ordine.objects.filter(id_tavolo=tavolo_1).aggregate(Max('id_ordine'))['id_ordine__max']
    next_id = 1 if max_id is None else max_id + 1

    ordine = Ordine.objects.create(
        id_tavolo=tavolo,
        id_ordine=next_id,
        npiatti=npiatti
    )

    for nome_piatto, qty in counts.items():
        piatto = Piatto.objects.get(nome_piatto=nome_piatto)
        Composizione.objects.create(
            id_ordine=ordine,         # usa l'oggetto Ordine (PK = id)
            id_tavolo=tavolo,         # usa l'oggetto Tavolo
            nome_piatto=piatto,
            quantita=qty
        )

    request.session['carrello'] = []
    return redirect('piatti')

def storico_ordini(request):
    ordini = Ordine.objects.filter(id_tavolo=1)
    lista_ordini = []

    for ordine in ordini:
        composizioni = Composizione.objects.filter(
            id_ordine=ordine,
            id_tavolo=ordine.id_tavolo
        )
        piatti = [(c.nome_piatto.nome_piatto, c.quantita) for c in composizioni]
        lista_ordini.append({
            "ordine": ordine,
            "piatti": piatti
        })

    return render(request, 'storico_ordini.html', {
        "lista_ordini": lista_ordini
    })


def amministratore(request):
    tavoli = Tavolo.objects.all()
    dipendenti = Personale.objects.all()
    return render(request, 'sushi3/amministratore.html', {
        'tavoli': tavoli,
        'dipendenti': dipendenti
    })


@transaction.atomic
def aggiungi_prenotazione(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = request.POST.get('data')
        orario = request.POST.get('orario')
        turno = request.POST.get('turno')
        id_tavolo = request.POST.get('id_tavolo')

        cliente, _ = Cliente.objects.get_or_create(
            username=username,
            defaults={'attivo': 0, 'id_tavolo': None}
        )

        last = Prenotazione.objects.order_by('-id_pren').first()
        new_id = (last.id_pren + 1) if last else 1

        pren = Prenotazione.objects.create(
            data=data,
            orario=orario,
            turno=turno,
            username=cliente
        )

        tavolo = Tavolo.objects.get(id_tavolo=id_tavolo)
        PrenotaT.objects.create(id_pren=pren, id_tavolo=tavolo)

        return redirect('amministratore')

    tavoli = Tavolo.objects.all()
    return render(request, 'sushi3/amministratore.html', {'tavoli': tavoli})


def aggiungi_piatto(request):
    if request.method == 'POST':
        nome = request.POST['nome_piatto']
        descrizione = request.POST['descrizione']
        prezzo = request.POST['prezzo']
        tipologia = request.POST['tipologia']
        immagine = request.FILES['foto']

        if Piatto.objects.filter(nome_piatto=nome).exists():
            return render(request, 'sushi3/amministratore.html', {
                'messaggio_piatto': '⚠️ Il piatto esiste già e non è stato aggiunto.'
            })

        path_dir = os.path.join(settings.MEDIA_ROOT, 'foto_piatti')
        os.makedirs(path_dir, exist_ok=True)

        path_immagine = os.path.join(path_dir, immagine.name)
        with open(path_immagine, 'wb+') as f:
            for chunk in immagine.chunks():
                f.write(chunk)

        Piatto.objects.create(
            nome_piatto=nome,
            descrizione=descrizione,
            prezzo=prezzo,
            tipologia=tipologia,
            foto=immagine.name
        )

        return render(request, 'sushi3/amministratore.html', {
            'messaggio_piatto': '✅ Piatto aggiunto con successo.'
        })


def aggiungi_dipendente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        ruolo = request.POST['ruolo']

        if Personale.objects.filter(nome_pers=nome, ruolo=ruolo).exists():
            return render(request, 'sushi3/amministratore.html', {
                'messaggio_piatto': '⚠️ Dipendente già inserito.'
            })

        Personale.objects.create(nome_pers=nome, ruolo=ruolo)

        return render(request, 'sushi3/amministratore.html', {
            'messaggio_piatto': '✅ Dipendente aggiunto con successo.'
        })


def elimina_dipendente(request, id_personale):
    dipendente = get_object_or_404(Personale, id_personale=id_personale)
    dipendente.delete()
    return redirect('amministratore')
