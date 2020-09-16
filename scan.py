# Modules
import socket
import time
import threading
import sys
from optparse import OptionParser

# Usage menu
def usage():
  print(""" 

    Usage: scan.py [kwargs]
    
    ARGUMENTS (kwargs):

      REQUIRED:
        --ip: 
          The IP of the 'victim'

      OPTIONAL (One of these are needed):
        -p or --portscan:
          Just a simple scan up until the given port number.
        ###################################
        -w or --wp:
          Scan through all of the well known ports.

      HELP:
       -h or --help: 
      
      """)
  sys.exit()
#Setting up the options for the terminal
parser = OptionParser()
parser.set_conflict_handler("resolve")
#help
parser.add_option("-h", "--help", dest="help", action="store_true")
#vars
parser.add_option("--ip", dest="IP")
#options
parser.add_option("-p", "--portscan", dest="port_scan")
parser.add_option("-w", "--wp", dest="known_ports", action="store_true")
(options, args) = parser.parse_args()
#Checking for needed arguments
if options.help:
  usage()
if options.IP is None:
  usage()
if options.port_scan:
  options.known_ports = None
if options.known_ports:
  options.port_scan = None

# Main class
class Scanner():
  # On every start up
  def __init__(self):
    ####################### Variables to be used throughout the code #######################################
    print(f"\nStart time of scan: {time.ctime()}")
    self.options = options.__dict__
    self.IP = str(options.IP)
    self.openPorts = []
    self.iterator = 2
    self.done = False
    self.wellKnownports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 111, 115, 119, 135, 139, 143, 443, 445, 464, 992, 993, 995, 1723, 3306, 3389, 5900, 8080]
    print(f"Host: {self.IP}")
    ######################## Looping through the options and executing them #################################
    for i in self.options:
      # Port scanning (thread)
      if (i == "port_scan") and (self.options["port_scan"] != None):
        print("Port scan started")
        for index in range(self.iterator):
          for port in range(int(self.options[i])):
            thread = threading.Thread(target=self.portScan, args=(port,))
            thread.daemon = True
            thread.start()
            time.sleep(0.01)
        if port == (int(self.options[i]) - 1):
          if index == (int(self.iterator - 1)):
            if self.done == False:
              for i in self.openPorts:
                print(f"{i}  open")
                self.done = True
      #Well known port scanner
      elif (i == "known_ports") and (self.options["known_ports"] is True):
        print("Scanning all the known ports")
        for index in range (self.iterator):
          for port in self.wellKnownports:
            thread = threading.Thread(target=self.wellKnownPortScan, args=(port,))
            thread.daemon = True
            thread.start()
            time.sleep(0.01)
          if self.done == False:
            for i in self.openPorts:
              print(f"{i}  open")
              self.done = True

  ########################################## METHODS ###################################################
  # Simple port scan method 
  def portScan(self, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((self.IP, port))
    if self.result == 0:
      if port in self.openPorts:
        pass
      else:
        self.openPorts.append(port)
    else:
      pass

  # Well known port scan
  def wellKnownPortScan(self, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((self.IP, port))
    if self.result == 0:
      self.openPorts.append(port)
    else:
      pass

# Calling the class
if __name__ ==  "__main__":
  Scanning = Scanner()
