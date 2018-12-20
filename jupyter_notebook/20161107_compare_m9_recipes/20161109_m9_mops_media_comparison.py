#!/usr/bin/env python3

import sys, os, tango
import matplotlib.pyplot as plt
from parse_epc import parse_epc
from pprint import pprint

trajectories, times = parse_epc('20161109_m9_mops_media_comparison.epc')

if os.fork():
    raise SystemExit

if sys.argv[1] == 'M9':
    plt.plot(times, trajectories[1,3], color=tango.red[1], label='M9,on,apo')
    plt.plot(times, trajectories[1,4], color=tango.red[2], label='M9,on,holo')
    plt.plot(times, trajectories[2,3], color=tango.blue[1], label='M9,off,apo')
    plt.plot(times, trajectories[2,4], color=tango.blue[2], label='M9,off,holo')

elif sys.argv[1] == 'MOPS':
    plt.plot(times, trajectories[1,5], color=tango.red[1], label='MOPS,on,apo')
    plt.plot(times, trajectories[1,6], color=tango.red[2], label='MOPS,on,holo')
    plt.plot(times, trajectories[2,5], color=tango.blue[1], label='MOPS,off,apo')
    plt.plot(times, trajectories[2,6], color=tango.blue[2], label='MOPS,off,holo')

elif sys.argv[1] == 'EZ':
    plt.plot(times, trajectories[1,7], color=tango.red[1], label='EZ,on,apo')
    plt.plot(times, trajectories[1,8], color=tango.red[2], label='EZ,on,holo')
    plt.plot(times, trajectories[2,7], color=tango.blue[1], label='EZ,off,apo')
    plt.plot(times, trajectories[2,8], color=tango.blue[2], label='EZ,off,holo')

elif sys.argv[1] == 'on':
    plt.plot(times, trajectories[3,3], color=tango.red[2], label='M9,on,apo')
    plt.plot(times, trajectories[3,4], color=tango.green[2], label='MOPS,on,apo')
    plt.plot(times, trajectories[3,5], color=tango.blue[2], label='EZ,on,apo')
    plt.plot(times, trajectories[4,3], color=tango.red[0], label='M9,on,holo')
    plt.plot(times, trajectories[4,4], color=tango.green[0], label='MOPS,on,holo')
    plt.plot(times, trajectories[4,5], color=tango.blue[0], label='EZ,on,holo')

elif sys.argv[1] == 'off':
    plt.plot(times, trajectories[3,6], color=tango.red[2], label='M9,off,apo')
    plt.plot(times, trajectories[4,6], color=tango.red[0], label='M9,off,holo')
    plt.plot(times, trajectories[3,7], color=tango.green[2], label='MOPS,off,apo')
    plt.plot(times, trajectories[4,7], color=tango.green[0], label='MOPS,off,holo')
    plt.plot(times, trajectories[3,8], color=tango.blue[2], label='EZ,off,apo')
    plt.plot(times, trajectories[4,8], color=tango.blue[0], label='EZ,off,holo')

elif sys.argv[1] == 'apo':
    plt.plot(times, trajectories[5,3], color=tango.red[2], label='M9,on,apo')
    plt.plot(times, trajectories[6,3], color=tango.red[0], label='M9,off,apo')
    plt.plot(times, trajectories[5,4], color=tango.green[2], label='MOPS,on,apo')
    plt.plot(times, trajectories[6,4], color=tango.green[0], label='MOPS,off,apo')
    plt.plot(times, trajectories[5,5], color=tango.blue[2], label='EZ,on,apo')
    plt.plot(times, trajectories[6,5], color=tango.blue[0], label='EZ,off,apo')

elif sys.argv[1] == 'holo':
    plt.plot(times, trajectories[5,6], color=tango.red[2], label='M9,on,holo')
    plt.plot(times, trajectories[6,6], color=tango.red[0], label='M9,off,holo')
    plt.plot(times, trajectories[5,7], color=tango.green[2], label='MOPS,on,holo')
    plt.plot(times, trajectories[6,7], color=tango.green[0], label='MOPS,off,holo')
    plt.plot(times, trajectories[5,8], color=tango.blue[2], label='EZ,on,holo')
    plt.plot(times, trajectories[6,8], color=tango.blue[0], label='EZ,off,holo')

elif sys.argv[1] == 'M9,on,apo':
    plt.plot(times, trajectories[1,3], color=tango.red[1], label='M9,on,apo')
    plt.plot(times, trajectories[3,3], color=tango.red[1], label='M9,on,apo')
    plt.plot(times, trajectories[5,3], color=tango.red[1], label='M9,on,apo')

elif sys.argv[1] == 'M9,off,apo':
    plt.plot(times, trajectories[2,3], color=tango.red[1], label='M9,off,apo')
    plt.plot(times, trajectories[3,6], color=tango.red[1], label='M9,off,apo')
    plt.plot(times, trajectories[6,3], color=tango.red[1], label='M9,off,apo')

elif sys.argv[1] == 'MOPS,on,apo':
    plt.plot(times, trajectories[1,5], color=tango.red[1], label='MOPS,on,apo')
    plt.plot(times, trajectories[3,4], color=tango.red[1], label='MOPS,on,apo')
    plt.plot(times, trajectories[5,4], color=tango.red[1], label='MOPS,on,apo')

elif sys.argv[1] == 'MOPS,off,apo':
    plt.plot(times, trajectories[2,5], color=tango.red[1], label='MOPS,off,apo')
    plt.plot(times, trajectories[3,7], color=tango.red[1], label='MOPS,off,apo')
    plt.plot(times, trajectories[6,4], color=tango.red[1], label='MOPS,off,apo')

elif sys.argv[1] == 'EZ,on,apo':
    plt.plot(times, trajectories[1,7], color=tango.red[1], label='EZ,on,apo')
    plt.plot(times, trajectories[3,5], color=tango.red[1], label='EZ,on,apo')
    plt.plot(times, trajectories[5,5], color=tango.red[1], label='EZ,on,apo')

elif sys.argv[1] == 'EZ,off,apo':
    plt.plot(times, trajectories[2,7], color=tango.red[1], label='EZ,off,apo')
    plt.plot(times, trajectories[3,8], color=tango.red[1], label='EZ,off,apo')
    plt.plot(times, trajectories[6,5], color=tango.red[1], label='EZ,off,apo')

plt.xlabel('hours')
plt.ylabel('OD600')
plt.xlim(min(times), max(times))
plt.legend(loc='best')
plt.show()
