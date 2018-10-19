#!/usr/bin/env python

import sys
import webbrowser
from rtmapi import Rtm
import ConfigParser
import time
from lcdbackpack import LcdBackpack
from daemon import Daemon

def screenoff(display):
    display.display_off()
    display.clear()
    display.disconnect()
    
def taskcounter (self, myfilter, api):
    count = 0
    result = api.rtm.tasks.getList(filter=myfilter)
    for tasklist in result.tasks:
        for taskseries in tasklist:
            count += 1
    return(count)

class MyDaemon(Daemon):

    def run(self):

        # put the api token and secret in the credentials file (chmod 600)
        # get those parameters from http://www.rememberthemilk.com/services/api/keys.rtm

        debug = False

        config = ConfigParser.SafeConfigParser()
        # test for file presence
        # if not there, exit telling user to rename template to file and get api key
        ## TODO: implement previous comment
        config.readfp(open('rtmstatus.conf'))
        # test for config items existing
        if (not config.has_option('main', 'api_key') or not config.has_option('main', 'shared_secret')):
            # without api_key or shared_secret, I cannot do anything, so exit and tell user to get an API key
            print "You need to get a RTM API key and shared secret to use this script."
            # exiting with an error code because the script cannot run
            sys.exit(1)
        # if token isn't there then launch API without it so we can get one and store it, else launch anyway.
        if config.has_option('main','token'):
            api = Rtm(config.get('main', 'api_key'), config.get('main', 'shared_secret'), 'read', config.get('main', 'token'))
        else:
            api = Rtm(config.get('main', 'api_key'), config.get('main', 'shared_secret'), 'read', None)

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
            # If the token turns out to be invalid, we get a valid one and store it.
            config.set('main','token',api.token)
            with open('rtmstatus.conf', 'w') as configfile:
                config.write(configfile) # TODO test that this worked
            # reinitialize the Rtm object
            del api
            api = Rtm(config.get('main', 'api_key'), config.get('main', 'shared_secret'), 'read', config.get('main', 'token'))

        while True:
            backlight = config.get('main', 'defaultcolour')
            count = {}
            sections = config.sections()
            sections.sort(reverse=True)

            for section in sections:

                if section != 'main':

                    count[section] = taskcounter(config.get(section, 'filter'), api)

            display.clear()

            for section in sections:

                if section != 'main':

                    display.set_cursor_position(int(config.get(section,'x')),int(config.get(section,'y')))
                    if int(count[section]) < 10:
                        display.write(config.get(section,'label') + ': ' + str(count[section]))
                    else:
                        display.write(config.get(section,'label') + ':' + str(count[section]))

                    if (int(count[section]) > int(config.get(section,'threshold'))):
                        backlight = config.get(section, 'colour')

            rgb = backlight.split(',')
            display.set_backlight_rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]))
            time.sleep(float(config.get('main','polling_delay')))


if __name__ == "__main__":
    
    display = LcdBackpack('/dev/ttyACM0', 115200)
    
    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            display.connect()
            display.display_on()
            daemon.start()
        elif 'stop' == sys.argv[1]:
            screenoff(display)
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)