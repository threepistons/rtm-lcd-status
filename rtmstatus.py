#!/usr/bin/python

import sys
import signal
import webbrowser
from rtmapi import Rtm
from rtmstatusconf import Rtmsettings
import time
from lcdbackpack import LcdBackpack

class Taskcounter:
    # This class gets an integer number of tasks out of RTM, according to the supplied filter.
    # e.g.
    #    moo = Taskcounter('status:incomplete')
    #    print str(moo.count) # gives number of open tasks

    def __init__(self, myfilter):
        self.myfilter = myfilter
        count = 0
        result = api.rtm.tasks.getList(filter=self.myfilter)
        for tasklist in result.tasks:
            for taskseries in tasklist:
                count += 1
        self.count = count
        
def setbacklight(status):
    display.set_backlight_rgb(settings.colours[status][0],settings.colours[status][1],settings.colours[status][2])
        
def quitter(signal, frame):
    print('Quitting...')
    display.display_off()
    display.clear()
    display.disconnect()
    sys.exit(0)

if __name__ == '__main__':
    
    display = LcdBackpack('/dev/ttyACM0', 115200)
    signal.signal(signal.SIGINT, quitter)
    
    # put the api token and secret in the credentials file (chmod 600)
    # get those parameters from http://www.rememberthemilk.com/services/api/keys.rtm

    debug = True if (len(sys.argv) > 1 and sys.argv[1] == 'debug') else False
    colourtest = True if (len(sys.argv) > 1 and sys.argv[1] == 'colourtest') else False

    settings = Rtmsettings()
    api = Rtm(settings.main['api_key'], settings.main['shared_secret'], 'read', settings.main['token'])

    # authentication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
    # check for valid token
    if not api.token_valid():
        # use desktop-type authentication
        url, frob = api.authenticate_desktop()
        # open webbrowser, wait until user authorized application
        webbrowser.open(url)
        raw_input("Continue?")
        # get the token for the frob
        api.retrieve_token(frob)
        # print out new token, should be used to initialize the Rtm object next time
        # Put the new token in the credentials file by hand for now.
        print "New token: %s" % api.token

    display.connect()
    display.display_on()
    
    print('Press Ctrl+C to quit')
    
    while True:
        o = Taskcounter(settings.filters['overdue'])
        oi = Taskcounter(settings.filters['overdue_important'])
        s = Taskcounter(settings.filters['soon'])
        si = Taskcounter(settings.filters['soon_important'])
        
        display.clear()

        display.write("O'due: " + str(o.count) + ' Imp: ' + str(oi.count))
        display.set_cursor_position(1,2)
        display.write("Soon: " + str(s.count) + ' Imp: ' + str(si.count))

        if (oi.count > 0):
            setbacklight('overdue_important')
        elif (si.count > 0):
            setbacklight('soon_important')
        elif (o.count > 0):
            setbacklight('overdue')
        elif (s.count > 0):
            setbacklight('soon')
        else:
            setbacklight('no_tasks')

        if debug == True:
           print settings.filters['overdue'] + ': ' + str(o.count)
           print settings.filters['overdue_important'] + ': ' + str(oi.count)
           print settings.filters['soon'] + ': ' + str(s.count)
           print settings.filters['soon_important'] + ': ' + str(si.count)

        time.sleep(settings.main['polling_delay'])

