""" 
   Author: Originally Surendra Kane
   Edited by: shrocky2
   Script to control your Garge Door using an Amazon Echo. 
"""

import fauxmo
import logging
import time

#GPIO Added Information
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pinList = [7, 11, 13, 15]
for i in pinList:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)

time.sleep(.5)
#End GPIO Added Information


from debounce_handler import debounce_handler
logging.basicConfig(level=logging.DEBUG)

print " Control+C to exit program"
#Edit this section to personalize your TV Channels. The channel number is listed after each station.
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
channels = {'Garage Door':10001,
            'Item 1':10002,
            'Item 2':10003,
            'Item 3':10004,
            'Item 4':10005}
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """
    TRIGGERS = {"Garage Door":50001,
                "Item 1":50002,
                "Item 2":50003,
                "Item 3":50004,
                "Item 4":50005}

    def trigger(self,port,state):
      if state == True: #If the ON command is given, it will run this code
           if port == 10001: #Open/Close Garage Door
                GPIO.output(7, GPIO.LOW)
                time.sleep(1)
                GPIO.output(7, GPIO.HIGH)
                print "Open Garage Door"
                  
           print " "
      else: #If the OFF command is given, it will run this code
           if port == 10001: #Open/Close Garage Door
                GPIO.output(7, GPIO.LOW)
                time.sleep(1)
                GPIO.output(7, GPIO.HIGH)
                print "Open Garage Door"            
      print " "


    def act(self, client_address, state, name):
        print "State", state, "on", name, "from client @", client_address, "port:",channels[str(name)]
        self.trigger(channels[str(name)],state)
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    print " "
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            p.poll(100)
            time.sleep(0.1)
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            break
