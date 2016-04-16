#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from datetime import date
from datetime import timedelta

#recuperation date du jour
date_jour = date.today()
print "aujourd'hui", date_jour

# test au 14/04/2016 soit 45j après 29/02/2016
date_jour = date_jour - timedelta(days=45)
print "29 février", date_jour

demain = date_jour + timedelta(days=1)

#extraction numero du jour
numero_jour = str(demain.day)

# # take and store photos during xx sec
cde = "delcapture" + " " + numero_jour
print "commande", cde