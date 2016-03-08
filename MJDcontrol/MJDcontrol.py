#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import subprocess
import socket
import RPi.GPIO as GPIO
import time
import logging
import threading
import picamera
import datetime

host = ''
port = 12800


def updateeventintrusion ():
        global eventintrusionportail
        global eventintrusiongarage

        if (eventintrusiongarage or eventintrusionportail):

                #xx Debug
                #print "updateeventintrusion: eventintrusion.set()"

                eventintrusion.set()
        else:
                #xx Debug
                #print "updateeventintrusion: eventintrusion.clear()"

                eventintrusion.clear()


def SendIntrusionPortail():
	hote = "localhost"
	port = 12800

	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion_avec_serveur.connect((hote, port))

	msg_a_envoyer = "IntrusionPortail".encode()

	# Send message
	connexion_avec_serveur.send(msg_a_envoyer)

	# Wait result from serveur
	msg_recu = connexion_avec_serveur.recv(1024)
	#print(msg_recu.decode())



	# close connexion
	connexion_avec_serveur.send("fin".encode())


	connexion_avec_serveur.close ()


#!!Threaded!!#
def intrusionportailCheck ():
    while eventCamera.wait() :
            f = os.popen ('RFSniff')
            received = f.read()
            logging.info('reception radio')

            if (received[9:17] == "14467100"):
                    SendIntrusionPortail()
            time.sleep (1)



#!!Threaded!!#
def intrusiongarageCheck ():

        global eventintrusiongarage

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(22, GPIO.IN)


        while eventCamera.wait():
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(22, GPIO.IN)
                ButtonOFF = GPIO.input(22)

                #xx Debug
                #ButtonOFF = True
                #xx

                if ButtonOFF:
                        eventintrusiongarage = False

                else:
                        eventintrusiongarage = True
                        #xx print "intrusiongarageCheck: eventintrusiongarage = True"

                updateeventintrusion ()
                time.sleep (1)



#!!Threaded!!#

def camera():

        global eventintrusionportail

        while (eventCamera.wait() and eventintrusion.wait()):
                #xx Debug
                #print "camera: capture"

                captureintrusionportail = False
                if eventintrusionportail:
                        captureintrusionportail = True

                capture ()

                if captureintrusionportail:
                        eventintrusionportail = False
                updateeventintrusion ()


def capture ():
        #xx Debug
        #print "capture"
        logging.info('capture')

        # find today day number
        i = datetime.datetime.now()
        day = str (i.day)

	# take and store photos during xx sec

        cde = "PHOTODAY"+ " " + day
        logging.info(cde)
        subprocess.call (cde, shell=True)




#!!Threaded!!#
def SendAlert():

	while (eventCamera.wait() and eventintrusion.wait()):
			eventintrusion.wait()
			logging.info("INTRUSION")
			time.sleep (10)




def StartThreadcamera():
	Threadcamera = threading.Thread (target= camera, name= 'camera')
	Threadcamera.start ()

def StartThreadintrusiongarageCheck ():
	ThreadintrusiongarageCheck = threading.Thread (target= intrusiongarageCheck, name= 'intrusiongarageCheck')
	ThreadintrusiongarageCheck.start ()

def StartThreadintrusionportailCheck ():
	ThreadintrusionportailCheck = threading.Thread (target= intrusionportailCheck, name= 'intrusionportailCheck')
	ThreadintrusionportailCheck.start ()

def StartThreadSendAlert ():
	ThreadSendAlert = threading.Thread (target= SendAlert, name= 'SendAlert')
	ThreadSendAlert.start ()

##############################
#function: IntrusionPortail
#
#


def IntrusionPortail(Id_ClientConnection, received_msg):
        global eventintrusionportail

        #xx Debug
        #print "Intrusion Portail"

        logging.info(received_msg.decode())
        eventintrusionportail = True
        updateeventintrusion ()

        Id_ClientConnection.send(b"OK")
        received_msg = Id_ClientConnection.recv(1024)
        if received_msg != b"fin":
                logging.info("error received_msg NOK")
        #logging.info("End of connection")
        Id_ClientConnection.close()


##############################
#function: StartCamera
#
#

def StartCamera(Id_ClientConnection, received_msg):

        global IsCameraRunning

        logging.info(received_msg.decode())
        eventCamera.set()

        IsCameraRunning = True
        Id_ClientConnection.send(b"OK")
        received_msg = Id_ClientConnection.recv(1024)
        if received_msg != b"fin":
                logging.info("error received_msg NOK")
        #logging.info("End of connection")
        Id_ClientConnection.close()



##############################
#function: StopCamera
#
#

def StopCamera(Id_ClientConnection, received_msg):

        global IsCameraRunning

        eventCamera.clear()
        logging.info(received_msg.decode())
        IsCameraRunning = False
        Id_ClientConnection.send(b"OK")
        received_msg = Id_ClientConnection.recv(1024)
        if received_msg != b"fin":
                logging.info("error received_msg NOK")
        #logging.info("End of connection")
        Id_ClientConnection.close()


##############################
#function: IsCameraRunning
#
#

def Is_CameraRunning (Id_ClientConnection, received_msg):

        logging.info(received_msg.decode())

        global IsCameraRunning

        if IsCameraRunning:
                Id_ClientConnection.send(b"Running")
        else:
                Id_ClientConnection.send(b"NotRunning")

        received_msg = Id_ClientConnection.recv(1024)
        if received_msg != b"fin":
                logging.info("error received_msg NOK")
        #logging.info("End of connection")
        Id_ClientConnection.close()


#############################
#function: unknownAction
#
#

def unknownAction(Id_ClientConnection, received_msg):
        loop = 1
        while loop:
                logging.info(received_msg.decode())
                logging.info ('unknownAction')

                Id_ClientConnection.send(b"OK")
                received_msg = Id_ClientConnection.recv(1024)
                if received_msg == b"fin":
                        loop = 0
        #logging.info("End of connection")
        Id_ClientConnection.close()


###############################
#Main programme
###############################

#define events
eventCamera = threading.Event() 				# used for starting/stopping the camera
IsCameraRunning = False							# used by the web serveur to change the html view according the camera status
eventAlert = threading.Event()  				# used for starting/stopping the alert sending
eventintrusion = threading.Event()				# used for "global" intrusion signaling
eventintrusiongarage = False					# used for "garage" intrusion signaling
eventintrusionportail = False					# used for "portail" intrusion signaling

#define logging
logging.basicConfig(filename='/home/pi/Majordome/MJDlog/MJDlog.log',level=logging.DEBUG,format='%(asctime)s %(message)s')


# open the main server socket
Id_MainConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Id_MainConnection.bind((host, port))

# Threads launching
StartThreadcamera()
StartThreadSendAlert()
StartThreadintrusiongarageCheck ()
##StartThreadintrusionportailCheck ()

while 1:

        logging.info("The server is listening on port {}".format(port))
        Id_MainConnection.listen(5)

        # open client peer to peer connection
        Id_ClientConnection, infos_connection = Id_MainConnection.accept()
        logging.info('Accept connection with the client')

        #Start action
        received_msg = Id_ClientConnection.recv(1024)
        Action = received_msg
        dictActions = 	{b'StartCamera':StartCamera,
                         b'StopCamera':StopCamera,
                         b'IsCameraRunning':Is_CameraRunning,
						 b'IntrusionPortail':IntrusionPortail,
                        }
        dictActions.get(Action, unknownAction)(Id_ClientConnection, received_msg)





