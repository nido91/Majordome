import subprocess
from datetime import date
from datetime import timedelta

#recuperation date du jour
date_jour = date.today()

aujourdhui = date_jour + timedelta(days=0)

#extraction numero du jour
numero_jour = str(aujourdhui.day)

# # take and store photos during xx sec
cde = "delcapture" + " " + numero_jour
subprocess.call(cde, shell=True)
