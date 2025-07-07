
from django.db import models

class Prenotazione(models.Model):
    id_pren = models.AutoField(db_column='ID_Pren', primary_key=True)
    data = models.DateField(db_column='Data')
    orario = models.TimeField(db_column='Orario')
    turno = models.CharField(db_column='Turno', max_length=20)
    username = models.ForeignKey('Cliente', db_column='Username', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Prenotazione'

class PrenotaT(models.Model):
    id_pren = models.ForeignKey('Prenotazione', db_column='ID_Pren', on_delete=models.DO_NOTHING)
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Prenota_T'
        unique_together = (('id_pren', 'id_tavolo'),)

class Cliente(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=50)
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'Cliente'

class Tavolo(models.Model):
    id_tavolo = models.IntegerField(db_column='ID_tavolo', primary_key=True)
    tipologia = models.CharField(db_column='Tipologia', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Tavolo'

class Pagamento(models.Model):
    id_pag = models.AutoField(db_column='ID_pag', primary_key=True)
    importo = models.DecimalField(db_column='Importo', max_digits=8, decimal_places=2)
    data = models.DateField(db_column='Data')
    tipologia = models.CharField(db_column='Tipologia', max_length=50)
    nclient_sconto = models.ForeignKey('Sconto', db_column='nClient_Sconto', on_delete=models.DO_NOTHING, blank=True, null=True)
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Pagamento'

class Sconto(models.Model):
    nclient_sconto = models.IntegerField(db_column='nClient_Sconto', primary_key=True)
    percentuale = models.DecimalField(db_column='Percentuale', max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Sconto'

class Ordine(models.Model):
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING)
    id_ordine = models.IntegerField(db_column='ID_ordine')
    npiatti = models.IntegerField(db_column='nPiatti')

    class Meta:
        db_table = 'Ordine'
        unique_together = (('id_tavolo', 'id_ordine'),)

class Composizione(models.Model):
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING)
    id_ordine = models.ForeignKey('Ordine', db_column='ID_ordine', on_delete=models.DO_NOTHING)
    nome_piatto = models.ForeignKey('Piatto', db_column='Nome_piatto', on_delete=models.DO_NOTHING)
    quantita = models.IntegerField()

    class Meta:
        db_table = 'Composizione'
        unique_together = (('nome_piatto', 'id_tavolo', 'id_ordine'),)

class Menu(models.Model):
    tipologia = models.CharField(db_column='Tipologia', primary_key=True, max_length=50)
    descrizione = models.CharField(db_column='Descrizione', max_length=255)
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Menu'

class Piatto(models.Model):
    nome_piatto = models.CharField(db_column='Nome_piatto', primary_key=True, max_length=100)
    foto = models.CharField(db_column='Foto', max_length=255)
    tipologia = models.ForeignKey('Menu', db_column='Tipologia', on_delete=models.DO_NOTHING)
    descrizione = models.CharField(db_column='Descrizione', max_length=255)
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Piatto'

class Contiene(models.Model):
    nome_piatto = models.ForeignKey('Piatto', db_column='Nome_piatto', on_delete=models.DO_NOTHING)
    tipologia = models.ForeignKey('Menu', db_column='Tipologia', on_delete=models.DO_NOTHING)
    max_ordine = models.IntegerField(db_column='Max_ordine')

    class Meta:
        db_table = 'Contiene'
        unique_together = (('nome_piatto', 'tipologia'),)


class Allergene(models.Model):
    nome_all = models.CharField(db_column='Nome_all', primary_key=True, max_length=50)

    class Meta:
        db_table = 'Allergene'


class Ingrediente(models.Model):
    nome_ingr = models.CharField(db_column='Nome_ingr', primary_key=True, max_length=50)
    calorie = models.IntegerField(db_column='Calorie')

    class Meta:
        db_table = 'Ingrediente'


class Possiede(models.Model):
    nome_all = models.ForeignKey('Allergene', db_column='Nome_all', on_delete=models.DO_NOTHING)
    nome_ingr = models.ForeignKey('Ingrediente', db_column='Nome_ingr', on_delete=models.DO_NOTHING)
    letalita = models.CharField(db_column='Letalita', max_length=20)

    class Meta:
        db_table = 'Possiede'
        unique_together = (('nome_all', 'nome_ingr'),)


class Formato(models.Model):
    nome_ingr = models.ForeignKey('Ingrediente', db_column='Nome_ingr', on_delete=models.DO_NOTHING)
    nome_piatto = models.ForeignKey('Piatto', db_column='Nome_piatto', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Formato'
        unique_together = (('nome_ingr', 'nome_piatto'),)


class PiattoPreparato(models.Model):
    id_piatto = models.AutoField(db_column='ID_piatto', primary_key=True)
    stato = models.CharField(db_column='Stato', max_length=50)
    nome_piatto = models.ForeignKey('Piatto', db_column='Nome_piatto', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Piatto_Preparato'


class Personale(models.Model):
    id_personale = models.AutoField(db_column='ID_personale', primary_key=True)
    nome_pers = models.CharField(db_column='Nome_pers', max_length=100)
    ruolo = models.CharField(db_column='Ruolo', max_length=9)

    class Meta:
        db_table = 'Personale'


class Prepara(models.Model):
    id_personale = models.ForeignKey('Personale', db_column='ID_personale', on_delete=models.DO_NOTHING)
    id_piatto = models.ForeignKey('PiattoPreparato', db_column='ID_piatto', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Prepara'
        unique_together = (('id_personale', 'id_piatto'),)


class OrarioServizio(models.Model):
    turno_lavoro = models.CharField(db_column='Turno_lavoro', max_length=20)
    data_turno = models.DateField(db_column='Data_turno')

    class Meta:
        db_table = 'Orario_servizio'
        unique_together = (('turno_lavoro', 'data_turno'),)


class Servizio(models.Model):
    id_personale = models.ForeignKey('Personale', db_column='ID_personale', on_delete=models.DO_NOTHING)
    turno_lavoro = models.CharField(db_column='Turno_lavoro', max_length=20)
    data_turno = models.DateField(db_column='Data_turno')

    class Meta:
        db_table = 'Servizio'
        unique_together = (('id_personale', 'turno_lavoro', 'data_turno'),)


class Trasporto(models.Model):
    id_tavolo = models.ForeignKey('Tavolo', db_column='ID_tavolo', on_delete=models.DO_NOTHING)
    id_ordine = models.ForeignKey('Ordine', db_column='ID_ordine', on_delete=models.DO_NOTHING)
    id_personale = models.ForeignKey('Personale', db_column='ID_personale', on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'Trasporto'
        unique_together = (('id_tavolo', 'id_ordine', 'id_personale'),)
