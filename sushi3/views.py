

from django.shortcuts import render
from .models import Piatto

from django.conf import settings

def visualizza_piatti(request):
    piatti = Piatto.objects.all()
    return render(request, 'sushi3/piatti.html', {'piatti': piatti, 'MEDIA_URL': settings.MEDIA_URL})


from django.shortcuts import render, redirect
from .models import Piatto
from collections import Counter

from django.shortcuts import render, redirect
from .models import Piatto
from collections import Counter

def pagina_ordine_sushi(request):
    if 'carrello' not in request.session:
        request.session['carrello'] = []

    if request.method == 'POST':
        action = request.POST.get('action_type')
        if action == 'aggiungi':
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
        {
            'piatto': Piatto.objects.get(nome_piatto=nome),
            'quantita': qty
        }
        for nome, qty in counts.items()
    ]

    return render(request, 'sushi3/piatti.html', {
        'piatti': piatti,
        'carrello': carrello,
    })





from .models import Ordine, Composizione, Tavolo, Piatto
from django.utils.crypto import get_random_string
from django.http import HttpResponseRedirect
from django.urls import reverse

def invia_ordine(request):
    carrello = request.session.get('carrello', [])

    if not carrello:
        return HttpResponseRedirect(reverse('ordina_sushi'))  # se carrello vuoto

    # Simuliamo un tavolo (es. 1) per ora
    tavolo = Tavolo.objects.first()
    if not tavolo:
        return HttpResponse("❌ Nessun tavolo disponibile")

    # Genera ID ordine (es. random o incrementale)
    id_ordine = int(get_random_string(length=5, allowed_chars='1234567890'))

    # Conta i piatti
    npiatti = len(carrello)

    # Crea ordine
    ordine = Ordine.objects.create(
        id_tavolo=tavolo,
        id_ordine=id_ordine,
        npiatti=npiatti
    )

    # Conta le quantità dei piatti
    from collections import Counter
    counts = Counter(carrello)

    for nome_piatto, qty in counts.items():
        Composizione.objects.create(
            nome_piatto=nome_piatto,
            id_tavolo=tavolo,
            id_ordine=id_ordine,
            quantita=qty
        )

    # Svuota carrello
    request.session['carrello'] = []

    return HttpResponseRedirect(reverse('ordina_sushi'))



###################################################################################
from django.shortcuts import render

def amministratore(request):
    return render(request, 'sushi3/amministratore.html')

from django.shortcuts import render, redirect
from .models import Cliente, Prenotazione, Tavolo, PrenotaT
from django.db import transaction
from django.utils import timezone

@transaction.atomic
def aggiungi_prenotazione(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = request.POST.get('data')
        orario = request.POST.get('orario')
        turno = request.POST.get('turno')
        id_tavolo = request.POST.get('id_tavolo')

        # 1. Crea il cliente se non esiste
        cliente, creato = Cliente.objects.get_or_create(
            username=username,
            defaults={'attivo': 0, 'id_tavolo': None}
        )

        # 2. Trova il prossimo id_pren disponibile
        last = Prenotazione.objects.order_by('-id_pren').first()
        new_id = (last.id_pren + 1) if last else 1

        # 3. Crea la prenotazione
        pren = Prenotazione.objects.create(
        data=data,
        orario=orario,
        turno=turno,
        username=cliente  # ✅ giusto
    )


        # 4. Collega la prenotazione al tavolo
        tavolo = Tavolo.objects.get(id_tavolo=id_tavolo)
        PrenotaT.objects.create(id_pren=pren, id_tavolo=tavolo)

        return redirect('amministratore')

    # GET → visualizza la pagina con i tavoli
    tavoli = Tavolo.objects.all()
    return render(request, 'sushi3/amministratore.html', {'tavoli': tavoli})

import os
from django.conf import settings

def aggiungi_piatto(request):
    if request.method == 'POST':
        nome = request.POST['nome_piatto']
        descrizione = request.POST['descrizione']
        prezzo = request.POST['prezzo']
        tipologia = request.POST['tipologia']
        immagine = request.FILES['foto']

        # Verifica se il piatto già esiste
        if Piatto.objects.filter(nome_piatto=nome).exists():
            return render(request, 'sushi3/amministratore.html', {
                'messaggio_piatto': '⚠️ Il piatto esiste già e non è stato aggiunto.'
            })

        # Salva l'immagine nella cartella media/foto_piatti
        path_dir = os.path.join(settings.MEDIA_ROOT, 'foto_piatti')
        os.makedirs(path_dir, exist_ok=True)

        path_immagine = os.path.join(path_dir, immagine.name)
        with open(path_immagine, 'wb+') as f:
            for chunk in immagine.chunks():
                f.write(chunk)

        # Salva il piatto nel DB con solo il nome del file immagine
        nuovo_piatto = Piatto(
            nome_piatto=nome,
            descrizione=descrizione,
            prezzo=prezzo,
            tipologia=tipologia,
            foto=immagine.name  # salva solo il nome, NON il path completo
        )
        nuovo_piatto.save()

        return render(request, 'sushi3/amministratore.html', {
            'messaggio_piatto': '✅ Piatto aggiunto con successo.'
        })
    
from .models import Personale

def aggiungi_dipendente(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        ruolo = request.POST['ruolo']

        # Controllo per evitare duplicati (nome + ruolo)
        if Personale.objects.filter(nome_pers=nome, ruolo=ruolo).exists():
            return render(request, 'sushi3/amministratore.html', {
                'messaggio_piatto': '⚠️ Dipendente già inserito.'
            })

        Personale.objects.create(
            nome_pers=nome,
            ruolo=ruolo
        )

        return render(request, 'sushi3/amministratore.html', {
            'messaggio_piatto': '✅ Dipendente aggiunto con successo.'
        })
