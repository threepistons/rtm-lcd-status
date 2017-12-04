#!/usr/bin/python

import sys
import signal
import webbrowser
from rtmapi import Rtm
from rtmcreds import Rtmcreds
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
        
def quitter(signal, frame):
    print('Quitting...')
    a.display_off()
    a.clear()
    a.disconnect()
    sys.exit(0)

if __name__ == '__main__':
    
    a = LcdBackpack('/dev/ttyACM0', 115200)
    signal.signal(signal.SIGINT, quitter)
    
    # put the api token and secret in the credentials file (chmod 600)
    # get those parameters from http://www.rememberthemilk.com/services/api/keys.rtm

    debug = True if (len(sys.argv) > 1 and sys.argv[1] == 'debug') else False

    off = True if (len(sys.argv) > 1 and sys.argv[1] == 'off') else False

    creds = Rtmcreds()
    api = Rtm(creds.api_key, creds.shared_secret, "read", creds.token)

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

    # Variable naming:
    # * o = overdue
    # * u  = urgent (needs to be done soon, not the same as important)
    # * i  = important
    # * f  = filter

    incompletef = 'status:incomplete'
    importantf = 'priority:1'

    of = incompletef + ' and dueBefore:now'
    oif = of + ' and ' + importantf
    uf = incompletef + ' and dueWithin:"2 days of now"'
    uif = uf + ' and ' + importantf
    
    a.connect()
    a.display_on()
    a.clear()

    print('Press Ctrl+C to quit')
    
    while True:
        o = Taskcounter(of)
        oi = Taskcounter(oif)
        u = Taskcounter(uf)
        ui = Taskcounter(uif)

        a.write("O'due: " + str(o.count) + ' P1: ' + str(oi.count))
        a.set_cursor_position(1,2)
        a.write("Soon: " + str(u.count) + ' P1: ' + str(ui.count))

        if (oi.count > 0):
            a.set_backlight_rgb(255, 0, 0)
        elif (ui.count > 0):
            a.set_backlight_rgb(255, 30, 0)
        elif (o.count > 0):
            a.set_backlight_rgb(20, 20, 255)
        else:
            a.set_backlight_rgb(0, 255, 0)

        if debug == True:
           print of + ': ' + str(o.count)
           print oif + ': ' + str(oi.count)
           print uf + ': ' + str(u.count)
           print uif + ': ' + str(ui.count)

        time.sleep(300)

# At the moment, the only way to exit is to press CRTL+C, so there is no neat way to turn the LCD off.
# TODO: find out how to make this into a backgroundable daemon that can be controlled with a systemd unit.
