# Majordome
mise à jour de l'avatar
Dimanche 03/04/2016 process pour appliquer la fonction crontab afin d'effacer les images
1. pi§ sudo crontab -e    "ouvre en édition le fichier crontab avec les droits admin 
2. aller en fin de fichier et taper 0 0 * * * rm -R /home/pi/Jean/Majordome_V01R01/MJDcontrol/capture/*.jpg
"0mn 0h *jour *mois *semaine suivi de la cde  rm -R efface récursivement tous les .jpg
"pour essayer nous pourrons agir que sur le 1er terme et faire cp au lieu de rm
"je propose de faire un tar -[args] des .jpg puis de les stocker sur disque dur brancher sur la box
 
