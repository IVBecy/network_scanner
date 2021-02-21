# Modules
import socket,time,threading,sys
from optparse import OptionParser

# Usage text
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
# Usage
def usage():
  print(usage_text)
  sys.exit()

#Setting up the options for the terminal
parser = OptionParser()
parser.set_conflict_handler("resolve")
parser.add_option("-h", "--help", dest="help", action="store_true")
parser.add_option("--ip", dest="IP")
parser.add_option("-p", "--portscan", dest="port_scan")
parser.add_option("-w", "--wp", dest="known_ports", action="store_true")
parser.add_option("-s", "--specificport", dest="specific_port")
parser.add_option("-f","--file", dest="fileName")
(options, args) = parser.parse_args()

# Main class
class Scanner():
  def __init__(self):
    self.options = options.__dict__
    self.IP = str(options.IP)
    self.openPorts = []
    self.methodCount = []
    self.trues = []
    self.methods = ["port_scan", "known_ports", "specific_port"]
    self.wellKnownports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 88, 101, 110, 111, 113, 115, 119, 135, 137, 138, 139, 143, 161, 194, 
    443, 445, 464, 512, 513, 531, 548, 626, 660, 687, 749, 751, 752, 873, 989, 990, 992, 993, 995, 1080, 1243, 1433, 1434, 
    1723, 1985, 2432, 2336, 3306, 3307, 3283, 3389, 5900, 8080, 9050, 9051, 9010, 33568, 40421, 60008]
    self.outputText = []

  # Updating info
  def update_screen(self):
    if __name__ == "__main__":
      print(self.outputText[-1])
    else:
      pass

  # Method for executing functions
  def LoopAndThread(self, ip):
    # Check args
    for i in self.options:
      if (i in self.methods) and (self.options[i] is not None):
        self.trues.append(i)
      if len(self.trues) > 1:
        print("Illegal amount of arguments")
        usage()  

    # Loop and execute
    self.startTime = time.time()
    self.outputText.append(f"\nStart time of scan: {time.ctime()}\nHost: {ip}\n\nPORT STATE\n")
    self.update_screen()

    for i in self.options:     
      # Port scanning
      if (i == "port_scan") and (self.options["port_scan"] is not None):
        self.options[i] = int(self.options[i])
        self.options[i] += 1
        #for index in range(self.iterator):
        for port in range(int(self.options[i])):
          thread = threading.Thread(target=self.portScan, args=(ip,port,))
          thread.daemon = True
          thread.start()
          time.sleep(0.01)
        self.openPorts = sorted(set(self.openPorts))
        for i in self.openPorts:
          self.outputText.append(f"{i}  open")
          self.update_screen()
        self.outputText.append(f"\nScan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.update_screen()
      # Well known port scanner
      elif (i == "known_ports") and (self.options["known_ports"] is True):
        for port in self.wellKnownports:
          thread = threading.Thread(target=self.wellKnownPortScan, args=(ip, port,))
          thread.daemon = True
          thread.start()
          time.sleep(0.01)
        self.openPorts = sorted(set(self.openPorts))
        for i in self.openPorts:
          self.outputText.append(f"{i}  open")
          self.update_screen()
        self.outputText.append(f"\nScan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.update_screen()
      # Specific port scan
      elif (i == "specific_port") and (self.options["specific_port"] is not None):
        thread = threading.Thread(target=self.SpecificPortScan, args=(ip,int(self.options[i]),)) 
        thread.daemon = True
        thread.start()
        time.sleep(0.1)
        self.openPorts = sorted(set(self.openPorts))
        for i in self.openPorts:
          self.outputText.append(f"{i}  open")
          self.update_screen()
        if len(self.openPorts) == 0:
          self.outputText.append(f"{self.options[i]} closed")
          self.update_screen()
        self.outputText.append(f"\nScan is done: {ip} scanned in  {(time.time() - self.startTime):.3} seconds")
        self.update_screen()

    # Writing to file if needed
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

# On-start
if __name__ ==  "__main__":
  #Checking for needed arguments
  if options.help:
    usage()
  if options.IP is None:
    usage()
  if (options.port_scan is None) and (options.known_ports is None) and (options.specific_port is None):
    usage()
  # Starting class
  Scanning = Scanner()
  Scanning.LoopAndThread(Scanning.IP)
