""" 
   Author: Originally Surendra Kane
   Edited by: shrocky2
  Script to control your TiVo using a Amazon Echo.
  This script originally was used to control the gpio ports on the raspberry pi, so you will see remnants of that code. 
"""

import fauxmo
import logging
import time
#Telnet Added Information
import getpass
import sys
import telnetlib
#End Telnet Added Information
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
channels = {'TiVo Pause':10000,
              'Netflix':10001,
              'Hulu':10002,
              'YouTube':10003,
              'A.B.C.':6.1,
              'N.B.C.':782,
              'C.B.S.':3.1,
              'Fox':47.1,
              'Comedy Central':754,
              'Turner':767,
              'HGTV':762,
              'ESPN':800,
              'The CW':787,
              'A and E':795,
              'Cartoon Network':872,
              'FX':753,
              'History Channel':796,
              'T.L.C.':764,
              'T.N.T.':797,
              'TV Land':731,
              'USA':757,
              'VH One':871,
              'WGN':778,
              'Travel Channel':758,
              'Open Garage':10010,
              'Garage Door':10011,
              'Close Garage':10012}
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


class device_handler(debounce_handler):
    """Triggers on/off based on 'device' selected.
       Publishes the IP address of the Echo making the request.
    """
    TRIGGERS = {"TiVo Pause":50001,
                "Netflix":50002,
                "Hulu":50003,
                "YouTube":50004,
                "A.B.C.":50005,
                "N.B.C.":50006,
                "C.B.S.":50007,
                "Fox":50008,
                "Comedy Central":50009,
                "Turner":50010,
                "HGTV":50011,
                "ESPN":50012,
                "The CW":50013,
                "A and E":50014,
                "Cartoon Network":50015,
                "FX":50016,
                "History Channel":50017,
                "T.L.C.":50018,
                "T.N.T.":50019,
                "TV Land":50020,
                "USA":50021,
                "VH One":50022,
                "WGN":50023,
                "Travel Channel":50024,
                "Open Garage":50025,
                "Garage Door":50026,
                "Close Garage":50027}

    def trigger(self,port,state):
      TiVo_IP_Address = "192.168.0.47"
#      print 'port:',  port,  "   state:", state
      if state == True: #If the ON command is given, it will run this code
        if port < 10000: #Numbers Less Than 10000 are channels, numbers above 10000 are Services like Netflix
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write('SETCH '+ str(port).replace("."," ") + '\r')
                        tn.close()
                        print "Channel Changed to", port
                except:
                        print "Telnet Error, Check TiVo IP Address"
                print " "
        else:
                if port == 10000: #TiVo Paused
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE PAUSE\r")
                         tn.close()
                         print "TiVo Paused"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                if port == 10001: #Netflix
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App Netflix is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"

                if port == 10002: #Hulu
                        print "Hulu Code Needed"
                if port == 10003: #YouTube
                        try:
                         tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                         tn.write("IRCODE TIVO\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(1)
                         tn.write("IRCODE RIGHT\r")
                         time.sleep(1)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE DOWN\r")
                         time.sleep(.4)
                         tn.write("IRCODE SELECT\r")
                         tn.close()
                         print "TiVo App YouTube is Starting"
                        except:
                         print "Telnet Error, Check TiVo IP Address"
                if port == 10004:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write('SETCH 10 1\r')
                        tn.close()
                        print "Channel Changed to", port
                if port == 10010: #Open Garage
                        GPIO.output(7, GPIO.LOW)
                        time.sleep(1)
                        GPIO.output(7, GPIO.HIGH)

                        print "Open Garage Door"
                if port == 10011: #Garage Door
                        GPIO.output(7, GPIO.LOW)
                        time.sleep(1)
                        GPIO.output(7, GPIO.HIGH)

                        print "Open Garage Door"
                if port == 10012: #Close Garage Door
                        GPIO.output(7, GPIO.LOW)
                        time.sleep(1)
                        GPIO.output(7, GPIO.HIGH)

                        print "Close Garage Door"
                print " "

               

      else: #If the OFF command is given, it will run this code
        if port == 10001 or port == 10002 or port == 10003: #Netflix, Hulu, or YoutTube OFF command is given
                try:
                        tn = telnetlib.Telnet(TiVo_IP_Address, "31339")
                        tn.write("IRCODE LIVETV\r")
                        tn.close()
                        print "TiVo LiveTv Button Pressed"
                except:
                        print "Telnet Error, Check TiVo IP Address"
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
