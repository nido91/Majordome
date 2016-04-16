# Majordome
Evolution faite le 16/04/2016 par nido91
ajout des fonctions delcaptureYesterdays.py, delcaptureTodays.py, delcaptureTomorrows.py et testfevrier.py
ces fonctions permettent de ce positionner dans le répertoire capture(jour-1), capture(jour) et capture(jour+1)
afin d'effacer les .jpg à une heure fixe commandée par crontab

Fonctionnement:
A: mettre les 3 prg dans le répertoire MJDcde
B: en fonction du choix du jour créer une commande : delcaptureTomorrow pour effacement du lendemain par ex
   #!/bin/bash
   cd /home/pi/Majordome/MJDcde
   python delcaptureTomorrow.py
C: la rendre executable $ chmod +x delcaptureTomorrow
D: création d'un lien symbolique
      $ cd /usr/bin
      $ sudo ln -s /home/pi/Majordome/MJDcde/delcaptureTomorrow delcaptureTomorrow
      $ crontab -e
           si éditeur vim se mettre en insertion en tapant i
           aller en fin de texte et taper 0 0 * * *  delcaptureTomorrow  (mn, heure)
           sortir de l'éditeur par Escape puis :wq

Chronologie:
 crontab à minuit execute delcaptureTomorrow qui lance le prg delcaptureTomorrow.py qui lance delcapture(jour)
        
