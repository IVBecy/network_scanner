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
        -p or --portscan [port limit]:
          Just a simple scan up until the given port number.
        ###################################
        -w or --wp:
          Scan through all of the well known ports.
         ###################################
        -s or --specificport [port]:
          Scans a specific port.

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
parser.add_option("-s", "--specificport", dest="specific_port")
(options, args) = parser.parse_args()
#Checking for needed arguments
if options.help:
  usage()
if options.IP is None:
  usage()
if (options.port_scan is None) and (options.known_ports is None) and (options.specific_port is None):
  usage()
# Main class
class Scanner():
  # On every start up
  def __init__(self):
    ####################### Variables to be used throughout the code #######################################
    self.options = options.__dict__
    self.IP = str(options.IP)
    self.openPorts = []
    self.methodCount = []
    self.trues = []
    self.iterator = 2
    self.done = False
    self.methods = ["port_scan", "known_ports", "specific_port"]
    self.wellKnownports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 88, 101, 110, 111, 115, 119, 135, 139, 143, 443, 445, 464, 531, 749, 873, 992, 993, 995, 1723, 3306, 3389, 5900, 8080]
    ################################# Checking number of arguments ########################################
    for i in self.options:
      if (i in self.methods) and (self.options[i] is not None):
        self.trues.append(i)
      if len(self.trues) > 1:
        print("Illegal amount of arguments")
        usage()  
    ######################## Looping through the options and executing them #################################
    print(f"\nStart time of scan: {time.ctime()}")
    self.startTime = time.time()
    print(f"Host: {self.IP}")
    for i in self.options:     
      # Port scanning (thread)
      if (i == "port_scan") and (self.options["port_scan"] is not None):
        print("Port scan started")
        print("\n")
        print("PORT STATE")
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
        print("\n")
        print(f"Scan is done: {self.IP} scanned in  {(time.time() - self.startTime):.3} seconds")
      #Well known port scanner
      elif (i == "known_ports") and (self.options["known_ports"] is True):
        print("Scanning all the known ports")
        print("\n")
        print("PORT STATE")
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
        print("\n")
        print(f"Scan is done: {self.IP} scanned in  {(time.time() - self.startTime):.3} seconds")

      # Specific port scan
      elif (i == "specific_port") and (self.options["specific_port"] is not None):
        print(f"Scanning, port {self.options[i]}")
        print("\n")
        print("PORT STATE")
        thread = threading.Thread(target=self.SpecificPortScan, args=(int(self.options[i]),)) 
        thread.daemon = True
        thread.start()
        time.sleep(0.1)
        for i in self.openPorts:
          print(f"{i}  open")
        if len(self.openPorts) == 0:
          print(f"{self.options[i]} closed")
        print("\n")
        print(f"Scan is done: {self.IP} scanned in  {(time.time() - self.startTime):.3} seconds")
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
  
  #Specific Port scan
  def SpecificPortScan(self, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((self.IP, port))
    if self.result == 0:
      self.openPorts.append(port)

# Calling the class
if __name__ ==  "__main__":
  Scanning = Scanner()
