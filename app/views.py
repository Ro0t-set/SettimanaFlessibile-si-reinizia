# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.utils import timezone
from .models import Corso, Iscrizione, Approvazione
from django.shortcuts import get_object_or_404, render
from .forms import CreaCorsi, IscrizioneForm, Mail, CercaCorsi, ConvalidaCorsi
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
#from __future__ import unicode_literals
import datetime
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.template.loader import render_to_string
from django.http import Http404
from django.contrib import messages
@csrf_protect

def errore(request):
    return render(request, 'corsi/errore.html')

def successo(request):
    return render(request, 'corsi/successo.html')

def errorefasciapiena(request):
    return render(request, 'corsi/errore_fasciapiena.html')

def disp_classi(request):
    return render(request, 'corsi/disp_classi.html')

def disp_classi_arte(request):
    return render(request, 'corsi/disp_classi_arte.html')

def disp_classi_informatica(request):
    return render(request, 'corsi/disp_classi_informatica.html')

def disp_classi_magna(request):
    return render(request, 'corsi/disp_classi_magna.html')

def disp_classi_palestra(request):
    return render(request, 'corsi/disp_classi_palestra.html')

@login_required(login_url='/login/')
def crea(request):
    convalida= ConvalidaCorsi
    if request.method == "POST":

        form = CreaCorsi(request.POST)

        if form.is_valid():

            corso = form.save(commit=False)
            #convalida = convalida.save(commit=False)

            corso.author = request.user
            corso.published_date = timezone.now()


            subject, from_email, to = 'corsi', 'settimanaflessibile@gmail.com', 'settimanaflessibile@gmail.com'
            text_content = '456'
            html_content =  ( str(form) )





            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            corso.save()
            #msg.send()
            for i in range(1,5):
                i=str(i)
                if eval('corso.studente_referente'+i) != None:
                    convalida=Approvazione.objects.create(corso_id= corso.id)
                    convalida.alunno = eval('corso.studente_referente'+i)
                    convalida.save()

            return redirect('successo')

    else:
        form = CreaCorsi()


    return render(request, 'corsi/crea.html', {'form' : form , 'convalida':convalida})

@login_required(login_url='/login/')
def home (request):

    # approvazione=[]
    # for i in range(1,5):
    #     i=str(i)
    #     try:
    #         selezione_della_approvazione= str(eval('Corso.objects.get(studente_referente'+i+'=request.user)'))
    #         approvazione.append(selezione_della_approvazione)
    #
    #     except:
    #         pass
    #
    #
    #
    # if request.method == "POST":
    #     corso_da_approvare = str(request.POST.get("name"))
    #     print(corso_da_approvare)
    #     ccorso_convalidato= eval('Corso.objects.get(titolo='+corso_da_approvare+')')
    #     form = CreaCorsi(request.POST, instance = corso_da_approvare)
    #     if form.is_valid():
    #         print("cazzo")
    #         conferma = form.save(commit=False)
    #         conferma.save()
    #
    # else:
    #     form=CreaCorsi(instance = corso_da_approvare)



    # for approvazione in approvazione:
    #     nome_corso, numero_corso = approvazione.split('-')
    #     print(nome_corso)


        # id_referente = str(request.GET.get("idreferente"))
        # if id_referente != "None":
        #     corso_convalidato=(eval('Corso.objects.get(studente_referente'+id_referente+'=request.user)'))
        #     corso_convalidato=eval('corso_convalidato.convalida'+id_referente)
        #     print(corso_convalidato)
        #     corso_convalidato = True
        #     print(corso_convalidato)
        #     corso_convalidato.save(commit=False)


    return render(request, 'corsi/home.html', {})

@login_required(login_url='/login/')
def tabelle (request):
     cerca = request.GET.get("q")
     form = CercaCorsi(request.GET)
     corsi = Corso.objects.all()
     contatore1= Corso.objects.filter(f1=True)
     contatore2= Corso.objects.filter(f2=True)
     contatore3= Corso.objects.filter(f3=True)
     contatore4= Corso.objects.filter(f4=True)
     contatore5= Corso.objects.filter(f5=True)
     contatore6= Corso.objects.filter(f6=True)
     contatore7= Corso.objects.filter(f7=True)
     contatore8= Corso.objects.filter(f8=True)
     contatore9= Corso.objects.filter(f9=True)

     contatore=[contatore1.count(),contatore2.count(),contatore3.count(),contatore4.count(),contatore5.count(),contatore6.count(),contatore7.count(),contatore8.count(),contatore9.count()]
     if form.is_valid():
         corsi = Corso.objects.filter(Q(titolo__icontains=cerca)|
         #Q(studenti_referenti__icontains=cerca)|
         Q(aule__aule__exact=cerca))




     return render(request, 'corsi/tabelle.html', {'corsi': corsi,  'form':form , 'contatore':contatore})



@login_required(login_url='/login/')
def privata(request):

    iscrizioni= Iscrizione.objects.filter(user=request.user)
    return render(request, 'corsi/privata.html', {'iscrizioni':iscrizioni})

@login_required(login_url='/login/')
def appelli(request, corso_id):
    corsi = Corso.objects.filter( pk=corso_id)
    fasca = Corso.objects.get( pk=corso_id)

    appello=[
    list(Iscrizione.objects.filter(corso1_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso2_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso3_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso4_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso5_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso6_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso7_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso8_id=fasca).values_list('user__username', flat=True)),
    list(Iscrizione.objects.filter(corso9_id=fasca).values_list('user__username', flat=True)),
    ]



    return render(request, 'corsi/appello.html', {'appello':appello})


@login_required(login_url='/login/')
def edit_iscrizioni(request, corso_id):
    corsi = Corso.objects.filter( pk=corso_id)
    fasca = Corso.objects.get( pk=corso_id)
    tabella= Iscrizione.objects.filter(user=request.user)
    iscrizione=get_object_or_404(Iscrizione, pk=tabella)
    classe_max= fasca.aule.max_iscritti
    singoli=request.GET.get("f")


    if fasca.progressivo:
        tabellagrafica=[fasca.f1, fasca.f2, fasca.f3, fasca.f4, fasca.f5, fasca.f6, fasca.f7, fasca.f8, fasca.f9]
    else:
        tabellagrafica= singoli


    contatore1= Iscrizione.objects.filter(corso1_id=fasca)
    contatore2= Iscrizione.objects.filter(corso2_id=fasca)
    contatore3= Iscrizione.objects.filter(corso3_id=fasca)
    contatore4= Iscrizione.objects.filter(corso4_id=fasca)
    contatore5= Iscrizione.objects.filter(corso5_id=fasca)
    contatore6= Iscrizione.objects.filter(corso6_id=fasca)
    contatore7= Iscrizione.objects.filter(corso7_id=fasca)
    contatore8= Iscrizione.objects.filter(corso8_id=fasca)
    contatore9= Iscrizione.objects.filter(corso9_id=fasca)

    contatore = eval('contatore'+str(singoli[1])+'.count()')

    if contatore>=classe_max:
        messages.error(request, 'Corso pieno!')
        return redirect('/filtro_fasce/?f='+singoli)
    else:


        if request.method == "POST":
            form = IscrizioneForm(request.POST, instance= iscrizione)


            if form.is_valid():
                iscrizione = form.save(commit=False)
                iscrizione.user = request.user
                iscrizione.published_date = timezone.now()
                if fasca.progressivo:

                    if contatore<classe_max:

                        for f in range(1, 10):
                            fasciaf = eval('fasca.f'+str(f))
                            idiscrizione = eval('iscrizione.corso{0}_id'.format(f))

                            if  (fasciaf != None) and (idiscrizione != None):
                                return redirect('errorefasciapiena')
                        '''
                        if fasca.f1 and iscrizione.corso1_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f2 and iscrizione.corso2_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f3 and iscrizione.corso3_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f4 and iscrizione.corso4_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f5 and iscrizione.corso5_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f6 and iscrizione.corso6_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f7 and iscrizione.corso7_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f8 and iscrizione.corso8_id != None:
                            return redirect('errorefasciapiena')

                        if fasca.f9 and iscrizione.corso9_id != None:
                            return redirect('errorefasciapiena')
                        '''



                        if fasca.f1 and iscrizione.corso1_id== None:
                            iscrizione.corso1 = fasca
                        if fasca.f2 and iscrizione.corso2_id== None:
                            iscrizione.corso2 = fasca
                        if fasca.f3 and iscrizione.corso3_id== None:
                            iscrizione.corso3= fasca
                        if fasca.f4 and iscrizione.corso4_id== None:
                            iscrizione.corso4= fasca
                        if fasca.f5 and iscrizione.corso5_id== None:
                            iscrizione.corso5= fasca
                        if fasca.f6 and iscrizione.corso6_id== None:
                            iscrizione.corso6= fasca
                        if fasca.f7 and iscrizione.corso7_id== None:
                            iscrizione.corso7= fasca
                        if fasca.f8 and iscrizione.corso8_id== None:
                            iscrizione.corso8= fasca
                        if fasca.f9 and iscrizione.corso9_id== None:
                            iscrizione.corso9= fasca
                    else:
                        return redirect('errore')


                else:
                    if contatore<classe_max:
                        if fasca.f1 and singoli=='f1' and iscrizione.corso1_id == None:
                            iscrizione.corso1_id = fasca
                        elif fasca.f2 and singoli=='f2' and iscrizione.corso2_id == None:
                            iscrizione.corso2_id = fasca
                        elif fasca.f3 and singoli=='f3' and iscrizione.corso3_id == None:
                            iscrizione.corso3_id= fasca
                        elif fasca.f4 and singoli=='f4' and iscrizione.corso4_id == None:
                            iscrizione.corso4_id= fasca
                        elif fasca.f5 and singoli=='f5' and iscrizione.corso5_id == None:
                            iscrizione.corso5_id= fasca
                        elif fasca.f6 and singoli=='f6' and iscrizione.corso6_id == None:
                            iscrizione.corso6_id= fasca
                        elif fasca.f7 and singoli=='f7' and iscrizione.corso7_id == None:
                            iscrizione.corso7_id= fasca
                        elif fasca.f8 and singoli=='f8' and iscrizione.corso8_id == None:
                            iscrizione.corso8_id= fasca
                        elif fasca.f9 and singoli=='f9' and iscrizione.corso9_id == None:
                            iscrizione.corso9_id= fasca
                    else:
                        return redirect('errore')


            iscrizione.save()
            return redirect('privata')

        else:
            form = IscrizioneForm(instance= iscrizione)


        return render(request, 'corsi/edit.html', {'form':form, 'corsi':corsi, 'contatore':contatore, 'tabellagrafica':tabellagrafica, 'iscrizione':iscrizione})



@login_required(login_url='/login/')
def filtro_fasce(request):

    pieno="0"
    corsi=request.GET.get("f")
    form = CercaCorsi(request.GET)
    cerca = request.GET.get("q")

    if corsi in ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9']:
        meta = str(corsi)
        corsi= eval('Corso.objects.filter('+meta+'=True).order_by("titolo")')
        fascia = corsi
    return render(request, 'corsi/filtro_fasce.html', {'corsi' : corsi, 'fascia': fascia, 'form':form})


    # if form.is_valid():
    #     if fascia== 'f1':
    #         corsi = Corso.objects.filter(Q(titolo__icontains=cerca)|
    #         Q(descrizione__icontains=cerca))


@login_required(login_url='/login/')
def elimina(request, corso_id):

    corsi = Corso.objects.filter( pk=corso_id)
    fasca = Corso.objects.get( pk=corso_id)
    tabella= Iscrizione.objects.filter(user=request.user)
    iscrizione=get_object_or_404(Iscrizione, pk=tabella)
    classe_max= fasca.aule.max_iscritti
    singoli=request.GET.get("f")

    if request.method == "POST":
        form = IscrizioneForm(request.POST, instance= iscrizione)


        if form.is_valid():
            iscrizione = form.save(commit=False)
            iscrizione.user = request.user
            iscrizione.published_date = timezone.now()
            if fasca.progressivo:

                if fasca.f1:
                    iscrizione.corso1_id = ''
                if fasca.f2:
                    iscrizione.corso2_id = ''
                if fasca.f3:
                    iscrizione.corso3_id= ''
                if fasca.f4:
                    iscrizione.corso4_id= ''
                if fasca.f5:
                    iscrizione.corso5_id= ''
                if fasca.f6:
                    iscrizione.corso6_id= ''
                if fasca.f7:
                    iscrizione.corso7_id= ''
                if fasca.f8:
                    iscrizione.corso8_id= ''
                if fasca.f9:
                    iscrizione.corso9_id= ''
            else:

                if fasca.f1 and singoli=='f1':
                    iscrizione.corso1_id = ''
                elif fasca.f2 and singoli=='f2':
                    iscrizione.corso2_id = ''
                elif fasca.f3 and singoli=='f3':
                    iscrizione.corso3_id= ''
                elif fasca.f4 and singoli=='f4':
                    iscrizione.corso4_id= ''
                elif fasca.f5 and singoli=='f5':
                    iscrizione.corso5_id= ''
                elif fasca.f6 and singoli=='f6':
                    iscrizione.corso6_id= ''
                elif fasca.f7 and singoli=='f7':
                    iscrizione.corso7_id= ''
                elif fasca.f8 and singoli=='f8':
                    iscrizione.corso8_id= ''
                elif fasca.f9 and singoli=='f9':
                    iscrizione.corso9_id= ''
                else:
                    return redirect('privata')


        iscrizione.save()
        return redirect('privata')

    else:
        form = IscrizioneForm(instance= iscrizione)

    return render(request, 'corsi/elimina.html', {'form':form, 'corsi':corsi})


def help(request):
    if request.method == "POST":
        form = Mail(request.POST)
        if form.is_valid():
            subject, from_email, to = form.cleaned_data['mail'], 'settimanaflessibile@gmail.com', 'settimanaflessibile@gmail.com'
            text_content = '456'
            html_content =  form.cleaned_data['testo']
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            return redirect('successo')
    else:
        form = Mail()
    return render(request, 'corsi/help.html', {'form': form})
