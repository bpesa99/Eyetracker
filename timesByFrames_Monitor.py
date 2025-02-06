from psychopy import visual, core, event
import serial
import time
import pylab
from psychopy.visual import ShapeStim

port = serial.Serial('COM4',115200) # Mit dem Arduino verbinden
print("Mit dem Arduino verbunden.")
time.sleep(1)
pmes1 = [] #Differenz von Grafikkarte und Monitor
pmes2 = [] #Differenz von Programm zu Grafikkarte

nIntervals = 500

print("Start der Kalibrierung.")
win = visual.Window(fullscr=True, waitBlanking=True, screen=0)
Vert = [[(-0.2,-0.2),(-0.2,0.2),(0.2,0.2),(0.2,-0.2)]] #Größe des Rechtecks, +/- 1 ist der höchste Wert
myStim1 = ShapeStim(win, vertices=Vert, fillColor='black')
myStim2 = ShapeStim(win, vertices=Vert, fillColor='white')

for frameN in range(300):
    myStim1.draw()
    if event.getKeys():
        break
    win.flip() #Wartet auf die Grafikkarte für das nächste Bild
    
print("Kalibrierung abgeschlossen.")

wait = 0
while wait == 0:
    wait = int(port.readline().decode().strip()) #Arduino ist für den Test bereit.

print("Start des Tests.")

oldbild=1
for frameN in range(nIntervals):
    if (frameN//10) % 2 != 0:
        myStim1.draw()
        bild=1
    else:
        myStim2.draw()
        bild=2
    if event.getKeys():
        break
    if bild != oldbild:
        t1=time.perf_counter_ns() #Start des Bildwechsels vom Programm
    win.flip()
    hatread=0 
    if bild != oldbild:
        t2=time.perf_counter_ns() #Die Grakikkarte hat den Bildwechsel verarbeitet
        x=0
        while (port.inWaiting() == 0 and (time.perf_counter()-t2)<0.03):
            x = x + 1
        t3=time.perf_counter_ns() #Der Bildwechsel wurde vom Arduino detektiert
    while port.inWaiting() > 0:
        port.read() #Filler, damit die Schleife funktioniert
        hatread=1
    if bild != oldbild:
        pmes1.append((t3-t2)/1000000)
        pmes2.append((t2-t1)/1000000)
        print(hatread) #wenn 0, dann wurde das Bild nicht erkannt
    oldbild = bild
port.close()
win.close()

abw = pylab.std(pmes1)

pylab.figure(figsize=[15, 11])
pylab.subplot(3, 2, 1)
pylab.plot(pmes1, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title("Zeitdauer zwischen PsychoPy und Monitor")

print(abw)

pylab.subplot(3, 2, 2)
pylab.hist(pmes1, 5, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('N frames')
pylab.title("Histogramm der Zeitdauer zwischen PsychoPy und Monitor")

pylab.subplot(3, 2, 5)
pylab.plot(pmes2, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title("Zeitdauer zwischen PsychoPy und Grafikkarte")

pylab.subplot(3, 2, 6)
pylab.hist(pmes2, 50, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('N frames')
pylab.title("Histogramm der Zeitdauer zwischen PsychoPy und Grafikkarte")

pylab.subplot(3,2,3)
if abw < 2:
    pylab.text(0.7,0.5,"Die Messergbnisse sind gut!",fontsize=20,color='green')
elif abw >= 2 and abw < 2.6:
    pylab.text(0.7,0.5,"Die Messergebnisse sind akzeptabel!",fontsize=20,color='yellow')
elif abw >= 2.6:
    pylab.text(0.7,0.6,"Die Messergbnisse sind inakzeptabel!",fontsize=20,color='red',va='center')
    pylab.text(0.7,0.4,"Kontrolle der Diagramme notwendig!",fontsize=20,color='red',va='center')
pylab.axis('off')
pylab.show()
    
core.quit()