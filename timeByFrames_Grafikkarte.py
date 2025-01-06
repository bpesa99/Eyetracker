from psychopy import visual, logging, core, event
visual.useFBO = True

import matplotlib
import pylab
import sys
from psychopy.visual import ShapeStim

nIntervals = 500 # nIntervals/50 Bilder werden angezeigt
win = visual.Window([1920, 1080], fullscr=True, allowGUI=False, waitBlanking=True)
    
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
win.close()

intervalsMS = pylab.array(win.frameIntervals) * 1000 # Zeiten der Bildwechsel in ms
m = pylab.mean(intervalsMS) # Mittelwert
sd = pylab.std(intervalsMS) # Standardabweichung

msg = "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f"
distString = msg % (m, sd, m - 2.58 * sd, m + 2.58 * sd)
nTotal = len(intervalsMS)
nDropped = sum(intervalsMS > (1.5 * m))
msg = "Dropped/Frames = %i/%i = %.3f%%"
droppedString = msg % (nDropped, nTotal, 100 * nDropped / float(nTotal))

# Zeitintervale werden geplottet
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
