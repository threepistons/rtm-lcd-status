#!/usr/bin/python

import sys
import webbrowser
from rtmapi import Rtm
from rtmcreds import Rtmcreds
import time
from lcdbackpack import LcdBackpack

class Taskcounter:

    def __init__(self, myfilter):
        self.myfilter = myfilter
        count = 0
        result = api.rtm.tasks.getList(filter=self.myfilter)
        for tasklist in result.tasks:
            for taskseries in tasklist:
                count += 1
        self.count = count

if __name__ == '__main__':
    # call the program as `listtasks.py api_key shared_secret [optional: token]`
    # get those parameters from http://www.rememberthemilk.com/services/api/keys.rtm
    creds = Rtmcreds()
    api = Rtm(creds.api_key, creds.shared_secret, "read", creds.token)
    
    # authenication block, see http://www.rememberthemilk.com/services/api/authentication.rtm
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
        # (a real application should store the token somewhere)
        print "New token: %s" % api.token
    
    # get all open tasks, see http://www.rememberthemilk.com/services/api/methods/rtm.tasks.getList.rtm
    
    # Variable naming:
    # * o = overdue
    # * u  = urgent (needs to be done soon, not the same as important)
    # * i  = important
    # * f  = filter
    
    incompletef = 'status:incomplete'
    importantf = 'priority:1'
    
    of = incompletef + ' and dueBefore:now'
    oif = of + ' and ' + importantf
    uf = incompletef + ' and dueWithin:"2 days of today"'
    uif = uf + ' and ' + importantf
    
    o = Taskcounter(of)
    print of + ': ' + str(o.count)
    
    oi = Taskcounter(oif)
    print oif + ': ' + str(oi.count)
    
    u = Taskcounter(uf)
    print uf + ': ' + str(u.count)
    
    ui = Taskcounter(uif)
    print uif + ': ' + str(ui.count)
    

