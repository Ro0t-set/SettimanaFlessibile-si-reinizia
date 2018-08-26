# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your models here.
class Aula(models.Model):
    aule= models.CharField(max_length=100, default="")
    max_iscritti= models.IntegerField(default=0)
    def __str__(self):
        return str(self.aule)

    class Meta:
        verbose_name = "Aula"
        verbose_name_plural = "Aule"


class Corso(models.Model):
    titolo = models.CharField(max_length=100)
    studente_referente1 = models.ForeignKey('auth.User', related_name='studente_referente1', null=True)
    studente_referente2 = models.ForeignKey('auth.User', related_name='studente_referente2', blank=True, null=True)
    studente_referente3 = models.ForeignKey('auth.User', related_name='studente_referente3', blank=True, null=True)
    studente_referente4 = models.ForeignKey('auth.User', related_name='studente_referente4', blank=True, null=True)
    studente_referente5 = models.ForeignKey('auth.User', related_name='studente_referente5', blank=True, null=True)
    descrizione= models.TextField(blank=True)
    classi_autori = models.CharField(max_length=40, default="")
    esperti_esterni = models.CharField(max_length=100,blank=True, null=True, default="")
    aule = models.ForeignKey('Aula')


    progressivo= models.BooleanField(default=False)

    f1= models.BooleanField(default=False)
    f2= models.BooleanField(default=False)
    f3= models.BooleanField(default=False)
    f4= models.BooleanField(default=False)
    f5= models.BooleanField(default=False)
    f6= models.BooleanField(default=False)
    f7= models.BooleanField(default=False)
    f8= models.BooleanField(default=False)
    f9= models.BooleanField(default=False)

    convalida1= models.BooleanField(default=False)
    convalida2= models.BooleanField(default=False)
    convalida3= models.BooleanField(default=False)
    convalida4= models.BooleanField(default=False)
    convalida5= models.BooleanField(default=False)



    class Meta:
        verbose_name = "Corso"
        verbose_name_plural = "Corsi"

    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.titolo)




class Iscrizione(models.Model):

    user = models.ForeignKey('auth.User')
    corso1= models.ForeignKey('Corso', blank=True, null=True, related_name="corso1")
    corso2= models.ForeignKey('Corso', blank=True, null=True, related_name="corso2")
    corso3= models.ForeignKey('Corso', blank=True, null=True, related_name="corso3")
    corso4= models.ForeignKey('Corso', blank=True, null=True, related_name="corso4")
    corso5= models.ForeignKey('Corso', blank=True, null=True, related_name="corso5")
    corso6= models.ForeignKey('Corso', blank=True, null=True, related_name="corso6")
    corso7= models.ForeignKey('Corso', blank=True, null=True, related_name="corso7")
    corso8= models.ForeignKey('Corso', blank=True, null=True, related_name="corso8")
    corso9= models.ForeignKey('Corso', blank=True, null=True, related_name="corso9")

    class Meta:
        verbose_name = "Iscrizione"
        verbose_name_plural = "Iscrizioni"

    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


    def __str__(self):
        return str(self.user)
