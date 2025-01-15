from psychopy import visual, logging, core, event
import serial
import time
import pylab
from psychopy.visual import ShapeStim
visual.useFBO = True

port = serial.Serial('COM4',115200) # Mit dem Arduino verbinden
print("Mit dem Arduino verbunden.")
time.sleep(1)
pmes1 = [] #Differenz von Grafikkarte und Monitor
intervalsMS = []

nIntervals = 500

print("Start der Kalibrierung.")
win = visual.Window([1920, 1080], fullscr=True, allowGUI=False, waitBlanking=True)
Vert = [[(-0.5,-0.5),(-0.5,0.5),(0.5,0.5),(0.5,-0.5)]] #Größe des Rechtecks, +/- 1 ist der höchste Wert
myStim1 = ShapeStim(win, vertices=Vert, fillColor='black', lineWidth=0, size=1)
for frameN in range(300):
    myStim1.draw()
    if event.getKeys():
        break
    win.flip() #Wartet auf die Grafikkarte für das nächste Bild
win.close()
print("Kalibrierung abgeschlossen.")

wait = 0
while wait == 0:
    wait = int(port.readline().decode().strip()) #Arduino ist für den Test bereit.

print("Start des Tests.")

win2 = visual.Window([1920, 1080], fullscr=True, allowGUI=False, waitBlanking=True)
Vert = [[(-.9,-.9),(-.9,.9),(.9,.9),(.9,-.9)]]
myStim2 = ShapeStim(win2, vertices=Vert, fillColor='black', lineWidth=0, size=1)
myStim3 = ShapeStim(win2, vertices=Vert, fillColor='white', lineWidth=0, size=1)

win2.recordFrameIntervals = True #Zeichnet die Zeiten der Bildwechsel abhängig von de Grafikkarte auf (win.flip())
oldbild=2 
for frameN in range(nIntervals):
    if (frameN//10) % 2 != 0:
        myStim2.draw()
        bild=1
    else:
        myStim3.draw()
        bild=2
    if event.getKeys():
        break
    win2.logOnFlip(msg='frame=%i' %frameN, level=logging.EXP)
    if bild != oldbild:
        t1=time.perf_counter_ns()
    win2.flip()
    hatread=0 
    if bild != oldbild:
        t2=time.perf_counter_ns()
        x=0
        while (port.inWaiting() == 0 and (time.perf_counter()-t2)<0.03):
            x = x + 1
        t3=time.perf_counter_ns()
    while port.inWaiting() > 0:
        port.read()
        hatread=1
    if bild != oldbild:
        intervalsMS.append((t2-t1)/1000000) #Zeitdauer der Grafikkarte zum Prozessieren des Bildes
        pmes1.append((t3-t2)/1000000) #Zeitdifferenz zwischen Grafikkarte und Monitor
        print((t3-t2)/1000000) 
        print((t2-t1)/1000000) 
        print(hatread) #wenn 0, dann wurde das Bild nicht erkannt
    oldbild = bild
port.close()
win2.close()

pylab.figure(figsize=[15, 10])
m = pylab.mean(pmes1)
abw = pylab.std(pmes1)


pylab.subplot(3, 2, 1)
pylab.plot(pmes1, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title("Zeitdifferenz von Grafikkarte zu Monitor")
if abw < 2.4:
    pylab.text(58,-20,"Die Messergbnisse sind valide!",fontsize=20,color='green', ha='center', va='center')
elif abw >= 2.4:
    pylab.text(58,-20,"Die Messergbnisse sind nicht valide!",fontsize=23,color='red', ha='center', va='center')
    pylab.text(58,-25,"Kontrolle des Histogramms der Zeitdifferenz von Grafikkarte zu Monitor notwendig!",fontsize=23,color='red', ha='center', va='center')
print(abw)
pylab.subplot(3, 2, 2)
pylab.hist(pmes1, 50, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('n frames')
pylab.title("Histogramm der Zeitdifferenz von Grafikkarte zu Monitor")


pylab.subplot(3, 2, 5)
pylab.plot(intervalsMS, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title("Zeitdauer der Grafikkarte zum Prozessieren des Bildes")

pylab.subplot(3, 2, 6)
pylab.hist(intervalsMS, 50, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('n frames')
pylab.title("Histogramm der Zeitdauer der Grafikkarte zum Prozessieren des Bildes")
pylab.show()
    


core.quit()