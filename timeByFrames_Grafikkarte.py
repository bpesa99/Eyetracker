#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The most accurate way to time your stimulus presentation is to
present for a certain number of frames. For that to work you need
your window flips to synchronize to the monitor and not to drop
any frames. This script examines the precision of your frame flips.

Shut down as many applications as possible, especially those that
might try to update
"""

from psychopy import visual, logging, core, event
visual.useFBO = True  # if available (try without for comparison)

import matplotlib
import pylab
import sys
from psychopy.visual import ShapeStim

nIntervals = 500
win = visual.Window([1920, 1080], fullscr=True, allowGUI=False, waitBlanking=True)

#myStim = visual.GratingStim(win, tex='sin', mask=None,
    #size=500, sf=0.0001, units='pix', autoLog=False)
    
Vert = [[(-.9,-.9),(-.9,.9),(.9,.9),(.9,-.9)]]
myStim1 = ShapeStim(win, vertices=Vert, fillColor='black', lineWidth=0, size=1)
myStim2 = ShapeStim(win, vertices=Vert, fillColor='white', lineWidth=0, size=1)
# logging.console.setLevel(logging.INFO)# uncomment to log every frame

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
    #time.sleep(0.5)
win.fullscr = False
win.close()

# calculate some values
intervalsMS = pylab.array(win.frameIntervals) * 1000
m = pylab.mean(intervalsMS)
sd = pylab.std(intervalsMS)
# se=sd/pylab.sqrt(len(intervalsMS)) # for CI of the mean

msg = "Mean=%.1fms, s.d.=%.2f, 99%%CI(frame)=%.2f-%.2f"
distString = msg % (m, sd, m - 2.58 * sd, m + 2.58 * sd)
nTotal = len(intervalsMS)
nDropped = sum(intervalsMS > (1.5 * m))
msg = "Dropped/Frames = %i/%i = %.3f%%"
droppedString = msg % (nDropped, nTotal, 100 * nDropped / float(nTotal))

# plot the frameintervals
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

pylab.savetxt("FlipTimes.txt",intervalsMS/10)
win.close()
core.quit()

# The contents of this file are in the public domain.
