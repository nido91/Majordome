#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from datetime import date
from datetime import timedelta

#recuperation date du jour
date_jour = date.today()

demain = date_jour + timedelta(days=1)

#extraction numero du jour
numero_jour = str(demain.day)

# # take and store photos during xx sec
cde = "delcapture" + " " + numero_jour
subprocess.call(cde, shell=True)
