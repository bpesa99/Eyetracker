from psychopy import visual, logging, core, event
import serial
import time
import pylab
from psychopy.visual import ShapeStim

visual.useFBO = True

port = serial.Serial('COM4',115200) # Mit dem Arduino verbinden
time.sleep(1)
pmes = [] #Werte vom Arduino

wait = 0
while wait == 0:
    wait = int(port.readline().decode().strip()) # Wartet auf den Arduino

nIntervals = 500 # nIntervals/50 Bilder werden angezeigt
win = visual.Window([1920, 1080], fullscr=False, allowGUI=False, waitBlanking=True)
Vert = [[(-.9,-.9),(-.9,.9),(.9,.9),(.9,-.9)]]
myStim1 = ShapeStim(win, vertices=Vert, fillColor='black', lineWidth=0, size=1) # schwarzes Rechteck
myStim2 = ShapeStim(win, vertices=Vert, fillColor='white', lineWidth=0, size=1) # weißes Rechteck

win.recordFrameIntervals = True
for frameN in range(nIntervals):
    if (frameN//50) % 2 != 0:
        myStim1.draw()
    else:
        myStim2.draw()
    if event.getKeys():
        break
    win.logOnFlip(msg='frame=%i' %frameN, level=logging.EXP)
    win.flip()
    while port.inWaiting() > 0:
        pmes.append(float(int(port.readline().decode().strip())/1000)) # auslesen der vom Arduino gemessenen Zeit
port.close()
win.close()

# Berechnen der Zeitdifferenz zwischen Grafikkarte und Monitor
intervals = pylab.array(win.frameIntervals) * 1000
intervalsMS = []
for i in range(len(pmes)):
    if i == 0:
        intervalsMS.append(pmes[i])
    else:
        intervalsMS.append(pmes[i] - intervals[i])
m = pylab.mean(intervalsMS)
sd = pylab.std(intervalsMS)

msg = "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f"
distString = msg % (m, sd, m - 2.58 * sd, m + 2.58 * sd)
nTotal = len(intervalsMS)
nDropped = sum(intervalsMS > (1.5 * m))
msg = "Frames = %i"
droppedString = msg % (nTotal)

pylab.figure(figsize=[12, 8])
pylab.subplot(1, 2, 1)
pylab.plot(intervalsMS, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title(droppedString)

pylab.subplot(1, 2, 2)
pylab.hist(intervalsMS, 50, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('n frames')
pylab.title(distString)
pylab.show()

win.close()
core.quit()