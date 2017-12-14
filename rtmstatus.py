#!/usr/bin/python

import sys
import signal
import webbrowser
from rtmapi import Rtm
import ConfigParser
import time
from lcdbackpack import LcdBackpack

def taskcounter (myfilter):
    count = 0
    result = api.rtm.tasks.getList(filter=myfilter)
    for tasklist in result.tasks:
        for taskseries in tasklist:
            count += 1
    return(count)
        
def setbacklight(colour):
    rgb = colour.split(',')
    display.set_backlight_rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]))
        
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

    config = ConfigParser.SafeConfigParser()
    config.readfp(open('rtmstatus.conf'))
    api = Rtm(config.get('main', 'api_key'), config.get('main', 'shared_secret'), 'read', config.get('main', 'token'))

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
        count = {}
        sections = config.sections()
        sections.sort(reverse=True)
        for section in sections:
            if section != 'main':
                count[section] = taskcounter(config.get(section, 'filter'))
        display.clear()
        setbacklight(config.get('main', 'defaultcolour'))
        for section in sections:
            if section != 'main':        
                display.set_cursor_position(int(config.get(section,'x')),int(config.get(section,'y')))
                display.write(config.get(section,'label') + ': ' + str(count[section]))
                if (int(count[section]) > int(config.get(section,'threshold'))):
                    setbacklight(config.get(section, 'colour'))
 

        time.sleep(float(config.get('main','polling_delay')))

