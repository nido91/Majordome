
import os
import subprocess

f = os.popen ('date')
strdate= f.read()
listdate = strdate.split()
day = listdate[1]

cde = "PHOTODAY"+ " " + day
subprocess.call (cde, shell=True)
