import socket

hote = "localhost"
#hote = '192.168.1.18'
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))

msg_a_envoyer = "StartCamera".encode()

#print("Envoi du message")
connexion_avec_serveur.send(msg_a_envoyer)

#Wait result from serveur
msg_recu = connexion_avec_serveur.recv(1024)
#print(msg_recu.decode())
#print("Camera OK")
 

#demande fermeture de la connexion par le serveur
connexion_avec_serveur.send("fin".encode())


connexion_avec_serveur.close ()
