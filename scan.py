# Modules
import socket
import time
import threading
import sys
from optparse import OptionParser

# Usage menu
usage_text = """ 

    Usage: scan.py [kwargs]
    
    ARGUMENTS (kwargs):

      REQUIRED:
        ------------------------------------------------
        --ip: 
          The IP of the 'victim'.
        ------------------------------------------------

      OPTIONAL (One of these is needed):
        ------------------------------------------------
        -p or --portscan [port limit]:
          Just a simple scan up until the given port number.
        ------------------------------------------------
        -w or --wp:
          Scan through all of the well known ports.
          If used in GUI, leave the port input blank.
        ------------------------------------------------
        -s or --specificport [port]:
          Scans a specific port.
        ------------------------------------------------
        -f or --file [filename]:
          Write scan reports to a file.
        ------------------------------------------------

      HELP:
       -h or --help: 
      
      """
def usage():
  print(usage_text)
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
parser.add_option("-f","--file", dest="fileName")
(options, args) = parser.parse_args()
if __name__ == "__main__":
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
    self.iterator = 3
    self.done = False
    self.targetInfo = {}
    self.methods = ["port_scan", "known_ports", "specific_port"]
    self.wellKnownports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 88, 101, 110, 111, 115, 119, 135, 139, 143, 443, 445, 464, 531, 749, 873, 992, 993, 995, 1723, 3306, 3389, 5900, 8080, 9050, 9051, 9010]
    self.outputText = ""

  ########################################## METHODS ###################################################
  # method for looping over each option, and execute the one that is being called
  def LoopAndThread(self, ip):
    ################################ Checking number of arguments ########################################
    for i in self.options:
      if (i in self.methods) and (self.options[i] is not None):
        self.trues.append(i)
      if len(self.trues) > 1:
        print("Illegal amount of arguments")
        usage()  
    ######################## Looping through the options and executing them #################################
    print(f"Start time of scan: {time.ctime()}\nHost: {ip}\n\nPORT STATE\n")
    self.startTime = time.time()
    self.outputText += f"\nStart time of scan: {time.ctime()}\nHost: {ip}\n\nPORT STATE\n"
    for i in self.options:     
      # Port scanning (thread)
      if (i == "port_scan") and (self.options["port_scan"] is not None):
        for index in range(self.iterator):
          for port in range(int(self.options[i])):
            thread = threading.Thread(target=self.portScan, args=(ip,port,))
            thread.daemon = True
            thread.start()
            time.sleep(0.01)
        if port == (int(self.options[i]) - 1):
          if index == (int(self.iterator - 1)):
            if self.done == False:
              for i in self.openPorts:
                print(f"{i}  open")
                self.outputText += f"{i}  open\n"
                self.done = True
        print("\n")
        print(f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.outputText += f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds"
      #Well known port scanner
      elif (i == "known_ports") and (self.options["known_ports"] is True):
        for index in range (self.iterator):
          for port in self.wellKnownports:
            thread = threading.Thread(target=self.wellKnownPortScan, args=(ip, port,))
            thread.daemon = True
            thread.start()
            time.sleep(0.01)
          if self.done == False:
            for i in self.openPorts:
              print(f"{i}  open")
              self.outputText += f"{i}  open\n"
              self.done = True
        print("\n")
        print(f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.outputText += f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds"
      # Specific port scan
      elif (i == "specific_port") and (self.options["specific_port"] is not None):
        for index in range(self.iterator):
          thread = threading.Thread(target=self.SpecificPortScan, args=(ip,int(self.options[i]),)) 
          thread.daemon = True
          thread.start()
          time.sleep(0.1)
        #removing unneeded items in the array
        for ar in self.openPorts:
          if self.openPorts.count(ar) > 1:
            while self.openPorts.count(ar) != 1:
              self.openPorts.remove(ar)
        for i in self.openPorts:
          print(f"{i}  open")
          self.outputText += f"{i}  open\n"
        if len(self.openPorts) == 0:
          print(f"{self.options[i]} closed")
          self.outputText += f"{self.options[i]} closed"
        print("\n")
        print(f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.outputText += f"Scan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds"

    #Writing to file if needed
    if options.fileName:
      f = open(str(options.fileName), "a")
      f.write(self.outputText)
  
  # Simple port scan method 
  def portScan(self, ip ,port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((ip, port))
    if self.result == 0:
      if port in self.openPorts:
        pass
      else:
        self.openPorts.append(port)
    else:
      pass

  # Well known port scan
  def wellKnownPortScan(self, ip, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((ip, port))
    if self.result == 0:
      self.openPorts.append(port)
    else:
      pass
  
  #Specific Port scan
  def SpecificPortScan(self, ip, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.result = self.sock.connect_ex((ip, port))
    if self.result == 0:  
      self.openPorts.append(port)

# Calling the class
if __name__ ==  "__main__":
  Scanning = Scanner()
  Scanning.LoopAndThread(Scanning.IP)
