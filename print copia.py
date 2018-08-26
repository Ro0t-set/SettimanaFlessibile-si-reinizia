#!/usr/bin/env python
import os
import sys

if name == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    
    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)

import math
import string
from django.contrib.auth.models import User
from app.models import Iscrizione
from app.models import Corso
from django.shortcuts import get_object_or_404


r=0
riga = 0
while riga < 400:
    riga = riga + 1
    try:
      corsi= Corso.objects.get(id= riga)
      f1=("Mar 3-4", (list(Iscrizione.objects.filter(corso1_id=corsi.id).values_list('user__username', flat=True))))
      iscritti= (Iscrizione.objects.filter(corso1_id=corsi.id))
      counter= iscritti.count()
      if counter != 0:
        r= r+1
        print(r,corsi)
        print(f1)
        print("_________________________________________________________________________________")

                   
                   
                   
    except:
      pass
