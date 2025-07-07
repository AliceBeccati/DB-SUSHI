# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Prenotazione(models.Model):
    id_pren = models.IntegerField(db_column='ID_Pren', primary_key=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data')  # Field name made lowercase.
    orario = models.TimeField(db_column='Orario')  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=20)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prenotazione'


class PrenotaT(models.Model):
    pk = models.CompositePrimaryKey('ID_tavolo', 'ID_Pren')
    id_pren = models.IntegerField(db_column='ID_Pren')  # Field name made lowercase.
    id_tavolo = models.IntegerField(db_column='ID_tavolo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prenota_T'


class Cliente(models.Model):
    username = models.CharField(db_column='Username', primary_key=True, max_length=50)  # Field name made lowercase.
    id_tavolo = models.CharField(db_column='ID_tavolo', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cliente'


class Pagamento(models.Model):
    id_pag = models.IntegerField(db_column='ID_pag', primary_key=True)  # Field name made lowercase.
    importo = models.DecimalField(db_column='Importo', max_digits=8, decimal_places=2)  # Field name made lowercase.
    data = models.DateField(db_column='Data')  # Field name made lowercase.
    tipologia = models.CharField(db_column='Tipologia', max_length=50)  # Field name made lowercase.
    nclient_sconto = models.IntegerField(db_column='nClient_Sconto', blank=True, null=True)  # Field name made lowercase.
    id_tavolo = models.IntegerField(db_column='ID_tavolo')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pagamento'


class Sconto(models.Model):
    nclient_sconto = models.IntegerField(db_column='nClient_Sconto', primary_key=True)  # Field name made lowercase.
    percentuale = models.DecimalField(db_column='Percentuale', max_digits=5, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sconto'


class Tavolo(models.Model):
    id_tavolo = models.IntegerField(db_column='ID_tavolo', primary_key=True)  # Field name made lowercase.
    tipologia = models.CharField(db_column='Tipologia', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tavolo'


class Ordine(models.Model):
    pk = models.CompositePrimaryKey('ID_tavolo', 'ID_ordine')
    id_tavolo = models.IntegerField(db_column='ID_tavolo')  # Field name made lowercase.
    npiatti = models.IntegerField(db_column='nPiatti')  # Field name made lowercase.
    id_ordine = models.IntegerField(db_column='ID_ordine')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ordine'


class Composizione(models.Model):
    pk = models.CompositePrimaryKey('Nome_piatto', 'ID_tavolo', 'ID_ordine')
    id_tavolo = models.IntegerField(db_column='ID_tavolo')  # Field name made lowercase.
    id_ordine = models.IntegerField(db_column='ID_ordine')  # Field name made lowercase.
    nome_piatto = models.CharField(db_column='Nome_piatto', max_length=100)  # Field name made lowercase.
    quantita = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Composizione'


class Menu(models.Model):
    descrizione = models.CharField(db_column='Descrizione', max_length=255)  # Field name made lowercase.
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    tipologia = models.CharField(db_column='Tipologia', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Menu'


class Piatto(models.Model):
    foto = models.CharField(db_column='Foto', max_length=255)  # Field name made lowercase.
    tipologia = models.CharField(db_column='Tipologia', max_length=50)  # Field name made lowercase.
    descrizione = models.CharField(db_column='Descrizione', max_length=255)  # Field name made lowercase.
    prezzo = models.DecimalField(db_column='Prezzo', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    nome_piatto = models.CharField(db_column='Nome_piatto', primary_key=True, max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Piatto'


class Contiene(models.Model):
    pk = models.CompositePrimaryKey('Nome_piatto', 'Tipologia')
    nome_piatto = models.CharField(db_column='Nome_piatto', max_length=100)  # Field name made lowercase.
    tipologia = models.CharField(db_column='Tipologia', max_length=50)  # Field name made lowercase.
    max_ordine = models.IntegerField(db_column='Max_ordine')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Contiene'


class Allergene(models.Model):
    nome_all = models.CharField(db_column='Nome_all', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Allergene'


class Possiede(models.Model):
    pk = models.CompositePrimaryKey('Nome_all', 'Nome_ingr')
    nome_all = models.CharField(db_column='Nome_all', max_length=50)  # Field name made lowercase.
    nome_ingr = models.CharField(db_column='Nome_ingr', max_length=50)  # Field name made lowercase.
    letalita = models.CharField(db_column='Letalita', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Possiede'


class Ingrediente(models.Model):
    nome_ingr = models.CharField(db_column='Nome_ingr', primary_key=True, max_length=50)  # Field name made lowercase.
    calorie = models.IntegerField(db_column='Calorie')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Ingrediente'


class Formato(models.Model):
    pk = models.CompositePrimaryKey('Nome_ingr', 'Nome_piatto')
    nome_ingr = models.CharField(db_column='Nome_ingr', max_length=50)  # Field name made lowercase.
    nome_piatto = models.CharField(db_column='Nome_piatto', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Formato'


class PiattoPreparato(models.Model):
    stato = models.CharField(db_column='Stato', max_length=50)  # Field name made lowercase.
    id_piatto = models.IntegerField(db_column='ID_piatto', primary_key=True)  # Field name made lowercase.
    nome_piatto = models.CharField(db_column='Nome_piatto', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Piatto_Preparato'


class Prepara(models.Model):
    pk = models.CompositePrimaryKey('ID_personale', 'ID_piatto')
    id_personale = models.IntegerField(db_column='ID_personale')  # Field name made lowercase.
    id_piatto = models.IntegerField(db_column='ID_piatto')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prepara'


class Personale(models.Model):
    nome_pers = models.CharField(db_column='Nome_pers', max_length=100)  # Field name made lowercase.
    ruolo = models.CharField(db_column='Ruolo', max_length=9)  # Field name made lowercase.
    id_personale = models.IntegerField(db_column='ID_personale', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Personale'


class Servizio(models.Model):
    pk = models.CompositePrimaryKey('ID_personale', 'Turno_lavoro', 'Data_turno')
    id_personale = models.IntegerField(db_column='ID_personale')  # Field name made lowercase.
    turno_lavoro = models.CharField(db_column='Turno_lavoro', max_length=20)  # Field name made lowercase.
    data_turno = models.DateField(db_column='Data_turno')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Servizio'


class OrarioServizio(models.Model):
    pk = models.CompositePrimaryKey('Turno_lavoro', 'Data_turno')
    turno_lavoro = models.CharField(db_column='Turno_lavoro', max_length=20)  # Field name made lowercase.
    data_turno = models.DateField(db_column='Data_turno')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Orario_servizio'


class Trasporto(models.Model):
    pk = models.CompositePrimaryKey('ID_tavolo', 'ID_ordine', 'ID_personale')
    id_tavolo = models.IntegerField(db_column='ID_tavolo')  # Field name made lowercase.
    id_ordine = models.IntegerField(db_column='ID_ordine')  # Field name made lowercase.
    id_personale = models.IntegerField(db_column='ID_personale')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trasporto'
